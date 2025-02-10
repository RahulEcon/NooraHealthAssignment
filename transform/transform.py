import os
import sys
import yaml
sys.path.insert(1, '.')
from postgres.postgres import postgres
from logger.logger import log

logger=log(__name__)

class transform:
    """Object to trigger transformation scripts, post loading.
    """     
    def __init__(self):
        self.PATH='transform/sql/'
        
    def _list_of_sql_files(self):
        """Helper method to generate a list of .sql files stored in the defined path

        Returns:
            list: List of .sql files
        """        
        if not os.path.exists(self.PATH):
            logger.error('File path is incorrect')
            return []
        return [file for file in os.listdir(self.PATH) if file.endswith(".sql")]
    
    def execute_sql_files(self):
        """Main method to run the .sql files.

        Returns:
            None: Returns None.
        """        
        for file in self._list_of_sql_files():
            postgres().sql(os.path.join(self.PATH,file),file_path=True,output=False)
            logger.info('{0} successfully executed'.format(file))
        return None
    
