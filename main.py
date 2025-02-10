import os
import sys
sys.path.insert(1, '.')
from load.load import load
from transform.transform import transform
from tests.table_validation import tableValidation
from logger.logger import log

logger=log(__name__)

# Run the extract and load process
try:
    load().csv()
except:
    pass
# Create relevant Tables
try:
    transform().execute_sql_files()
except:
    pass
# Run data validation checks (Examples)
if tableValidation('raw','messages').date_column_in_consistent_format('inserted_at',"%m/%d/%Y %H:%M:%S")==True:
    logger.info('Date validation passed')
    pass
else:
    raise Exception('Date Validation failed!')
if tableValidation('raw','stg_messages').column_has_blanks('uuid')==True:
    raise Exception('Null Validation Failed')
else:
    logger.info('Null Validation Passed')
if tableValidation('raw','stg_messages').column_contains_only_allowed_values('direction',['outbound','inbound'])==True:
    logger.info('Value validation passed!')
else:
    raise Exception('Value validation failed!')