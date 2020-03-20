import os
import time
import functools
from django.utils.text import slugify
from django.db import connection, reset_queries


def query_debugger(func):
    """
    Decorator to measure queryset quantity and time.
    """
    @functools.wraps(func)
    def inner_func(*args, **kwargs):

        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        return result

    return inner_func


def get_quiz_image_location(instance, filename: str) -> str:
    """
    Return quiz image location with format:
    /quiz/<slug:name>.<extension>.
    """
    ext = filename.split('.')[-1]
    slugified_name = slugify(instance.name)
    basename = '{}.{}'.format(slugified_name, ext)
    return os.path.join('quiz', basename)
