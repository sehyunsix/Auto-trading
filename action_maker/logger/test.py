import logging


def init_logger():
    logging.basicConfig(
        filename="example.log",
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.DEBUG,
        filemode="w",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )
    mylogger = logging.getLogger("my")
    # mylogger.setLevel(logging.INFO)
