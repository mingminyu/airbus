 select * from test.students 
where 1 = 1
    and dt = '{BATCH_DATE}'
order by dt
LIMIT 1 
