=======
History
=======

0.4.0 (2019-09-21)
------------------

* All expected parsing errors are now raised as ``ParsingError`` rather than the base ``Exception`` type.
* Fix name of distance paramter to distances.geographical. Previously it was "diameter" but was used as a radius. It is now "radius".
* Relax restriction on networkx version (now ``~=2.1``)
* Add documentation for each problem field
* Other minor documentation changes
* Add offical 3.7 support
* Add missing history entry for v0.3.3
* Remove some dead code

0.3.3 (2019-03-24)
------------------

* Fix parsing bug for key-value lines whose value itself contains colons

0.3.2 (2018-10-07)
------------------

* Fix bug in ``Problem.is_complete`` that produced a ``TypeError`` when run
* Fix bug in ``Problem.is_depictable`` that produced a ``TypeError`` when run
* Fix bug in ``Problem.get_display`` that produced an ``AttributeError`` when run
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
