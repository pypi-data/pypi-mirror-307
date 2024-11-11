import logging
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.base import BaseHook
from impala.dbapi import connect
import psycopg2
import pymysql
class ImpalaToRDBSyncOperator(BaseOperator):
    @apply_defaults
    def __init__(self,
                 impala_conn_id: str,
                 rdb_type: str,
                 rdb_conn_id: str,
                 impala_query: str,
                 table: str,
                 mode: str = 'upsert',  # insert, upsert, insert_overwrite
                 batch_size: int = 1000,
                 primary_keys: str = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.impala_conn_id = impala_conn_id
        self.rdb_type = rdb_type
        self.rdb_conn_id = rdb_conn_id
        self.impala_query = impala_query
        self.table = table
        self.mode = mode
        self.batch_size = batch_size
        self.primary_keys = primary_keys if primary_keys else []

    def get_impala_connection(self):
        logging.info(f"Connecting to Impala using connection id: {self.impala_conn_id}")
        conn = BaseHook.get_connection(self.impala_conn_id)
        impala_conn = connect(
            host=conn.host,
            port=conn.port,
            user=conn.login,
            password=conn.password,
            auth_mechanism="LDAP",
            use_http_transport=True,
            http_path="cliservice",
            use_ssl=True,
        )
        logging.info("Successfully connected to Impala")
        return impala_conn

    def get_postgres_connection(self):
        logging.info(f"Connecting to PostgreSQL using connection id: {self.rdb_conn_id}")
        conn = BaseHook.get_connection(self.rdb_conn_id)
        pg_conn = psycopg2.connect(
            host=conn.host,
            port=conn.port,
            user=conn.login,
            password=conn.password,
            dbname=conn.schema
        )
        logging.info("Successfully connected to PostgreSQL")
        return pg_conn

    def get_mysql_connection(self):
        logging.info(f"Connecting to MySQL using connection id: {self.rdb_conn_id}")
        conn = BaseHook.get_connection(self.rdb_conn_id)
        mysql_conn = pymysql.connect(
            host=conn.host,
            port=conn.port,
            user=conn.login,
            password=conn.password,
            database=conn.schema,
            charset='utf8mb4'
        )
        logging.info("Successfully connected to MySQL")
        return mysql_conn

    def extract_columns(self, cursor):
        return [desc[0] for desc in cursor.description]

    def generate_insert_query(self, columns):
        column_list = ', '.join(columns)
        value_list = ', '.join(['%s'] * len(columns))
        insert_query = f"INSERT INTO {self.table} ({column_list}) VALUES ({value_list})"
        logging.info(f"Generated insert query: {insert_query}")
        return insert_query

    def generate_pg_upsert_query(self, columns):
        column_list = ', '.join(columns)
        value_list = ', '.join(['%s'] * len(columns))
        primary_key_list = ', '.join(self.primary_keys)
        update_list = ', '.join([f"{col} = EXCLUDED.{col}" for col in columns if col not in self.primary_keys])
        upsert_query = (f"INSERT INTO {self.table} ({column_list}) VALUES ({value_list}) "
                        f"ON CONFLICT ({primary_key_list}) DO UPDATE SET {update_list}")
        logging.info(f"Generated upsert query: {upsert_query}")
        return upsert_query

    def generate_mysql_upsert_query(self, columns):
        column_list = ', '.join(columns)
        value_list = ', '.join(['%s'] * len(columns))
        update_list = ', '.join([f"{col} = VALUES({col})" for col in columns if col not in self.primary_keys])
        upsert_query = (f"INSERT INTO {self.table} ({column_list}) VALUES ({value_list}) "
                        f"ON DUPLICATE KEY UPDATE {update_list}")

        logging.info(f"Generated upsert query: {upsert_query}")
        return upsert_query

    def execute(self, context):
        # Connect to Impala
        impala_conn = self.get_impala_connection()
        impala_cursor = impala_conn.cursor()

        logging.info(f"Executing Impala query: {self.impala_query}")
        # Execute Impala query
        impala_cursor.execute(self.impala_query)

        # Extract columns
        columns = self.extract_columns(impala_cursor)

        # Generate SQL based on mode
        if self.mode == 'insert':
            logging.info("Mode is 'insert'")
            insert_query = self.generate_insert_query(columns)
        elif self.mode == 'upsert':
            logging.info("Mode is 'upsert'")
            if not self.primary_keys:
                raise ValueError("Upsert mode requires a primary_key")
            if self.rdb_type == 'pg' or self.rdb_type == 'postgres':
                insert_query = self.generate_pg_upsert_query(columns)
            elif self.rdb_type == 'mysql':
                insert_query = self.generate_mysql_upsert_query(columns)
        elif self.mode == 'insert_overwrite':
            logging.info("Mode is 'insert_overwrite'")
            insert_query = f"TRUNCATE {self.table}; {self.generate_insert_query(columns)}"
        else:
            raise ValueError(f"Unsupported mode: {self.mode}")

        # Connect to DB
        if self.rdb_type=='pg' or self.rdb_type=='postgres':
            rdb_conn = self.get_postgres_connection()
            rdb_cursor = rdb_conn.cursor()
        elif self.rdb_type=='mysql':
            rdb_conn = self.get_mysql_connection()
            rdb_cursor = rdb_conn.cursor()

        logging.info(f"Starting batch synchronization with batch size: {self.batch_size}")
        # Batch synchronization
        total_rows = 0
        while True:
            rows = impala_cursor.fetchmany(self.batch_size)
            if not rows:
                break
            rdb_cursor.executemany(insert_query, rows)
            rdb_conn.commit()
            total_rows += len(rows)
            logging.info(f"Inserted/updated {len(rows)} rows, total rows processed: {total_rows}")

        logging.info(f"Completed synchronization, total rows inserted/updated: {total_rows}")

        # Close connections
        rdb_cursor.close()
        rdb_conn.close()
        impala_cursor.close()
        impala_conn.close()
        logging.info("All connections closed successfully")