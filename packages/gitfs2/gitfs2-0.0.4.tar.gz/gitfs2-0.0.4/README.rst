================================================================================
gitfs2
================================================================================

.. image:: https://api.travis-ci.org/moremoban/gitfs2.svg
   :target: http://travis-ci.org/moremoban/gitfs2

.. image:: https://codecov.io/github/moremoban/gitfs2/coverage.png
   :target: https://codecov.io/github/moremoban/gitfs2
.. image:: https://badge.fury.io/py/gitfs2.svg
   :target: https://pypi.org/project/gitfs2

.. image:: https://pepy.tech/badge/gitfs2/month
   :target: https://pepy.tech/project/gitfs2

.. image:: https://img.shields.io/github/stars/moremoban/gitfs2.svg?style=social&maxAge=3600&label=Star
    :target: https://github.com/moremoban/gitfs2/stargazers

.. image:: https://img.shields.io/static/v1?label=continuous%20templating&message=%E6%A8%A1%E7%89%88%E6%9B%B4%E6%96%B0&color=blue&style=flat-square
    :target: https://moban.readthedocs.io/en/latest/#at-scale-continous-templating-for-open-source-projects

.. image:: https://img.shields.io/static/v1?label=coding%20style&message=black&color=black&style=flat-square
    :target: https://github.com/psf/black

.. image:: https://dev.azure.com/moremoban/gitfs2/_apis/build/status/moremoban.gitfs2?branchName=master
   :target: https://dev.azure.com/moremoban/gitfs2/_build/latest?definitionId=2&branchName=master


It helps perform `file operations <https://docs.pyfilesystem.org/en/latest/guide.html>`_ over a git repository.
It clones the git repository and returns python file system 2's `OSFS <https://docs.pyfilesystem.org/en/latest/reference/osfs.html>`_ instance.

The idea originates from `moban <https://github.com/moremoban/moban>`_, which uses git repositories as
a vehicle to have versioned templates for the creation of a new python package. Surely, it can be implemented
in any other ways but moban v0.6.0 mandates python file system 2 interface. Hence this library is written.

Get a file inside a python package
--------------------------------------------------------------------------------

.. code-block:: python

    >>> import fs
    >>> git_fs = fs.open_fs("git://github.com/moremobans/pypi-mobans.git!/templates")
    >>> git_fs.readtext("_version.py.jj2")
    '__version__ = "0.0.4"\n__author__ = "C.W."\n'


Get from a different branch
--------------------------------------------------------------------------------

.. code-block:: python

    >>> import fs
    >>> git_fs = fs.open_fs("git://github.com/moremobans/pypi-mobans.git?branch=master!/templates")
    >>> git_fs.read("_version.py.jj2")
    '__version__ = "0.0.4"\n__author__ = "C.W."\n'


Checkout submodules recursively
--------------------------------------------------------------------------------

.. code-block:: python

    >>> git_fs = fs.open_fs("git://github.com/moremobans/pypi-mobans.git?branch=master&submodule=true!/templates")


Does it write?
--------------------------------------------------------------------------------

Yes locally, it will write as you can do so without using gitfs2. And no, it
does not help commit and push the changes for you.

Plus, the intention is never to write to a repository.

Primary use case
--------------------------------------------------------------------------------

You can do the following with moban:

.. code-block:: bash

    $ moban -t 'git://github.com/moremoban/pypi-mobans.git!/templates/_version.py.jj2' \
            -c 'git://github.com/moremoban/pypi-mobans.git!/config/data.yml' \
            -o _version.py
    Info: Found repo in /Users/jaska/Library/Caches/gitfs2/repos/pypi-mobans
    Templating git://github.com/moremoban/pypi-mobans.git!/templates/_version.py.jj2 to _version.py
    Templated 1 file.
    $ cat _version.py
    __version__ = "0.1.1rc3"
    __author__ = "C.W."



License
--------------------------------------------------------------------------------

MIT


Installation
================================================================================


You can install gitfs2 via pip:

.. code-block:: bash

    $ pip install gitfs2


or clone it and install it:

.. code-block:: bash

    $ git clone https://github.com/moremoban/gitfs2.git
    $ cd gitfs2
    $ python setup.py install
