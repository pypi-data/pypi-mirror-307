v1.3.0
======

Features
--------

- Compatible for Flake8 from version ``flake8>=4``. (#4)


v1.2.2
======

Bugfixes
--------

- Pin to flake8<6 as it's incompatible. (#2)
- Remove reference to py.builtin in tests. (#2)
- Disabled the 'enabler' plugin when running tests. (#2)


v1.2.1
======

Bugfixes
--------

- Declare minimum flake8 as v5. (#1)


v1.2.0
======

Features
--------

- Adopted jaraco/skeleton for packaging.


v1.1.3
------

- Fixed compatibility with flake8 v5. Now requires flake8 v5 or later.
- More cleanup in the README.

v1.1.2
------

- Revived project and relocated to
  `coherent-oss <https://github.com/coherent-oss/pytest-flake8>`_.
- Refreshed project metadata.

1.1.1
-----

- Update classifiers to indicate older versions are no longer supported
- No longer use deprecated pytest constructs
- Bump requirements to more accurately indicate what is currently needed

1.1.0
-----

- Drop Python 2 support and dependency on py; from @erikkemperman
- Drop support for Python 3.5, 3.6
- Stop testing on Python versions prior to 3.7
- Add a `flake8-max-doc-length` option; from @rodrigomologni
- Fix some minor typos; from @kianmeng

1.0.7
-----

- Implement collect() for Flake8Item; from @thomascobb
- Document skipping behavior in README; from @jpyams

1.0.6
-----

- Fix compatibility with flake8 >= 3.8, from @marc

1.0.5
-----

- Fix deprecation warning; from @jonasundderwolf

1.0.4
-----

- Support flake8 3.7+ by checking existence of "app.make_notifier";
  from jirikuncar@github
- More fixes for Travis CI -- properly specify Python versions, in
  particular for pypy (and fix a typo)

1.0.3
-----

- Don't use long deprecated functions from pytest, broke with pytest 4.1.0
- Fix typo that caused some tests to not run as expected
- Run Travis CI tests against Python 3.7, and fix some issues with current tox

1.0.2
-----

- Test on Python 3.7
- Escape a regex string with r""

1.0.1
-----

- Correct junit XML output for pytest 3.5.x

1.0.0
-----

- Honor ignore settings in default flake8 config section; from
  brianbruggeman@github
- Improve junit XML output; from Struan Judd

0.9.1
-----

- Do continuous integration with Travis; from alex-dr@github
- Declare compatibility with Python 3.6

0.9
---

- Extend options already loaded instead of replacing them; from
  mforbes@github
- Correct some issues preventing proper operation with flake8 3.5.0;
  from jezdez@github
- Register pytest marker for flake8; from alex-dr@github

0.8.1
-----

0.8
---

- Allow running with no cacheprovider
- Modernize use of fixtures in tests

0.7
---

- Added new options "flake8-max-complexity", "flake8-show-source"
  and "flake8-statistics"

0.6
---

- Update for flake8 3.x

0.5
---

- Fix rendering of rST; from Ken Dreyer

0.4
---

- Really fix cache usage; had a comparison between tuple and
  list which always failed

0.3
---

- Use integrated pytest cache instead of separate pytest-cache
  module (which is now integrated)
- Use documented hooks for start and end of a test run

0.2
---

- Added ability to override maximum line length

0.1
---

- initial release
