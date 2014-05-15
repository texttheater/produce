produce
=======

Produce is an incremental build system for the command line, like make or redo.
It strives to be simple and user-friendly. It is less geared towards compiling
code, and more towards processing data and running sets of machine learning
experiments. Specifically, it works well with filenames that have not just one
but many variable parts, e.g. to indicate experimental parameters.

Produce recently graduated from first working prototype to "dogfood": the
developer is using it daily in his main project.

Dependencies
------------

* A Unix-like operating system such as Linux or Mac OS X. Cygwin under Windows
  may also work.
* Python 3

Installation
------------

Produce consists of a single executable Python script called "produce". Just
make sure it is in your PATH, e.g. by copying it to /usr/local/bin or by
linking to it from your $HOME/bin directory.

Usage
-----

When invoked, Produce will look for a file called produce.ini in the current
working directory. Its format is not documented yet, but there is 
[an example project](https://github.com/texttheater/produce/tree/master/doc/samples/tokenization)
that should be enlightening.

Also have a look at the
[PyGrunn 2014 slides](https://texttheater.github.io/produce-pygrunn2014).

Getting in touch
----------------

Produce is being developed by Kilian Evang <%{firstname}@%{lastname}.name>.
I would love to hear from you if you find it useful, if you have questions and
if there are any particular features that you would like added next.

