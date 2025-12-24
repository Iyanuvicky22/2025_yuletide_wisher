"""
Pass
"""
import os
import logging
from datetime import datetime


timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
day_stamp = datetime.now().strftime("%Y-%m-%d")

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, f"{day_stamp}_yuletide.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    filename=log_path,
    filemode='a'
)

logger = logging.getLogger(__name__)