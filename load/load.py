import os
import sys
sys.path.insert(1, '.')
from dotenv import load_dotenv, find_dotenv
from logger.logger import log
import toml
import dlt
from extract.csv_extract import csvExtract

logger=log(__name__)
class load:
    """Main object to load data into Postgres Data Warehouse/Database. Uses dlt package and design philosophy.
    """    
    def __init__(self):
        self.CONFIG= toml.load('./.dlt/config.toml')
        dotenv_path = find_dotenv('.env')
        if not dotenv_path:
            raise FileNotFoundError("Could not find the .env file")
        load_dotenv(dotenv_path)
        
        
    def _database_cred_generator(self):
        """ Hidden function to generate connection string for connecting to the postgres database.

        Returns:
            str: Postgres connection string.
        """    
        postgres_user = os.getenv('POSTGRES_USER')
        postgres_pass = os.getenv('POSTGRES_PASS')
        postgres_host = os.getenv('POSTGRES_HOST')
        postgres_db = os.getenv('POSTGRES_DATABASE')

        if not all([postgres_user, postgres_pass, postgres_host, postgres_db]):
            raise ValueError("One or more required environment variables are missing!")
        try:
            connection_string= 'postgresql://{0}:{1}@{2}:5432/{3}'.format(
                postgres_user,
                postgres_pass,
                postgres_host,
                postgres_db
            )
            print(connection_string)
        except Exception:
            logger.exception('')
            return None
        connector=dlt.destinations.postgres(connection_string)
        return connector
        
    def init_pipeline(self,pipeline_name:str):  
        """method to initialize pipeline with relevant specifications.

        Args:
            pipeline_name (str): Name of the pipeline, usually the same as the table name.

        Returns:
            dlt.pipeline: Pipeline Object
        """        
        return dlt.pipeline(
            pipeline_name=pipeline_name,
            destination=self._database_cred_generator(),
            dataset_name='raw',
            import_schema_path="load/schemas/import",
        export_schema_path="load/schemas/export"
        )
        
    def csv(self):
        """Main function to load data stored in CSVs
        """        
        csv_gen=csvExtract().extract()
        for batch in csv_gen:
            table_name=batch[0]
            data=batch[1]
            pipeline=self.init_pipeline(table_name)
            try:
                load_info=pipeline.run(data=data,
                                    table_name=table_name,
                                    write_disposition='replace')
                logger.info('{0} load to postgres successfull. Information: {1}'.format(table_name,load_info))
            except Exception:
                logger.exception('')
                exit