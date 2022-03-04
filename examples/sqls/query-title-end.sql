--[sql1]
-- test1
SELECT * FROM test.t1
;
--test2
CREATE TABLE IF NOT EXSISTS test.t1
    STORED AS PARQUET
SELECT * FROM test.studuents
;
--[end]

--[sql2]
--test3
SELECT * FROM test.t2
--[end]