produce
=======

Replacement for Make geared towards processing data rather than compiling
code. Strives to be simple and user-friendly. Key feature: supports multiple
expansions in pattern rules.

produce is in an early stage of development. Current status: first working
prototype.

Dependencies
------------

* A Unix-like operating system such as Linux or Mac OS X. Cygwin under Windows
  may also work.
* Python 3 (!)

Installation
------------

Produce consists of a single executable Python script called "produce". Just
make sure it is in your PATH, e.g. by copying it to /usr/local/bin or by
linking to it from your $HOME/bin directory.

Usage
-----

When invoked, Produce will look for a file called produce.ini in the current
working directory. Its format is not documented yet, but there is an example
project in doc/samples/tokenization that should be enlightening.

Getting in touch
----------------

Produce is being developed by Kilian Evang <%{firstname}@%{lastname}.name>.
I would love to hear from you if you find it useful, if you have questions and
if there are any particular features that you would like added next.

