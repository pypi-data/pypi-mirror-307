# Copyright 2024 Agnostiq Inc.
"""Blueprint that uses NVIDIA NIMs and a Snowflake database to
implement RAG."""

from typing import Optional

import covalent_blueprints as cb
from covalent_blueprints import blueprint, get_blueprint

from covalent_blueprints_ai._prefix import PREFIX
from covalent_blueprints_ai.database import BaseDatabaseConfig
from covalent_blueprints_ai.secrets import _account_secrets

NGC_API_KEY_MESSAGE = """No NGC API key is available.
Please pass an `ngc_api_key` argument or store a secret named 'NGC_API_KEY':

    import covalent_blueprints as cb

    cb.store_secret('NGC_API_KEY', 'my-ngc-api-key')
"""


@blueprint("NVIDIA NIMs Reranked RAG Service")
def nvidia_llama_rag(
    db_config: Optional[BaseDatabaseConfig] = None,
    ngc_api_key: str = "",
    overwrite_api_key: bool = False,
):
    """A blueprint that deploys three NVIDIA NIMs composed into a RAG
    model using an external database.

    The following NIMs are utilized by this blueprint:
    - nvcr.io/nim/meta/llama3-8b-instruct:1.0.0
    - nvcr.io/nim/snowflake/arctic-embed-l:1.0.1
    - nvcr.io/nim/nvidia/nv-rerankqa-mistral-4b-v3:1.0.1

    Args:
        db_config: Configuration for a database provider, e.g.
            Snowflake.
        ngc_api_key: API key for the NVIDIA GPU Cloud (NGC). Required
            if 'NGC_API_KEY' secret is not stored.
        overwrite_api_key: Whether to overwrite the 'NGC_API_KEY'
            account secret.

    Returns:
        Covalent blueprint that runs the composed RAG model.

    Example:
        ```
        # Run the RAG using a Snowflake database.
        from covalent_blueprints_ai import nvidia_llama_rag
        from covalent_blueprints_ai.database import SnowflakeConfig

        db_config = SnowflakeConfig(
            user="username",
            password="password",
            account="ORGID-USERID",
        )

        # Create the blueprint.
        bp = nvidia_llama_rag(
            db_config=db_config,
            ngc_api_key="your-ngc-api-key",
            overwrite_api_key=True,
        )

        # Obtain main rag client and clients individual services.
        rag_client, llama_client, emb_client, rr_client = bp.run()

        # Add data to the Snowflake table.
        ingested = rag_client.ingest_data(
            data=[
                "Agnostiq Inc. is a started founded in Toronto.",
                "Agnostic develops Covalent Cloud.",
                "Covalent Cloud\\'s website URL is covalent.xyz",
            ]
        )

        # Run the RAG model.
        response = rag_client.query_llama(
            prompt="What is Agnostiq Inc?"
        )
        print(response["choices"][0]["message"]["content"])
        ```
    """

    if db_config is None:
        from covalent_blueprints_ai.database import SnowflakeConfig

        db_config = SnowflakeConfig()

    if not ngc_api_key and "NGC_API_KEY" not in _account_secrets:
        raise RuntimeError(NGC_API_KEY_MESSAGE)

    if ngc_api_key:
        if "NGC_API_KEY" in _account_secrets and not overwrite_api_key:
            raise ValueError(
                "'NGC_API_KEY' secret already exists in your account. "
                "Pass `overwrite_api_key=True` to overwrite it."
            )
        cb.store_secret("NGC_API_KEY", ngc_api_key)

    bp = get_blueprint(f"{PREFIX}/nvidia_llama_rag")
    bp.set_default_inputs(db_config=db_config.to_dict())

    return bp
