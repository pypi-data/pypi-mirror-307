"""Implements RAG using three NVIDIA NIMs and an external database."""

# TODO: Generalize to support databases other than Snowflake.

import os
import time

import covalent as ct
import covalent_cloud as cc
import requests
import snowflake.connector

from covalent_blueprints_ai._versions import covalent_blueprints_pkg

cc.create_env(
    name="nim-llama3-8b-instruct",
    pip=[covalent_blueprints_pkg],
    base_image="public.ecr.aws/covalent/ag-algos:l41352",
    wait=True,
)

cc.create_env(
    name="nim-arctic-embed-l",
    pip=[covalent_blueprints_pkg],
    base_image="public.ecr.aws/covalent/ag-algos:s55324",
    wait=True,
)

cc.create_env(
    name="nim-nv-rerankqa-mistral-4b-v3",
    pip=[covalent_blueprints_pkg],
    base_image="public.ecr.aws/covalent/ag-algos:m62451",
    wait=True,
)

cc.create_env(
    name="snowflake",
    pip=["snowflake-connector-python", covalent_blueprints_pkg],
    wait=True,
)


def poll_server(url, poll_freq):
    """Poll a server until a non-error response is received."""
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    while True:
        try:
            response = requests.get(url, headers=headers, timeout=60)
            response.raise_for_status()
            break
        except Exception:  # pylint: disable=broad-exception-caught
            time.sleep(poll_freq)


def start_nims_server(
    pythonpath,
    poll_url="http://localhost:8000/v1/health/ready",
    poll_freq=5,
):
    """Initialize and poll a NIM's local server."""
    if isinstance(pythonpath, list):
        pythonpath = ":".join(pythonpath)

    os.system(
        "unset VLLM_ATTENTION_BACKEND "
        "&& "
        f"PYTHONPATH={pythonpath} "
        "/bin/bash "
        "/opt/nvidia/nvidia_entrypoint.sh "
        "/opt/nim/start-server.sh "
        "&"
    )
    poll_server(poll_url, poll_freq)


llama3_exec = cc.CloudExecutor(
    env="nim-llama3-8b-instruct",
    memory="32GB",
    num_gpus=1,
    gpu_type="l40",
    num_cpus=12,
    time_limit="3 hours",
)


@cc.service(executor=llama3_exec, name="NIM Llama3 8B Service")
def nim_llama3_8b_service():
    """Hosts the NIM for 'meta/llama3-8b-instruct'."""

    # Start local server.
    pythonpath = [
        "/var/lib/covalent/lib",
        "/usr/local/lib/python3.10/dist-packages",
    ]
    start_nims_server(pythonpath)

    url = "http://localhost:8000/v1/chat/completions"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    return {"url": url, "headers": headers}


@nim_llama3_8b_service.endpoint("/generate")
def generate(url=None, headers=None, *, prompt=None, messages=None, **kwargs):
    """Generate a response to a prompt or a list of conversational
    messages. Either `prompt` or `messages` must be provided.

    Kwargs:
        prompt (str): A prompt to generate a response for.
        messages (list): A list of conversational messages.

    Any additional keyword arguments are included in the payload of
    the request to the server's POST /completions endpoint.
    """
    if not (prompt or messages):
        return "Please provide a prompt or a list of messages."

    # Construct request.
    payload = {"model": "meta/llama3-8b-instruct"}

    # Handle message or prompt.
    if messages:
        payload["messages"] = messages
    elif prompt:
        payload["messages"] = [{"role": "user", "content": prompt}]

    # Include any additional kwargs.
    for k, v in kwargs.items():
        payload[k] = v

    # Forward request to local NIM server.
    response = requests.post(url=url, headers=headers, json=payload, timeout=300)
    response.raise_for_status()
    return response.json()


emb_exec = cc.CloudExecutor(
    env="nim-arctic-embed-l",
    memory="32GB",
    num_gpus=1,
    gpu_type="l40",
    num_cpus=12,
    time_limit="3 hours",
)


@cc.service(executor=emb_exec, name="NIM Arctic Embedding Service")
def nim_arctic_embed_service():
    """Hosts the NIM for 'snowflake/arctic-embed-l'."""

    # Start local server.
    pythonpath = [
        "/var/lib/covalent/lib",
        "/usr/local/lib/python3.10/dist-packages",
        "/usr/lib/python3.10/dist-packages",
        "/app/src",
    ]
    start_nims_server(pythonpath)

    url = "http://localhost:8000/v1/embeddings"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    return {"url": url, "headers": headers}


@nim_arctic_embed_service.endpoint("/get_embedding")
def get_embedding(url=None, headers=None, *, inputs=None, truncate="NONE"):
    """Obtain the embedding for a given input text or a list of input
    texts.

    Kwargs:
        inputs (str or list): The input text or list thereof.
        truncate (str): The truncation strategy to use. Defaults to
            'NONE'.
    """
    if not inputs:
        return "Please provide an input text or list thereof."

    # Construct request.
    payload = {
        "model": "snowflake/arctic-embed-l",
        "input": inputs,
        "input_type": "query",
        "truncate": truncate,
    }

    # Forward request to local NIM server.
    response = requests.post(url=url, headers=headers, json=payload, timeout=300)
    response.raise_for_status()
    return response.json()


rr_exec = cc.CloudExecutor(
    env="nim-nv-rerankqa-mistral-4b-v3",
    memory="32GB",
    num_gpus=1,
    gpu_type="l40",
    num_cpus=12,
    time_limit="3 hours",
)


@cc.service(executor=rr_exec, name="NIM RerankQA Service")
def nim_rerankqa_service():
    """Hosts the NIM for 'nvidia/nv-rerankqa-mistral-4b-v3'."""

    # Start local server.
    pythonpath = [
        "/var/lib/covalent/lib",
        "/usr/local/lib/python3.10/dist-packages",
        "/usr/lib/python3.10/dist-packages",
        "/app/src",
    ]
    start_nims_server(pythonpath)

    url = "http://localhost:8000/v1/ranking"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    return {"url": url, "headers": headers}


@nim_rerankqa_service.endpoint("/ranking")
def ranking(url=None, headers=None, *, query=None, passages=None):
    """Rank a list of passages for a given query.

    Kwargs:
        query (dict): The query to rank passages for.
        passages (list): The list of passages to rank.
    """
    if not (query and passages):
        return {"error": "Missing query or passages"}

    # Handle simple format for ease of use.
    if isinstance(query, str):
        query = {"text": query}

    for i, passage in enumerate(passages):
        if isinstance(passage, str):
            passages[i] = {"text": passage}

    # Construct request.
    payload = {
        "model": "nvidia/nv-rerankqa-mistral-4b-v3",
        "query": query,
        "passages": passages,
    }

    # Forward request to local NIM server.
    response = requests.post(url=url, headers=headers, json=payload, timeout=300)
    response.raise_for_status()
    return response.json()


micro_ex = cc.CloudExecutor(
    env="snowflake",
    num_cpus=4,
    memory="12GB",
    time_limit="3 hours",
)


class CustomSnowflakeConnection:
    """Managed Snowflake connection with guaranteed liveness."""

    def __init__(self, user=None, password=None, account=None):
        self.user = user or os.environ["SNOWFLAKE_USER"]
        self.password = password or os.environ["SNOWFLAKE_PASSWORD"]
        self.account = account or os.environ["SNOWFLAKE_ACCOUNT"]
        self._conn = None

    @property
    def conn(self):
        """ "Refreshed connection to Snowflake."""
        if self._conn is not None:
            self._conn.close()
        self._conn = snowflake.connector.connect(
            user=self.user,
            password=self.password,
            account=self.account,
            client_session_keep_alive=True,
            client_session_keep_alive_heartbeat_frequency=1200,
        )
        return self._conn

    def cursor(self):
        """Get a cursor for a guaranteed-live connection."""
        return self.conn.cursor()


@cc.service(executor=micro_ex, name="NIM RAG Interface")
def interface_service(llama_client, emb_client, rr_client, db_config):
    """Interface for the multi-NIM network."""

    db_credentials = db_config.get("credentials")
    config = db_config.get("config")

    sf_user = db_credentials.get("user")
    sf_password = db_credentials.get("password")
    sf_account = db_credentials.get("account")

    conn = CustomSnowflakeConnection(
        user=sf_user,
        password=sf_password,
        account=sf_account,
    )

    database_name = config.get("database_name")
    schema_name = config.get("schema_name")
    table_name = config.get("table_name")
    warehouse_name = config.get("warehouse_name")

    # Set up the Snowflake DB.
    cursor = conn.cursor()
    cursor.execute(f"CREATE WAREHOUSE IF NOT EXISTS {warehouse_name}")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    cursor.execute(f"USE DATABASE {database_name}")
    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
    cursor.execute(f"USE SCHEMA {database_name}.{schema_name}")

    # Create the table if it does not exist.
    cursor.execute(
        f"CREATE OR REPLACE TABLE {table_name} "
        f"(text STRING, embedding VECTOR(float, 1024))"
    )
    return {
        "conn": conn,
        "llama_client": llama_client,
        "emb_client": emb_client,
        "rr_client": rr_client,
        "warehouse_name": warehouse_name,
        "table_name": table_name,
        "table_path": f"{database_name}.{schema_name}.{table_name}",
    }


@interface_service.endpoint("/ingest_data")
def ingest_data(warehouse_name, conn, emb_client, table_path, *, data):
    """Compute the embedding and ingest data into the Snowflake DB.

    Kwargs:
        data (str or list): The text data to ingest.
    """
    if not isinstance(data, list):
        data = [data]

    # Obtain embeddings from the Arctic Embedding service.
    outputs = emb_client.get_embedding(inputs=data)
    embeddings = [output["embedding"] for output in outputs["data"]]

    # Insert data and embeddings into the Snowflake DB.
    cursor = conn.cursor()
    cursor.execute(f"USE WAREHOUSE {warehouse_name}")
    for text, embedding in zip(data, embeddings):
        cursor.execute(
            f"INSERT INTO {table_path}(text, embedding) "
            f"SELECT '{text}', {embedding}::VECTOR(FLOAT, 1024)"
        )
    return {"ingested": data, "embeddings": embeddings}


@interface_service.endpoint("/query_llama")
def query_llama(
    conn,
    emb_client,
    rr_client,
    warehouse_name,
    llama_client,
    table_path,
    *,
    prompt=None,
    messages=None,
    retrieve=True,
    rerank=True,
    k=4,
    n=2,
):
    """Query the Llama-RAG-reranking pipeline with a prompt or a list
    of messages.

    Kwargs:
        prompt (str): A prompt to query the pipeline with.
        messages (list): A list of messages to send to the pipeline.
        retrieve (bool): Whether to retrieve texts from the DB.
        rerank (bool): Whether to re-rank the retrieved texts.
        k (int): The maximum number of texts to retrieve from the DB.
        n (int): The number of top reranked texts to return.
    """
    if not (prompt or messages):
        return "Please provide a prompt or a list of messages."

    # --# Basic LLM #--#
    if not retrieve:
        # Generate a response using the Llama3 model.
        return llama_client.generate(prompt=prompt, messages=messages)

    # --# Complete RAG #--#
    # Obtain the query embedding.
    if messages:
        inputs = [m["content"] for m in messages if m["role"] == "user"]
    else:
        inputs = [prompt]

    embeddings = emb_client.get_embedding(inputs=inputs)
    embeddings = embeddings["data"]

    # Retrieve the top k texts from the Snowflake DB.
    retrieved = []
    cursor = conn.cursor()
    cursor.execute(f"USE WAREHOUSE {warehouse_name}")
    for embedding_data in embeddings:
        embedding = embedding_data["embedding"]
        cursor.execute(
            "SELECT text, "
            f"VECTOR_COSINE_SIMILARITY(embedding, {embedding}::VECTOR(FLOAT, 1024)) "
            f"AS similarity FROM {table_path} "
            "ORDER BY similarity DESC "
            f"LIMIT {k}"
        )
        outputs = [t[0] for t in cursor.fetchall()]
        retrieved.extend([output.strip('"') for output in outputs])

    if rerank:
        # Re-rank and get the the top n <= k texts.
        query_prompt = messages[-1]["content"] if messages else prompt
        rr_outputs = rr_client.ranking(query=query_prompt, passages=retrieved)
        ranked = [retrieved[o["index"]] for o in rr_outputs["rankings"][:n]]
        retrieved = ranked

    retrieved = "- " + "\n- ".join(retrieved)
    query_messages = [
        {
            "role": "system",
            "content": (
                "Generate a brief response based on "
                f"the following information:\n{retrieved}"
            ),
        },
    ]

    if messages:
        query_messages.extend(messages)
    else:
        query_messages.append({"role": "user", "content": prompt})

    return llama_client.generate(messages=query_messages)


@ct.lattice(executor=micro_ex, workflow_executor=micro_ex)
def nims_rag_setup_workflow(db_config):
    """Deploy the services comprising the RAG pipeline."""
    llama_client = nim_llama3_8b_service()
    emb_client = nim_arctic_embed_service()
    rr_client = nim_rerankqa_service()

    rag_client = interface_service(
        llama_client,
        emb_client,
        rr_client,
        db_config=db_config,
    )

    return rag_client, llama_client, emb_client, rr_client


dispatch_id = cc.dispatch(nims_rag_setup_workflow)(
    db_config={
        "config": {
            "database_name": "nvidia_nims_rag_database",
            "schema_name": "nvidia_nims_rag_schema",
            "table_name": "nvidia_nims_rag_table",
            "warehouse_name": "nvidia_nims_rag_warehouse",
        },
        "credentials": {
            "user": "username",
            "password": "password",
            "account": "ORGID-USERID",
        },
    }
)
print(dispatch_id)
