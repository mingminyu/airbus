
SELECT * FROM test.t1
;
--test2
CREATE TABLE IF NOT EXSISTS test.t1
    STORED AS PARQUET
SELECT * FROM test.studuents
;
