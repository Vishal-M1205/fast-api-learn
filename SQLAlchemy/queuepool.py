#
#! A pool consists of multiple available conection , no need to establish
#! new connection for every request , when the connection did its work
#! the connection is not ended either it returns to the  pool

#! the connection wont close at connection.close() it checks in to the loops for reusing

from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from db_engine import conn_url

engine = create_engine(
    url=conn_url,
    poolclass=QueuePool,  #! By default it is queue pool
    pool_size=3,
    max_overflow=10,
    pool_pre_ping=True,
    pool_timeout=30,
    pool_recycle=1800,
)

#! pool_size - no of connections it need to have
#! max_overflow - how much additional conn can  be created
#! pool_tieout - if all the conn is occupied , then it for the secs and raise the TimeOutError
#! pool_recycle the conn when the conn exceeds the time , replaced at check out , time calculated based on
#! its working time
#! pool_pre_ping - checks the conn before handling it to the app
