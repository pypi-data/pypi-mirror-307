# Copyright 2024 Agnostiq Inc.
"""Database configurations for AI Blueprints."""

import warnings
from abc import ABC, abstractmethod
from enum import Enum
from pprint import pformat
from typing import Dict, Optional

from covalent_blueprints_ai.secrets import _account_secrets


class DatabaseKind(str, Enum):
    """Enumeration of supported databases."""

    SNOWFLAKE = "snowflake"


class BaseDatabaseConfig(ABC):
    """Base class for database configuration."""

    def __init__(
        self,
        kind: str,
        credentials: Dict[str, str],
        config: Dict[str, str],
        secrets: Optional[Dict[str, str]],
        check_connection: bool = True,
        validate_configuration: bool = True,
    ):

        if kind not in list(DatabaseKind):
            raise ValueError(f"Unsupported kind of database: '{kind}'")

        self.kind = kind
        self.credentials = credentials
        self.config = config
        self.secrets = secrets

        if validate_configuration:
            self._validate_configuration()
        else:
            warnings.warn(
                "Skipping configuration validation. Set "
                "`validate_configuration=True` to validate the "
                "configuration parameters."
            )

        if check_connection:
            self._check_connection()
        else:
            warnings.warn(
                "Skipping connection check. Set `check_connection=True` "
                "to verify the connection to the database."
            )

    def to_dict(self):
        """Return the database configuration as a dictionary."""
        return {
            "kind": str(self.kind),
            "credentials": self.credentials,
            "config": self.config,
            "secrets": self.secrets,
        }

    def __repr__(self):
        return pformat(self.to_dict())

    def _validate_param(self, name: str):
        """This method checks if absent parameter values are in fact
        represented by a secret in the user's account.

        If the named param exists as a secret, return an empty string.
        Otherwise, return the param value.

        Raise a ValueError if the param is required, but is neither set
        nor stored as a secret.
        """
        if param := getattr(self, name):
            # Return the param if it is truthy.
            return param

        if self.secrets:
            # Handling for params that can be stored as secrets.
            secret_name = self.secrets.get(name)
            if secret_name in _account_secrets:
                return ""  # pass on empty string as placeholder
            if secret_name is not None:
                # Named param was not specified nor stored as secret.
                raise ValueError(
                    f"Configuration parameter '{name}' is required. "
                    f"Please pass a value for '{name}' or store its "
                    f"value as an account secret named '{secret_name}'."
                )
        # Named parameter was not specified.
        raise ValueError(f"Configuration parameter '{name}' is required")

    def _validate_configuration(self):
        """Validate the configuration."""
        for param in self.config:
            self.config[param] = self._validate_param(param)
        for param in self.credentials:
            self.credentials[param] = self._validate_param(param)

    @abstractmethod
    def _check_connection(self):
        raise NotImplementedError


class SnowflakeConfig(BaseDatabaseConfig):
    """Configuration for a Snowflake database."""

    def __init__(
        self,
        user: str = "",
        password: str = "",
        account: str = "",
        warehouse_name: str = "nvidia_nims_rag_warehouse",
        database_name: str = "nvidia_nims_rag_database",
        schema_name: str = "nvidia_nims_rag_schema",
        table_name: str = "nvidia_nims_rag_table",
        check_connection: Optional[bool] = None,
        validate_configuration: Optional[bool] = None,
    ):

        self.user = user
        self.password = password
        self.account = account
        self.warehouse_name = warehouse_name
        self.database_name = database_name
        self.schema_name = schema_name
        self.table_name = table_name

        _cred_specified = any([self.user, self.password, self.account])

        if _cred_specified and check_connection is None:
            check_connection = True
        elif check_connection is None:
            check_connection = False

        if _cred_specified and validate_configuration is None:
            validate_configuration = True
        elif validate_configuration is None:
            validate_configuration = False

        super().__init__(
            kind=DatabaseKind.SNOWFLAKE,
            credentials={
                "user": self.user,
                "password": self.password,
                "account": self.account,
            },
            config={
                "warehouse_name": self.warehouse_name,
                "database_name": self.database_name,
                "schema_name": self.schema_name,
                "table_name": self.table_name,
            },
            secrets={
                "user": "SNOWFLAKE_USER",
                "password": "SNOWFLAKE_PASSWORD",
                "account": "SNOWFLAKE_ACCOUNT",
            },
            check_connection=check_connection,
            validate_configuration=validate_configuration,
        )

    def _check_connection(self):
        """Check the connection to the Snowflake database."""
        snowflake_connector = None
        try:
            # pylint: disable=import-outside-toplevel
            import snowflake.connector as snowflake_connector

        except ImportError:
            warnings.warn(
                "Failed to check connection because the Snowflake "
                "Python connector is not installed. Please retry "
                "after running `pip install snowflake-connector-python`."
            )

        if snowflake_connector:
            try:
                snowflake_connector.connect(
                    user=self.user,
                    password=self.password,
                    account=self.account,
                )
            except Exception as e:
                raise ValueError(
                    "Failed to connect to Snowflake database. "
                    "Please verify the `user`, `password`, and `account` credentials, "
                    "or set `check_connection=False` to skip connection check."
                ) from e
