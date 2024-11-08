__version__ = '0.1.3.15'

import logging
# Setup the logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format to include timestamp
    datefmt='%Y-%m-%d %H:%M:%S'  # Set the date/time format
)

logger = logging.getLogger(__name__)