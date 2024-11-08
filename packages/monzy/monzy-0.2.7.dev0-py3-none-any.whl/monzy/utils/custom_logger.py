import functools
import inspect
import json
import os
import sys
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

from loguru import logger as loguru_base_logger


class CustomLogger:
    """Class to create custom loggers using the Loguru package.

    This class should not be instantiated directly. Use the `get_logger` class method
    to retrieve the logger instance.

    Raises:
        RuntimeError: Raised if the class constructor is called directly.
    """

    logger = None

    def __init__(self):
        raise RuntimeError("Call get_logger() instead")

    @classmethod
    def get_logger(cls):
        """Retrieves an instance of the logger with customised settings.

        The logger is configured to output logs to stderr with a specified format and
        log level set by the environment variable `LOG_LEVEL`, defaults to INFO.

        Returns:
            Logger: An instance of the customised Loguru logger.
        """
        if not cls.logger:
            cls.logger = loguru_base_logger
            cls.logger.remove()
            cls.logger = cls.logger.patch(cls.logger_patch)
            cls.logger.add(
                sys.stderr, format="{extra[serialized]}", level=os.getenv("LOG_LEVEL", "INFO")
            )

        return cls.logger

    @classmethod
    def logger_patch(cls, record: Dict[str, Any]) -> None:
        """Customises the log record format for the Loguru logger.

        This method is used to patch the logger and serialize the log record data into JSON format.

        Args:
            record (Dict[str, Any]): Dictionary containing log record data.
        """
        record["extra"]["serialized"] = json.dumps(
            {
                "timestamp": str(record["time"]),
                "module": record["name"],
                "function": record["function"],
                "line_number": record["line"],
                "level": record["level"].name,
                "message": record["message"],
                "extra": record["extra"],
            }
        )


def suppress_args_to_mask(
    list_of_args: List[Tuple[str, Any]], params_to_mask: List[str]
) -> List[Tuple[str, Any]]:
    """Filters out arguments to be masked, replacing them with 'suppressed'.

    Args:
        list_of_args (List[Tuple[str, Any]]): List of function arguments.
        params_to_mask (List[str]): List of string representations of params to mask.

    Returns:
        List[Tuple[str, Any]]: List of arguments with non-primitives suppressed.
    """
    filtered_args = [
        x if x[0] not in params_to_mask else (x[0], "suppressed") for x in list_of_args
    ]
    return filtered_args


def suppress_non_primitive_args(list_of_args: List[Tuple[str, Any]]) -> List[Tuple[str, Any]]:
    """Filters out non-primitive arguments, replacing them with 'suppressed'.

    Args:
        list_of_args (List[Tuple[str, Any]]): List of function arguments.

    Returns:
        List[Tuple[str, Any]]: List of arguments with non-primitives suppressed.
    """
    filtered_primitives = [x if is_primitive(x[1]) else (x[0], "suppressed") for x in list_of_args]
    return filtered_primitives


def is_primitive(obj: Any) -> bool:
    """Checks if an object is an instance of a primitive type.

    Args:
        obj (Any): Standard Python object.

    Returns:
        bool: True if the object is a primitive type, False otherwise.
    """
    primitives = (bool, str, int, float, type(None))
    return isinstance(obj, primitives)


def get_aws_context_value(list_of_args: List[Tuple[str, Any]], key: str) -> Optional[str]:
    """Retrieves a specific value from the AWS context argument based on the provided key.

    Args:
        list_of_args (List[Tuple[str, Any]]): List of arguments from the function.
        key (str): The key to retrieve from the context argument.

    Returns:
        Optional[str]: The value associated with the key in the AWS context, or None if not found.
    """
    for arg_tuple in list_of_args:
        if "context" in arg_tuple:
            context_arg = arg_tuple[1]
            return getattr(context_arg, key)
    return None


def get_func_signature(list_of_args: List[Tuple[str, Any]]) -> str:
    """Generates a string representation of the function's signature, with parameters filtered and
    masked as needed.

    Args:
        list_of_args (List[Tuple[str, Any]]): List of arguments passed to the function.
        kwargs (Dict[str, Any]): Dictionary of keyword arguments passed to the function.

    Returns:
        str: String representation of the function's signature.
    """
    args_repr = [f"{a[0]}={a[1]!r}" for a in list_of_args]
    signature = ", ".join(args_repr)
    return signature


def loggable(
    _func: Optional[Callable] = None,
    *,
    log_params: bool = True,
    log_primitive_params_only: Optional[bool] = True,
    log_response: bool = False,
    params_to_mask: Optional[List[str]] = None,
) -> Callable:
    """Decorator to log standardized info level logs, including start and end of function signals,
    parameters, responses, and timing.

    By default response values are suppressed and only primitive types (bool, str, int, float, None)
    are logged, while other types are suppressed.

    Args:
        _func (Callable, optional): Function to wrap with the decorator. Defaults to None.
        log_params (bool, optional): Whether to log the function parameter names and values. Defaults to True.
        log_primitive_params_only (Optional[bool], optional): Whether to log only primitive parameter types. Defaults to True.
        log_response (bool, optional): Whether to log the function response. Defaults to False.
        params_to_mask (Optional[List[str]], optional): List of parameters to mask. Defaults to None.

    Returns:
        Callable: Wrapped function with logging.
    """
    if params_to_mask is None:
        params_to_mask = []

    def decorator_log(func: Callable) -> Callable:
        """Decorator that wraps a function to add logging functionality.

        Args:
            func (Callable): Function to be wrapped.

        Returns:
            Callable: Wrapped function with logging.
        """

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Wrapper function that adds logging around the execution of the decorated function.

            Args:
                *args (Any): Positional arguments passed to the function.
                **kwargs (Any): Keyword arguments passed to the function.

            Returns:
                Any: Result of the decorated function.
            """
            logger = CustomLogger.get_logger()

            sig_keys = inspect.signature(func).parameters.keys()
            # Get the values of the kwargs in the order defined by the function signature.
            kw_vals = tuple(kwargs[k] for k in sig_keys if kwargs.get(k) is not None)
            list_of_args = list(zip(sig_keys, args + kw_vals))

            if os.getenv("AWS_EXECUTION_ENV"):
                if func.__name__ in ("handler", "lambda_handler"):
                    aws_request_id = get_aws_context_value(list_of_args, "aws_request_id")
                    aws_log_stream_name = get_aws_context_value(list_of_args, "log_stream_name")

                    # Setting AWS_REQUEST_ID for subsequent @loggable calls on non-handler functions
                    os.environ["AWS_REQUEST_ID"] = aws_request_id
                else:
                    aws_request_id = os.getenv("AWS_REQUEST_ID")
                    aws_log_stream_name = os.getenv("AWS_LAMBDA_LOG_STREAM_NAME")

                extra = {
                    "aws_request_id": aws_request_id,
                    "aws_log_stream_name": aws_log_stream_name,
                }
                logger.configure(extra=extra)

            if log_params:
                list_of_args = suppress_args_to_mask(list_of_args, params_to_mask)
                if log_primitive_params_only:
                    list_of_filtered_args = suppress_non_primitive_args(list_of_args)
                    signature = get_func_signature(list_of_filtered_args)
                else:
                    signature = get_func_signature(list_of_args)

                start_msg = f"{func.__name__} [{signature}]"
            else:
                start_msg = f"{func.__name__}"

            logger.info(start_msg + " : start")
            try:
                start = time.perf_counter()
                result = func(*args, **kwargs)
                end = time.perf_counter()

                base_end_msg = f"{start_msg} : end : time taken [{round(end - start, 5)}]s : response : [{type(result)}="
                if not log_response:
                    end_msg = f"{base_end_msg}<suppressed>]"
                else:
                    end_msg = f"{base_end_msg}<{result}>]"

                logger.info(end_msg)
                return result
            except Exception as e:
                logger.exception(
                    f"Exception raised in function {func.__name__}. Exception: {str(e)}"
                )
                raise e

        return wrapper

    if _func is None:
        return decorator_log
    else:
        return decorator_log(_func)
