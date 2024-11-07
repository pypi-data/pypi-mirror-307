from datetime import datetime
from typing import Literal
import sys

def get_timestamp():
    return datetime.utcnow() # Would use `datetime.now(datetime.UTC)`, but it only works in 3.11.

def get_execution_environment() -> (
    Literal["snowflake_notebook", "google_colab", "hex", "jupyter", "python"]
):
    if "snowbook" in sys.modules:
        return "snowflake_notebook"
    if "google.colab" in sys.modules:
        return "google_colab"
    if "hex" in sys.modules or "hex_data_service" in sys.modules or "hex_api" in sys.modules:
        return "hex"
    if "ipykernel" in sys.modules:
        return "jupyter"
    return "python"


def in_cloud_environment() -> bool:
    return get_execution_environment() in ('snowflake_notebook', 'google_colab', 'hex')
