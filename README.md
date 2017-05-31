# dsk.greeting

## Greeting form

* `Source code @ GitHub <https://github.com/besja/dsk.greeting>`_
* `Releases @ PyPI <http://pypi.python.org/pypi/dsk.greeting>`_
* `Documentation @ ReadTheDocs <http://dskgreeting.readthedocs.org>`_
* `Continuous Integration @ Travis-CI <http://travis-ci.org/besja/dsk.greeting>`_

## How it works

This package provides a Plone addon as an installable Python egg package.

The generated Python package holds an example content type `ContentPage` which
provides a folderish version of the default **Page** document type.

The implementation is kept simple on purpose and asumes that the developer will
add further content manually.


## Installation

To install `dsk.greeting` you simply add ``dsk.greeting``
to the list of eggs in your buildout, run buildout and restart Plone.
Then, install `dsk.greeting` using the Add-ons control panel.
