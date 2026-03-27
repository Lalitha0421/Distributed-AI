import logging

# Configure logging once
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Create and export logger
logger = logging.getLogger("ai_knowledge_system")
logger.setLevel(logging.INFO)