import logging

from IPython.display import display as ipy_display

logger = logging.getLogger("ipy")


def in_ipynb():
    try:
        from IPython import get_ipython

        if "IPKernelApp" not in get_ipython().config:
            return False
    except:  # noqa: E722
        return False
    return True


def display(obj: any):
    if not in_ipynb():
        return
    ipy_display(obj)


def log(
    msg: object,
    *args: object,
):
    logger.info(msg, *args)
