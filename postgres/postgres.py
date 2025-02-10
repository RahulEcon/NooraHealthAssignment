import os
import sys
import toml
import psycopg2
from psycopg2.extras import RealDictCursor
sys.path.insert(1, '.')
from logger.logger import log

logger=log(__name__)

class postgres:
    """Module for running sql queries on postgres.
    """    
    def __init__(self):
            CONFIG= toml.load('./.dlt/config.toml')
                
    def _conn(self):
        """Helper function generating a connector object for the postgres module.
        """        
        def __check_if_cred_is_there(cred_str:str):
            if os.getenv(cred_str)==None:
                logger.critical('Credential {0} not defined in config.toml'.format(cred_str))
                raise Exception.add_note('Credential {0} not defined in config.toml'.format(cred_str))
            else:
                return os.getenv(cred_str)
        try:
            conn=psycopg2.connect(database=__check_if_cred_is_there('POSTGRES_DATABASE'),
                                  user=__check_if_cred_is_there('POSTGRES_USER'),
                                  password=__check_if_cred_is_there('POSTGRES_PASS'),
                                  host=__check_if_cred_is_there('POSTGRES_HOST')
                                  )
            logger.debug('Postgres connection opened successfully.')
            return conn
        except Exception as err:
            logger.critical('POSTGRES:{0}'.format(err))
            return None
        
    def sql(self,sql:str,file_path:bool,output:bool):
        """Method used to run SQL queries on postgres.

        Args:
            sql (str): relevant .sql file or sql string
            file_path (bool): if true, uses file path to a .sql file. Else it expects a string
            output (bool): If True, returns output of query, else only runs the query.

        Returns:
            dict: Output of SQL query.
        """        
        conn=self._conn()
        if file_path==True:
            with open(sql, "r", encoding="utf-8") as file:
                sql_statement=file.read()
        else:
            sql_statement=sql
        if conn==None:
            logger.error('POSTGRES: Connection failed, cannot run statement: {0}'.format(sql_statement))
            exit
        else:
            pass
        cur=conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(sql_statement)
            logger.debug('POSTGRES | SQL | PASS | Query: "{0}" run successfully!'.format(sql_statement))
        except Exception as err:
            logger.critical('POSTGRES | SQL | FAIL | {0} | {1}'.format(sql_statement,err))
            conn.rollback()
            conn.close()
            logger.debug('FAIL | Execution rolledback, and Postgres connection closed, after failed execution.')
            return None
        if output==True:
            result=cur.fetchall()
            result=[dict(row) for row in result]
        else:
            result=None
        conn.commit()
        conn.close()
        logger.debug('SUCCESS | Postgres connection closed, after successful execution.')
        return result