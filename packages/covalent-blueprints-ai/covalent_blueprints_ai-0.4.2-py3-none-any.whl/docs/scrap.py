import os
import snowflake.connector


class CustomSnowflakeConnection:
    def __init__(self, user=None, password=None, account=None):
        self.user = user or os.environ.get("SNOWFLAKE_USER")
        self.password = password or os.environ.get("SNOWFLAKE_PASSWORD")
        self.account = account or os.environ.get("SNOWFLAKE_ACCOUNT")
        self._conn = None

    def _reset_conn(self):
        self._conn = None

    @property
    def conn(self):
        """Managed Snowflake connection object."""
        if self._conn is None:
            self._conn = snowflake.connector.connect(
                user=self.user,
                password=self.password,
                account=self.account,
            )
            self._conn.client_session_keep_alive = True
            self._conn.client_session_keep_alive_heartbeat_frequency = 1800

        return self._conn

    def cursor(self):
        """Get a cursor for a guaranteed-live connection."""
        try:
            return self.conn.cursor()
        except snowflake.connector.errors.ProgrammingError:
            print("❄️❄️❄️ Reconnecting to Snowflake...")
            self._reset_conn()
            return self.conn.cursor()
