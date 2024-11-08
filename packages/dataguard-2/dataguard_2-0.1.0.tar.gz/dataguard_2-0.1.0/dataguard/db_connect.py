import sqlalchemy as sk
import os
from sqlalchemy.engine import URL
from abc import ABC, abstractmethod


class DatabaseError(Exception):
    """Custom exception for database-related errors"""

    pass


class DatabaseConnection(ABC):
    def execute_query(self, query: str):
        """
        Method to return table data in list

        Args:
            query : raw sql query to execute

        Returns:
            List of dectionary

        Example:
            >>> result = conn.execute_query("SELECT * FROM users LIMIT 5")
                OR
            >>> query = "SELECT * FROM users LIMIT 5"
            >>> result = conn .execute_query(query)
        """
        try:
            if not self.connection:
                raise ConnectionError("Not connected to the database")
            result = self.connection.execute(sk.text(query))
            return [dict(zip(result.keys(), row)) for row in result]
        except sk.exc.SQLAlchemyError as e:
            raise DatabaseError(f"Error executing query: {str(e)}")

    def _is_mysql(self):
        return isinstance(self, MySQLConnection)

    def _is_postgres(self):
        return isinstance(self, PostgreSQLConnection)

    def _is_snowflake(self):
        return isinstance(self, SnowflakeConnection)

    def _is_bigquery(self):
        return isinstance(self, BigqueryConnection)

    def _is_databricks(self):
        return isinstance(self, DatabricksConnection)

    def _is_redshift(self):
        return isinstance(self, RedshiftConnection)

    def _is_sqlserver(self):
        return isinstance(self, SQLServerConnection)


class MySQLConnection(DatabaseConnection):
    """
    class to create a mysql connection

    This class allows to create a connection object for mysql and provide
    method to execute sql query on this object

    Args:
        user (String) :
            username
        password (String) :
            password
        host (String) :
            hostname
        database (String) :
            target database name

    Methods:
        execute_query() : str
                execute sql query for you and return result in list of dictionries
        _is_mysql() : None
                it helps you to get the connection type name

    Example:
    _________
    >>> conn = MySQLConnection(
        user = "username",
        password = "password",
        host = "hostname",
        database = "database name"
        )
    >>> conn.connect()
    >>> result = conn.execute_query("SELECT * FROM users LIMIT 5")

    """

    def __init__(self, user: str, password: str, host: str, database: str):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.connection = None

    def connect_db(self):
        try:
            engine = sk.create_engine(
                f"mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.database}"
            )
            self.connection = engine.connect()
        except sk.exc.SQLAlchemyError as e:
            raise DatabaseError(f"Error connecting to MySQL: {str(e)}")


class PostgreSQLConnection(DatabaseConnection):
    """
    class to create a postgresql connection

    This class allows to create a connection object for postgresql and provide
    method to execute sql query on this object

    Args:
        user (String) :
            username
        password (String) :
            password
        host (String) :
            hostname
        database (String) :
            target database name

    Methods:
        execute_query() : str
                execute sql query for you and return result in list of dictionries
        _is_postgres() : None
                it helps you to get the connection type name

    Example:
    _________
    >>> conn = PostgreSQLConnection(
        user = "username",
        password = "password",
        host = "hostname",
        database = "database name"
        )
    >>> conn.connect()
    >>> result = conn.execute_query("SELECT * FROM users LIMIT 5")

    """

    def __init__(self, user: str, password: str, host: str, database: str):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.connection = None

    def connect_db(self):
        try:
            engine = sk.create_engine(
                f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}/{self.database}"
            )
            self.connection = engine.connect()
        except sk.exc.SQLAlchemyError as e:
            raise DatabaseError(f"Error connecting to PostgreSQL: {str(e)}")


class SnowflakeConnection(DatabaseConnection):
    """
    class to create a snowflake connection

    This class allows to create a connection object for snowflake and provide
    method to execute sql query on this object

    Args:
        user (String) :
            user name
        password (String) :
            password
        account_identifier (String) :
            account identifier
        database (String) :
            target database name

    Methods:
        execute_query() : str
                execute sql query for you and return result in list of dictionries
        _is_snowflake() : None
                it helps you to get the connection type name

    Example:
    _________
    >>> conn = SnowflakeConnection(
        user = "username",
        password = "password",
        account_identifier =  "account_identifier",
        database = "database name"
        )
    >>> conn.connect()
    >>> result = conn.execute_query("SELECT * FROM users LIMIT 5")
    """

    def __init__(
        self, user: str, password: str, account_identifier: str, database: str
    ):
        self.user = user
        self.password = password
        self.account_identifier = account_identifier
        self.database = database
        self.connection = None

    def connect_db(self):
        try:
            engine = sk.create_engine(
                f"snowflake://{self.user}:{self.password}@{self.account_identifier}/{self.database}",
            )
            self.connection = engine.connect()
        except sk.exc.SQLAlchemyError as e:
            raise DatabaseError(f"Error connecting to Snowflake: {str(e)}")


class DatabricksConnection(DatabaseConnection):
    """
    class to create a databricks connection

    This class allows to create a connection object for databricks and provide
    method to execute sql query on this object

    Args:
        access_token (string) :
            valid access token for databricks
        server_hostname (String) :
            server host name for databricks
        http_path (String) :
            http path for databricks

    Notes:
        To find the server hostname and HTTP path, log into Databricks and search for 'Advanced Options' in the cluster settings.

    Methods:
        execute_query() : str
                execute sql query for you and return result in list of dictionries
        _is_databricks() : None
                it helps you to get the connection type name

    Example:
    _________
    >>> conn = DatabricksConnection(
        access_token = "access token",
        server_hostname = "server host name"
        http_path = "http path"
        )
    >>> conn.connect()
    >>> result = conn.execute_query("SELECT * FROM users LIMIT 5")

    """

    def __init__(self, access_token: str, server_hostname: str, http_path: str):
        self.access_token = access_token
        self.server_hostname = server_hostname
        self.http_path = http_path
        self.connection = None
        self.connect_db()

    def connect_db(self):
        try:
            engine = sk.create_engine(
                f"databricks+connector://token:{self.access_token}@{self.server_hostname}:443/hive_metastore",
                connect_args={"http_path": self.http_path},
            )
            conn = engine.connect()
            self.connection = conn
            return conn
        except sk.exc.SQLAlchemyError as e:
            raise DatabaseError(f"Error connecting to Databricks: {str(e)}")


class BigqueryConnection(DatabaseConnection):
    """
    class to create a bigquery connection

    This class allows to create a connection object for bigquery and provide
    method to execute sql query on this object

    Args:
        auth_file (String) :
            valid authentication file path
        project (String) :
            name of project

    Methods:
        execute_query() : str
                execute sql query for you and return result in list of dictionries
        _is_biquery() : None
                it helps you to get the connection type name

    Example:
    _________
    >>> conn = BigqueryConnection(
        auth_file = "file path",
        project = "project name"
        )
    >>> conn.connect()
    >>> result = conn.execute_query("SELECT * FROM users LIMIT 5")

    """

    def __init__(self, auth_file: str, project: str):
        self.auth_file = auth_file
        self.project = project
        self.connection = None

    def connect_db(self):
        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f"{self.auth_file}"
            engine = sk.create_engine(f"bigquery://{self.project}")
            self.connection = engine.connect()
        except (sk.exc.SQLAlchemyError, OSError) as e:
            raise DatabaseError(f"Error connecting to BigQuery: {str(e)}")


class RedshiftConnection(DatabaseConnection):
    """
    class to create a redshift connection

    This class allows to create a connection object for redshift and provide
    method to execute sql query on this object

    Args:
        host (String) :
            hostname
        user (String) :
            username
        password (String) :
            password
        port (Int) :
            port number
        database (String) :
            target database name

    Methods:
        execute_query() : str
                execute sql query for you and return result in list of dictionries
        _is_redshift() : None
                it helps you to get the connection type name

    Example:
    _________
    >>> conn = RedshiftConnection(
        host = "hostname",
        user = "username",
        password = "password",
        post = 1234,
        database = "database name"
        )
    >>> conn.connect()
    >>> result = conn.execute_query("SELECT * FROM users LIMIT 5")

    """

    def __init__(self, host: str, user: str, password: str, port: int, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.database = database
        self.connection = None

    def connect_db(self):
        try:
            engine = sk.create_engine(
                f"redshift+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            )
            self.connection = engine.connect()
        except sk.exc.SQLAlchemyError as e:
            raise DatabaseError(f"Error connecting to Redshift: {str(e)}")


class SQLServerConnection(DatabaseConnection):
    """
    class to create a SQL Server connection

    This class allows to create a connection object for SQL Server and provide
    method to execute sql query on this object

    Args:
        user (String) :
            user name
        password (String) :
            password
        host (String) :
            host
        port (Int) :
            port
        database (String) :
            target database name
        driver (String) :
            odbc driver to connect with database

    Methods:
        execute_query() : str
                execute sql query for you and return result in list of dictionries
        _is_sqlserver() : None
                it helps you to get the connection type name

    Example:
    _________
    >>> conn = SQLServerConnection(
        user = "username",
        password = "password",
        host = "host",
        database = "database name",
        driver = "driver" # driver="ODBC Driver 17 for SQL Server"
        )
    >>> conn.connect()
    >>> result = conn.execute_query("SELECT * FROM users LIMIT 5")
    """

    def __init__(self, user: str, password: str, host: str, port: int, database: str):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.driver = "{ODBC Driver 17 for SQL Server}"
        self.connection = None

    def connect_db(self):
        try:
            connection_string = f"DRIVER={self.driver};SERVER={self.host};PORT={self.port};DATABASE={self.database};UID={self.user};PWD={self.password};&autocommit=true"
            connection_url = URL.create(
                "mssql+pyodbc", query={"odbc_connect": connection_string}
            )
            engine = sk.create_engine(
                connection_url, use_setinputsizes=False, echo=False
            )
            self.connection = engine.connect()
            return engine
        except sk.exc.SQLAlchemyError as e:
            raise DatabaseError(f"Error connecting to SQLServer: {str(e)}")


def create_connection(db_type, **kwargs):
    """
    Create a database connection based on the specified type and parameters.

    Args:
        db_type (str): Type of database to connect to.
                    Supported types: mysql, postgresql, snowflake, databricks, bigquery, redshift
        **kwargs: Connection parameters (vary by database type)

    Returns:
        DatabaseConnection: An instance of the appropriate database connection class

    Raises:
        ValueError: If an unsupported database type is specified or if required parameters are missing

    Notes:
        - Required parameters for each database type:
        * mysql, postgresql: host, user, password, database
        * snowflake: account_identifier, user, password, database
        * databricks: server_hostname, access_token, http_path
        * bigquery: project, auth_file
        * redshift: host, user, password, port, database

        - Ensure that necessary drivers are installed for the database you're connecting to.
        - For security, it's recommended to use environment variables or secure vaults for storing sensitive
        information like passwords and access tokens.
        - BigQuery connections require a valid authentication file path.

    Example:
        >>> conn = create_connection("mysql", host="localhost", user="myuser",
        ...                          password="mypassword", database="mydb")
        >>> conn.connect()
        >>> result = conn.execute_query("SELECT * FROM users LIMIT 5")
    """
    try:
        if db_type == "mysql":
            return MySQLConnection(
                kwargs["host"],
                kwargs["user"],
                kwargs["password"],
                kwargs["database"],
            )
        elif db_type == "postgresql":
            return PostgreSQLConnection(
                kwargs["host"],
                kwargs["user"],
                kwargs["password"],
                kwargs["database"],
            )
        elif db_type == "snowflake":
            return SnowflakeConnection(
                kwargs["account_identifier"],
                kwargs["user"],
                kwargs["password"],
                kwargs["database"],
            )
        elif db_type == "databricks":
            return DatabricksConnection(
                kwargs["access_token"],
                kwargs["server_hostname"],
                kwargs["http_path"],
            )
        elif db_type == "bigquery":
            return BigqueryConnection(
                kwargs["auth_file"],
                kwargs["project"],
            )
        elif db_type == "redshift":
            return RedshiftConnection(
                kwargs["host"],
                kwargs["user"],
                kwargs["password"],
                kwargs["port"],
                kwargs["database"],
            )
        elif db_type == "sqlserver":
            return SQLServerConnection(
                kwargs["user"],
                kwargs["password"],
                kwargs["host"],
                kwargs["port"],
                kwargs["database"],
            )
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
    except KeyError as e:
        raise ValueError(f"Missing required parameter for {db_type}: {str(e)}")


# Main usage
# if __name__ == "__main__":
#     # Create a Redshift connection
#     conn = create_connection(
#         db_type="sqlserver",
#         user="SA",
#         password="Password123",
#         port=1433,
#         host="localhost",
#         database="sigma_test",
#     )
#     conn.connect()
#     result = conn.execute_query("select * from dbo.NewTable")
#     print(result)
#     if conn._is_redshift():
#         print("connection successfull")
