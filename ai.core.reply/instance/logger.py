from loguru import logger
import sys

# Show which module makes output
corr_id = 'BASIC'

logger.remove()
logger.add(sys.stdout, format="[{level.icon}  {level.name[0]}]\t{time:YYYY-MM-DD HH:mm:ss.SSS}\tCID: {extra[corr_id]}\t{message}")

if __name__ == "__main__":
    # Pytest does not help with checkout output highlighting
    logger = logger.bind(corr_id=corr_id)
    logger.warning("This is a module and should not be run directly. Running self-tests...")
    logger.info("Okay!")
