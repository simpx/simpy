"""
Tests for ``simpy.events.Event``.

"""
# Pytest gets the parameters "env" and "log" from the *conftest.py* file
import re

import pytest


def test_succeed(env):
    """Test for the Environment.event() helper function."""
    def child(env, event):
        value = yield event
        assert value == 'ohai'
        assert env.now == 5

    def parent(env):
        event = env.event()
        env.process(child(env, event))
        yield env.timeout(5)
        event.succeed('ohai')

    env.process(parent(env))
    env.run()


def test_fail(env):
    """Test for the Environment.event() helper function."""
    def child(env, event):
        try:
            yield event
            pytest.fail('Should not get here.')
        except ValueError as err:
            assert err.args[0] == 'ohai'
            assert env.now == 5

    def parent(env):
        event = env.event()
        env.process(child(env, event))
        yield env.timeout(5)
        event.fail(ValueError('ohai'))

    env.process(parent(env))
    env.run()


def test_names(env):
    def pem():
        yield env.exit()

    assert re.match(r'<Event\(\) object at 0x.*>', str(env.event()))

    assert re.match(r'<Timeout\(1\) object at 0x.*>', str(env.timeout(1)))
    assert re.match(r'<Timeout\(1, value=2\) object at 0x.*>',
                    str(env.timeout(1, value=2)))

    assert re.match(r'<Condition\(all_events, \(<Event\(\) object at 0x.*>, '
                    r'<Event\(\) object at 0x.*>\)\) object at 0x.*>',
                    str(env.event() & env.event()))

    assert re.match(r'<Process\(pem\) object at 0x.*>',
                    str(env.process(pem())))


def test_value(env):
    """After an event has been triggered, its value becomes accessible."""
    event = env.timeout(0, 'I am the value')

    env.run()

    assert event.value == 'I am the value'


def test_unavailable_value(env):
    """If an event has not yet been triggered, its value is not availabe and
    trying to access it will result in a AttributeError."""
    event = env.event()

    try:
        event.value
        assert False, 'Expected an exception'
    except AttributeError as e:
        assert e.args[0].endswith('is not yet available')


def test_triggered(env):
    def pem(env, event):
        value = yield event
        env.exit(value)

    event = env.event()
    event.succeed('i was already done')

    result = env.run(env.process(pem(env, event)))

    assert result == 'i was already done'


def test_callback_modification(env):
    """The callbacks of an event will get set to None before actually invoking
    the callbacks. This prevents concurrent modifications."""

    def callback(event):
        assert event.callbacks is None

    event = env.event()
    event.callbacks.append(callback)
    event.succeed()
    env.run(until=event)


def test_condition_callback_removal(env):
    """A condition will remove all outstanding callbacks from its events."""
    a, b = env.event(), env.event()
    a.succeed()
    env.run(until=a | b)
    # The condition has removed its callback from event b.
    assert not a.callbacks and not b.callbacks


def test_condition_nested_callback_removal(env):
    """A condition will remove all outstanding callbacks from its events (even
    if nested)."""
    a, b, c = env.event(), env.event(), env.event()
    b_and_c = b & c
    a_or_b_and_c = a | b_and_c
    a.succeed()
    env.run(until=a_or_b_and_c)
    # Callbacks from nested conditions are also removed.
    assert not a.callbacks
    assert not b.callbacks
    assert not c.callbacks
    for cb in b_and_c.callbacks:
        # b_and_c may have a _build_value callback.
        assert cb.__name__ != '_check'
    assert not a_or_b_and_c.callbacks
