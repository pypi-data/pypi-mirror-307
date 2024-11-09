import logging

# Create a logger for this package without configuring it
logger = logging.getLogger("kaziro")


def log(*args, level=logging.INFO, verbose=False):
    """
    Log function that only logs messages when verbose is True.

    Args:
        *args: Variable length argument list, similar to print function.
        level: The logging level (e.g., logging.INFO, logging.DEBUG). Default is logging.INFO.
        verbose (bool): If True, the message will be logged. If False, nothing will be logged.
    """
    if verbose:
        message = " ".join(map(str, args))
        logger.log(level, message)


def setup_logger(name, debug=False):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
