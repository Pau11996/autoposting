from autoposting_app.cli import main
from autoposting_app.logging import get_logger

# Initialize logging early
logger = get_logger("main")

if __name__ == "__main__":
    logger.info("Starting autoposting application")
    try:
        main()
    except Exception as e:
        logger.error(f"Application failed with error: {e}", exc_info=True)
        raise
