from contextlib import contextmanager


@contextmanager
def null_contextmanager():
    yield
