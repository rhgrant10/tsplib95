=======
History
=======

0.3.2 (2018-10-07)
------------------

* Fix bug in ``Problem.is_complete`` that produced a ``TypeError`` when run
* Fix bug in ``Problem.is_depictable`` that produced a ``TypeError`` when run
* Fix bug in ``Problem.get_display`` that produced an ``AttributeError`` when
  run
* Added some unit tests for the ``Problem`` class
* Added some unit tests for the ``parser`` module

0.3.1 (2018-10-03)
------------------

* Fix bug in ``Problem.is_weighted`` that caused problems with defined nodes
  coords to use the unit distance function

0.3.0 (2018-08-12)
------------------

* Added XRAY1 and XRAY2 implementations
* Simplified some of the matrix code

0.2.0 (2018-08-12)
------------------

* Implement column-wise matrices
* Add a utiltiy for loading an unknown file
* Fix bug in the ATT distance function
* Update the CLI to use the models
* Document a bunch-o-stuff
* Switch to RTD sphinx theme
* Move most utilties into utils

0.1.0 (2018-08-12)
------------------

* First release on PyPI.
