from sql_configs import * #nao estou convicto se e uma boa pratica esse tipo de importacao
from sqlalchemy import create_engine
import logging
import sys
import pymysql
import pandas as pd

# setup
engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# stablish a connection to the database instance
try:
    conn = pymysql.connect(host=HOST, user=USERNAME, passwd=PASSWORD, db=DATABASE, connect_timeout=5)
    logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()


def insert_captures(captures_df):
    # important issues and links to insert many data once. For large amounts of data can cause memory issues.
    # https://docs.sqlalchemy.org/en/14/dialects/mssql.html#mssql-pyodbc-fastexecutemany
    # https://github.com/mkleehammer/pyodbc/wiki/Features-beyond-the-DB-API#fast_executemany
    # https://stackoverflow.com/questions/48006551/speeding-up-pandas-dataframe-to-sql-with-fast-executemany-of-pyodbc
    # for repeated inserts can be used "cursor.executemany()"

    print("dataframe: ", captures_df)

    with conn.cursor() as cur:
        for index, row in captures_df.iterrows():
            stmt = "INSERT INTO {} (datetime, flag_id, url_s3, camera_id, duration, video_id) VALUES(%s, %s, %s, %s, %s, %s)".format(CAPTURE_TABLE)

            cur.execute(stmt, (row['datetime'], row['flag_id'], row['url_s3'], row['camera_id'], row['duration'], row['video_id']))
            conn.commit()
