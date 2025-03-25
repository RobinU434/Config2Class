import logging


def set_log_level_debug():
    logging.getLogger().setLevel(logging.DEBUG)


def set_log_level_info():
    logging.getLogger().setLevel(logging.INFO)


def set_log_level_warn():
    logging.getLogger().setLevel(logging.WARNING)
