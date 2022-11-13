import logging
logger = logging

logger.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(module)s :: %(message)s')
logger.getLogger("_universal").setLevel(logging.WARNING)

