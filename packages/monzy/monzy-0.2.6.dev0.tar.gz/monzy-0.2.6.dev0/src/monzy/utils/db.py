import os

import pandas as pd
import sqlalchemy

from monzy.utils import sql_templates
from monzy.utils.custom_logger import logger


class Db:
    """Class to manage connection to a database and perform SQL operations."""

    def __init__(self):
        """Initialize Database connection."""
        self.conn = self.connect_to_db()
        logger.info(f"Connected to database: {os.getenv('DB_NAME')}")

    def connect_to_db(self):
        """Method to establish a connection to the database.

        Returns:
            sqlalchemy.engine.base.Connection: Database connection object.
        """
        username = os.getenv("DB_USER")
        password = os.getenv("DB_PASS")
        host = os.getenv("DB_HOST")
        database_type = os.getenv("DB_TYPE")
        database_name = os.getenv("DB_NAME")
        port = os.getenv("DB_PORT")
        sql_string = f"{database_type}://{username}:{password}@{host}:{port}/{database_name}"
        return sqlalchemy.create_engine(sql_string).connect()

    def query(self, sql, return_data=True) -> pd.DataFrame:
        """Execute an SQL query against the database.

        Args:
            sql (str): SQL query to execute.
            return_data (bool, optional): Whether to return data (True) or not (False). Defaults to True.

        Returns:
            pd.DataFrame: Resulting DataFrame if return_data=True.
        """
        if return_data:
            df = pd.read_sql_query(sql, self.conn)
            return df
        else:
            self.conn.execute(sqlalchemy.text(sql))
            self.conn.commit()

    def insert(self, table, df=None, sql=None, if_exists="append"):
        """Insert data into a table in the database.

        Args:
            table (str): Table name to insert into.
            df (pd.DataFrame, optional): DataFrame containing data to insert. Defaults to None.
            sql (str, optional): Custom SQL insert statement. Defaults to None.
            if_exists (str, optional): Action if the table exists ('append' or 'replace'). Defaults to 'append'.
        """
        if sql:
            insert_sql = f"INSERT INTO {table} (\n{sql}\n);"
            self.query(insert_sql, return_data=False)
            logger.info(f"Data inserted into {table}")
        else:
            rows = len(df)
            chunksize = 20000 if rows > 20000 else None
            schema, table_name = table.split(".")
            df.to_sql(
                schema=schema,
                name=table_name,
                index=False,
                con=self.conn,
                if_exists=if_exists,
                method="multi",
                chunksize=chunksize,
            )
            logger.info(f"{rows} rows inserted into {schema}.{table_name}")

    def delete(self, table: str, data: str) -> None:
        """Method to delete data from a table in the database.

        Args:
            table (str): Table name from which data will be deleted.
            data (pd.DataFrame): DataFrame containing data to be deleted.
        """
        sql_delete = sql_templates.delete.format(table=table, data=data)
        logger.info(f"Running delete statement: {sql_delete}")
        self.query(sql=sql_delete, return_data=False)
