import logging

from pyloggroup import log_group


@log_group("MainGroup", include_prints=True)
def main_function():
    print("====1Inside main function===")
    print("*" * 20)
    logging.info("Inside main function")
    inner_function()


@log_group("InnerGroup")
def inner_function():
    print("====2Inside inner function====")
    print("*" * 20)
    logging.info("Inside inner function")
    innermost_function()


@log_group("InnermostGroup")
def innermost_function():
    print("====3Inside innermost function====")
    print("*" * 40)
    logging.info("Inside innermost function")
    print("Innermost function executed")


main_function()
