from logging import getLogger, DEBUG, StreamHandler, Formatter


logger = getLogger('firstofficerslog')

# Logging configuration
logger.setLevel(DEBUG)

# create console handler
console_info_handler = StreamHandler()
console_info_handler.setLevel(DEBUG)

# create formatter and add it to the handlers
console_info_formatter = Formatter('>> %(message)s')

console_info_handler.setFormatter(console_info_formatter)

# add the handlers to the logger
logger.addHandler(console_info_handler)