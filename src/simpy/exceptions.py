"""
SimPy specific exeptions.

"""


class SimPyException(Exception):
    """Base class for all SimPy specific exceptions."""


class StopProcess(SimPyException):
    """Raised to stop a SimPy process (similar to :exc:`StopIteration`).

    In Python 2, a ``return value`` inside generator functions is not allowed.
    The fall-back was raising ``StopIteration(value)`` instead.  However, this
    is deprecated_ now, so we need a custom exception type for this.

    .. _deprecated: https://www.python.org/dev/peps/pep-0479/

    """
    def __init__(self, value):
        super(StopProcess, self).__init__(value)

    def __str__(self):
        return '%s(%r)' % (self.__class__.__name__, self.value)

    @property
    def value(self):
        """The process' return value."""
        return self.args[0]
