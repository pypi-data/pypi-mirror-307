# Copyright 2024 Agnostiq Inc.
"""General utilities for Covalent AI Blueprints."""
import covalent_cloud as cc


class IterableAccountSecrets:
    """Singleton class to manage Covalent Cloud account secrets.

    This class can only access the names of existing secrets, but not
    their values.
    """

    _instance = None

    def __init__(self):
        self.secrets = cc.list_secrets()

    def __iter__(self):
        return iter(self.secrets)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IterableAccountSecrets, cls).__new__(cls)
        return cls._instance


_account_secrets = IterableAccountSecrets()
