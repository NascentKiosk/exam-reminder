import logging
import os
from opencensus.ext.azure.log_exporter import AzureLogHandler

# Use the same environment variable you set in the container
connection_str = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING")

logger = logging.getLogger(__name__)

if connection_str:
    logger.addHandler(AzureLogHandler(connection_string=connection_str))

logger.setLevel(logging.INFO)

# Test logs
logger.info("✅ Test log: App Insights is working!")
logger.warning("⚠️ Test log: This is a warning")
logger.error("❌ Test log: This is an error")