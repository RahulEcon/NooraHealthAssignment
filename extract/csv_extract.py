import os
import sys
import csv
import toml
sys.path.insert(1, '.')
from logger.logger import log

logger=log(__name__)

class csvExtract:
    """Object to extract data from CSVs stored in specified path.
    """    
    def __init__(self):
        self.CONFIG=".dlt/config.toml"
    
    def _config(self,spec_key:str):
        """Helper function used to parse config for relevant config sepcifications

        Args:
            spec_key (str): Key to identify specification. Please refer config file for more.

        Returns:
            dict: Specified config spec
        """        
        try:
            config=toml.load(self.CONFIG)
        except FileNotFoundError:
            logger.critical('{0} not found. Please verify. Exiting..'.format(self.CONFIG))
            return None
        except Exception:
            logger.exception('')
            return None
        try:
            extract_specs=config['extract']['csv']
        except KeyError:
            logger.critical('"{0}" is missing details on extracting csv. Please verify. Exiting..'.format(self.CONFIG))
            return None
        except Exception:
            logger.exception('')
            return None
        try:
            return extract_specs[spec_key]
        except KeyError:
            logger.critical('{0} is not a valid spec for csvExtract. Please check file "{1}"'.format(spec_key,self.CONFIG))
            return None
        except Exception:
            logger.exception('')
            return None
        
    def extract(self): 
        """Main generator function to extract data stored in csvs in sepcified folder.

        Returns:
            None: If there is an error

        Yields:
            tuple: Consists of a tuple starting with the table name, followed by a list of dictinaries of the rows sepcified in the batch size.
        """        
        PATH=self._config('path')
        BATCH_SIZE=self._config('batch_size')
        if PATH==None or BATCH_SIZE==None:
            logger.critical('Extract failed due to incorrect config.')
            return None
        else:
            pass
        # Check if data path exists
        if not os.path.exists(PATH):
            logger.critical('"{0}" does not exist. Unable to loacate csv files.'.format(PATH))
            return None
        for file_name in os.listdir(PATH):
            if file_name.endswith(".csv"):
                file_path = os.path.join(PATH, file_name)
                table_name = os.path.splitext(file_name)[0]
                with open(file_path, mode="r", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    batch = []
                    for row in reader:
                        batch.append(dict(row))
                        if len(batch) == BATCH_SIZE:
                            yield table_name, batch
                            batch = []
                    if batch:  
                        yield table_name, batch
        
        
        

