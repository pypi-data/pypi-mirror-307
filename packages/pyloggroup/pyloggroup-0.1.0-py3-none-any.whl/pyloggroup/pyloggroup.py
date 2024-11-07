import builtins
import logging
from functools import wraps

# Set up basic configuration for logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
)

# Initialize a global indent level and prefix list
indent_level = 0
indent_prefixes = [""]  # Root level has no prefix


class TreeFormatter(logging.Formatter):
    """
    Custom logging formatter to handle tree-like indentation.
    """

    def format(self, record):
        global indent_level
        # Determine the appropriate prefix for the current indent level
        prefix = (
            indent_prefixes[indent_level] if indent_level < len(indent_prefixes) else ""
        )
        # Add the timestamp, log level, file, line number, and message to the format
        formatted_message = super().format(record)
        return f"{prefix}{formatted_message}"


# Add a custom formatter to the root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# Set the formatter to include timestamp, log level, filename, line number, and message
formatter = TreeFormatter(
    "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.handlers = [console_handler]  # Reset handlers to use only our handler


def log_group(group_name, include_prints=True):
    """
    Decorator to create log groups for a function, using tree-like indentation.

    Parameters:
    - group_name: The name of the log group.
    - include_prints: If True, print statements within the decorated function will be captured in the log.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            global indent_level
            # Update the indentation prefixes for the current level
            indent_prefixes.append("│   " * indent_level + "├── ")
            # Temporarily replace the built-in print function if include_prints is True
            original_print = builtins.print
            if include_prints:

                def log_print(*args, **kwargs):
                    message = " ".join(map(str, args))
                    logger.info(f"[PRINT] {message}")

                builtins.print = log_print  # Override print with log capturing
            else:
                builtins.print = original_print  # Ensure print behaves normally if include_prints is False

            # Log entry into the group
            logger.info(f"Entering log group: {group_name}")
            indent_level += 1  # Increase indentation level

            try:
                result = func(*args, **kwargs)
            finally:
                indent_level -= 1  # Decrease indentation level
                # Restore the original print function
                builtins.print = original_print
                # Log exit from the group
                logger.info(f"Exiting log group: {group_name}")
                indent_prefixes.pop()  # Remove the current level's prefix

            return result

        return wrapper

    return decorator
