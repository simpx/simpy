.. only:: html

    .. figure:: _static/simpy-logo-small.png
        :align: center

        Discrete event simulation for Python

        `News <https://plus.google.com/101634625602509193865>`_ |
        `PyPI <https://pypi.python.org/pypi/simpy>`_ |
        `Bitbucket <https://bitbucket.org/simpy/simpy/>`_ |
        `Issues
        <https://bitbucket.org/simpy/simpy/issues?status=new&status=open>`_ |
        `Mailing list <https://groups.google.com/forum/#!forum/python-simpy>`_

========
Overview
========

.. only:: html

    .. sidebar:: Documentation

        :ref:`Tutorial <intro>`
            learn the basics of SimPy in just a couple of minutes

        :ref:`Topical Guides <guides>`
            guides covering various features of SimPy in-depth

        :ref:`Examples <examples>`
            usage examples for SimPy

        :ref:`API Reference <api>`
            detailed description of SimPy’s API

        :ref:`Contents <contents>`
            for a complete overview

        :ref:`About <about>`
            non-technical stuff (history, change logs, ports, …)

SimPy is a process-based discrete-event simulation framework based on standard
Python.

Processes in SimPy are defined by Python `generator functions
<http://docs.python.org/3/glossary.html#term-generator>`_ and may, for example,
be used to model active components like customers, vehicles or agents.  SimPy
also provides various types of :ref:`shared resources <shared-resources>` to
model limited capacity congestion points (like servers, checkout counters and
tunnels).

Simulations can be performed :ref:`“as fast as possible” <simulation-control>`,
in :ref:`real time <realtime>` (wall clock time) or by manually :ref:`stepping
<simulation-step>` through the events.

Though it is theoretically possible to do continuous simulations with SimPy, it
has no features that help you with that. On the other hand, SimPy is overkill
for simulations with a fixed step size where your processes don’t interact with
each other or with shared resources.

A short example simulating two clocks ticking in different time intervals looks
like this:

>>> import simpy
>>>
>>> def clock(env, name, tick):
...     while True:
...         print(name, env.now)
...         yield env.timeout(tick)
...
>>> env = simpy.Environment()
>>> env.process(clock(env, 'fast', 0.5))
<Process(clock) object at 0x...>
>>> env.process(clock(env, 'slow', 1))
<Process(clock) object at 0x...>
>>> env.run(until=2)
fast 0
slow 0
fast 0.5
slow 1
fast 1.0
fast 1.5

The documentation contains a :ref:`tutorial <intro>`, :ref:`several guides
<guides>` explaining key concepts, a number of :ref:`examples
<examples>` and the :ref:`API reference <api>`.

SimPy is released under the MIT License. Simulation model developers are
encouraged to share their SimPy modeling techniques with the SimPy community.
Please post a message to the `SimPy mailing list
<https://groups.google.com/forum/#!forum/python-simpy>`_.

There is an introductory talk that explains SimPy’s concepts and provides some
examples: `watch the video <https://www.youtube.com/watch?v=Bk91DoAEcjY>`_ or
`get the slides <http://stefan.sofa-rockers.org/downloads/simpy-ep14.pdf>`_.

SimPy has also been reimplemented in other programming languages. See the
:ref:`list of ports <ports>` for more details.
