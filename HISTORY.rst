=======
History
=======


0.7.0 (2020-04-18)
------------------

* Refactored the models to unify the ``Problem`` and ``Solution`` classes into the new ``StandardProblem`` class.
* 93% test coverage, including distance functions, parsing functions, and rendering functions.
* You can finally *write* problems in TSPLIB95 format! Render to text, write to file, or save to filepath.
* Parsing text, reading files, and loading filepaths are all now supported.
* Deprecated the old loading utils.
* Custom problems now supported by allowing you to define your own fields.
* Library exceptions for parsing and rendering.
* Numerous bugfixes for the distance functions (ATT, XRAY*, GEO).
* Improved the CLI to use a pager and proper column tabulation.
* Made some progress modernizing the FORTRAN code for xray problems.
* Added codecoverage metrics and badge.


0.6.1 (2020-01-04)
------------------

* Fix bug that caused the parser to ignore the first line of a file


0.6.0 (2019-10-19)
------------------

* Changes to the conversion into a ``networkx.Graph``:

    * Depot, demand, and fixed edge data have been removed from graph metadata.
      Depot and demand data is now associated with individual nodes like fixed edge
      data was (and still is).
    * Add a ``normalized`` parameter to allow nodes to be renamed as zero-index
      integers when obtaining a ``networkx.Graph``.

* Depots, demands, node coordinates, and display data fields now default to
  empty containers rather than ``None``.
* Fixed twine/PyPI warning about long description mime type


0.5.0 (2019-10-02)
------------------

* New loaders that take just the text - no file necessary!
* Invalid keywords now result in a ``ParsingError``
* Update the CLI to catch and gracefully handle ``ParsingError``
* Fixed a bug when trying to amend an exception with line information


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
