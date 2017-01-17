===================
Time and Scheduling
===================

The aim of this section is to give you a deeper understanding of how time
passes in SimPy and how it schedules and processes events.


What is time?
=============

*Time* itself is not easy to grasp.  The `wikipedians describe it
<https://en.wikipedia.org/wiki/Time>`_ this way:

      *«Time is the indefinite continued progress of existence and events that
      occur in apparently irreversible succession from the past through the
      present to the future.  Time is a component quantity of various
      measurements used to sequence events, to compare the duration of events
      or the intervals between them, and to quantify rates of change of
      quantities in material reality or in the conscious experience.  Time is
      often referred to as the fourth dimension, along with the three spatial
      dimensions.»*


What's the problem with it?
===========================

Often, events (in the real world) appear to happen "at the same time", when
they are in fact happening at slightly different times.  Here is an obvious
example: Alice and Bob have birthday on the same day.  If your time scale is in
days, both birthday events happen at the same time.  If you increase the
resolution of you clock, e.g. to minutes, you may realise that Alice was
actually born at 0:42 in the morning and Bob at 11:14 and that there's quite
a difference between the time of both events.

Doing simulation on computers suffers from similar problems.  Integers (`and
floats, too
<http://blog.reverberate.org/2014/09/what-every-computer-programmer-should.html>`_)
are discrete numbers with a lot of void in between them.  Thus, events that
would occur after each other in the real world (e.g., at *t*:sub:`1` = 0.1 and
*t*:sub:`2` = 0.2) might occur at the "same" time if mapped to an integer scale
(e.g., at *t* = 0).

On the other hand, SimPy is (like most simulation frameworks)
a single-threaded, deterministic library.  It processes events sequentially
– one after another.  If two events are scheduled at the same time, the one
that is scheduled first will also be the processed first (FIFO).

That is very important for you to understand.  The processes in your
modeled/simulated world may run "in parallel", but when the simulation runs on
your CPU, all events are processed sequentially and deterministically.  If you
run your simulation multiple times (and if you don't use :mod:`random` ;-)),
you will *always* get the same results.

So keep this in mind:

- In the real world, there's usually no *at the same time*.

- Discretization of the time scale can make events appear to be *at the same
  time*.

- SimPy processes events *one after another*, even if they have the *same
  time*.


SimPy Events and time
=====================

Before we continue, let's recap the states an event can be in (see
:doc:`events` for details):

- untriggered: not known to the event queue
- triggered: scheduled at a time *t* and inserted into the event queue
- processed: removed from the event queue

SimPy's event queue is implemented as a `heap queue
<https://docs.python.org/3/library/heapq.html>`_: "Heaps are binary trees for
which every parent node has a value less than or equal to any of its children."
So if we insert events as tuples *(t, event)* (with *t* being the scheduled
time) into it, the first element in the queue will by definition always be the
one with the smallest *t* and the next one to be processed.

However, storing *(t, event)* tuples will not work if two events are scheduled
at the same time because events are not comparable.  To fix this, we also store
a strictly increasing event ID with them: *(t, eid, event)*.  That way, if two
events get scheduled for the same time, the one scheduled first will always be
processed first.


.. Remove determinism by "jittering" timeouts
.. ==========================================
..
.. .. TODO:
.. A relatively easy way to remove the determinism from your simulation is to
.. add "jitter" to
