import logging
import os
import sys

format_str = " %(asctime)s : %(levelname)s : %(message)s  "
log_dir_name = "logs"
log_file_path = os.path.join(log_dir_name, "running.log")
os.makedirs(log_dir_name, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=format_str,
    handlers=[logging.FileHandler(log_file_path), logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger("simple_computervision")
