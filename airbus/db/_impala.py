# coding: utf8
import re
import time
import logging
import pandas as pd
from rich.logging import RichHandler
from rich.console import Console
from rich.syntax import Syntax
from typing import Dict, Text, List
from impala.hiveserver2 import HiveServer2Connection, HiveServer2Cursor
from impala.dbapi import connect
from impala.util import as_pandas
from airbus.decorators import retry


class ImpalaRunner(object):
    retry_times = 5
    sleep_time = 60

    def __init__(
            self,
            db_config: Dict = None,
            sql: Text = None,
            sql_file: Text = None,
            context: Dict = None,
            verbose: bool = False,
            ) -> None:
        self.db_config = db_config
        self.sql_file = sql_file
        self.context = context
        self.verbose = verbose
        self.log = logging.getLogger("Impala")
        self.console = Console()
        self.conn = self._create_conn()

        if not sql and not sql_file:
            self.log.exception("[red]sql[/] and [red]sql_file[/] can not be [green]None[/]", extra={"makeup": True})

        if sql_file:
            self.sqls = self._parse_sqlfile()
        else:
            self.sqls = {"query": self._formatted_sql(sql)}


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close_conn()
        self.log.info("Impala Connection has been closed!")

    @retry
    def _create_conn(self) -> HiveServer2Connection:
        """Create a connection for Impala database according to db_config"""
        host = self.config["host"]
        port = self.config["port"]
        user = self.config["user"]
        password = self.config["password"]
        auth_mechanism = self.config["auth_mechanism"]

        conn = None

        if isinstance(host, Text):
            conn = connect(
                        host=host,
                        port=port,
                        user=user,
                        password=password,
                        auth_mechanism=auth_mechanism,
                        timeout=60)
        elif isinstance(host, List):
            for h in host:
                try:
                    conn = connect(
                                host=h,
                                port=port,
                                user=user,
                                password=password,
                                auth_mechanism=auth_mechanism,
                                timeout=60)
                    break
                except Exception as e:
                    self.logging.err(e)
        else:
            self.log.exception("[bold green]host[/] type must be [red]str[/] or [red]list[/]",
                            extra={"markup": True})

        if conn is None:
            self.log.Exception("Can not connect Impala Database with db_config")

        return conn

    def _close_conn(self):
        self.conn.close()

    def _parse_sqlfile(self):
        with open(self.filename, "r", encoding="utf8") as f:
            file_context = f.read().replace("${", "{")
            pat = r"--\[(.*?)\](.*?)\n--\[end\].*?" if file_context.find("[end]" != -1) else r"--\[(.*?)\](.*?)\n--\[.*?\]"

            if len(self.context) > 0:
                sqls = dict([(k, v.format_map(self.context))
                            for k, v in re.findall(pat, file_context, re.S) if v != ""])
            else:
                sqls = dict([(k, v) for k, v in re.findall(pat, file_context, re.S) if v != ""])

        return sqls

    def _get_sqls(self):
        pass

    def _format_sql(self, sql):
        """Formatted query sql with parameters in context.

        :param sql: str, Query SQL
        :return: str, Formatted SQL
        """
        if self.context:
            sql = sql.replace("${", "{").format_map(self.context)

        return sql

    @staticmethod
    def _verify_df(df: pd.DataFrame = None) -> pd.DataFrame:
        """Update Dataframe columns"""
        if df is None:
            raise Exception("Parameter `df` can not be None!")

        df.columns = [col.rsplit('.', 1)[-1] for col in df.columns]

        # update columns type
        for col in df.columns:
            series = df[col][df[col].notnull()]

            if not series.empty:
                if type(series.iloc[0]).__name__ == 'Decimal':
                    df[col] = df[col].astype(float)
                if type(series.iloc[0]).__name__ == 'Timestamp':
                    df[col] = df[col].astype(str)

        return df

    def _cursor_to_df(self, cursor: HiveServer2Cursor) -> pd.DataFrame:
        """Fetch all records with cursor."""
        data = cursor.description

        if data is not None and hasattr(data, '__iter__'):
            names = [metadata[0] for metadata in data]
            df = as_pandas(cursor)
            df.columns = names
        else:
            df = pd.DataFrame()

        df = self._verify_df(df)

        return df

    def _run_sql(self, sql: Text = None) -> pd.DataFrame:
        """Execute One SQL"""
        cur = self.conn.cursor()

        if sql.replace(" ", "") == "":
            self.log.info("Executed sql is empty")
            cur.close()
            return pd.DataFrame()

        else:
            self.log.info("Starting run sql:\n \033[1;34m{sql}\033[0m \n".format(sql=sql))
            self.console.info(code=sql, lexer="mysql", line_numbers=True)

            if self.verbose

        pass