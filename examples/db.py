from pathlib import Path
from airbus.db import ImpalaRunner, impala_to_df


root_path = Path(__file__).parent

databases = {
    "host": "impala.airbus.com",
    "port": 25005,
    "user": "",
    "password": "",
    "auth_mechanism": "plain"
}

runner = ImpalaRunner(
        db_config=databases,
        sql_file=root_path / 'sqls' / 'query-context.sql',
        context={"BATCH_DATE": '2022-03-01'},
        retry_times=2,
        sleep_time=10,
        verbose=False,
        )
print(runner.run_sql_block(title="sql1"))
print(runner.sqls)

df = impala_to_df(
        db_config=databases,
        sql="SELECT * FROM test.stuents WHERE 1 = 1  AND dt = '{BATCH_DATE}' ORDER BY dt LIMIT 1",
        context={"BATCH_DATE": '2022-03-01'},
        retry_times=2,
        sleep_time=10,
        verbose=True,
    )
print(df)




