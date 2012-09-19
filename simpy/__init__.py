# encoding: utf-8
"""
With SimPy, simulating is fun again!

"""
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

from simpy.core import Context, Process, Interrupt, Failure, simulate, step


__all__ = ['Simulation', 'Interrupt', 'Failure', 'test']
__version__ = '3.0a1'


def test():
    """Runs SimPy’s test suite via *py.test*."""
    import os.path
    try:
        import mock
        import pytest
    except ImportError:
        print('You need pytest and mock to run the tests. '
              'Try "pip install pytest mock".')
    else:
        pytest.main([os.path.dirname(__file__)])
