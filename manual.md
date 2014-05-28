Produce Manual
==============

Introduction
------------

Produce is a build automation tool. Build automation is useful whenever you
have one or several input files from which one or several output files are
generated automatically – possibly in multiple steps, so that you have
intermediate files.

The classic case for this is compiling C programs, where a simple project might
look like this:

TODO image

But build automation is also useful in other areas, such as science. For
example, in the [Groningen Meaning Bank](http://gmb.let.rug.nl/) project, a
Natural Language Processing pipeline is combined with corrections from human
experts to iteratively build a collection of texts with linguistic annotations.
Every time one of the tools in the pipeline is updated or a new human
correction is added, parts of the pipeline need to be re-run:

TODO image

Or take running machine learning experiments: we have a collection of labeled
data, split into a training portion and testing portions. We have various
feature sets and want to know which one produces the best model. So we train a
separate model based on each feature set and on the training data, and generate
corresponding labeled outputs and evaluation reports based on the development
test data:

TODO image

A number of articles (TODO links) point out that build automation is an
invaluable help in setting up experiments in a self-documenting manner, so that
they can still be understood, replicated and modified months or years later,
by you, your colleagues or other researchers. Many people use Make for this
purpose, and so did I, for a while. I specifically liked:

* The declarative notation. Every step of the workflow is expressed as a rule,
  listing the target, its direct dependencies and the command to run (the
  “recipe”). Together with a good file naming scheme, this almost eliminates
  the need for documentation.
* The Unix philosophy. Make is, at its core, a thin wrapper around shell
  scripts. Make orchestrates the steps, and shell scripts execute them, using
  their full power. Each tool does one thing, and does it well. This reliance
  on shell scripts is something that sets Make apart from more purpose-built
  build tools such as Ant or A-A-P.
* The wide availability. Make is installed by default on almost every Unix
  system, making it ideal for disseminating and exchanging code because the
  Makefile format is widely known and can be run everywhere.

So, if Make has so many advantages, why yet another build automation tool?
There are two reasons:

* Make’s syntax. Although the basic syntax is extremely simple, as soon as you
  want to go a _little bit_ beyond what it offers and use more advanced
  features, things get quite arcane very quickly.
* Wildcards are quite limited. If you want to match on the name of a specific
  target to generate its dependencies dynamically, you can only use one
  wildcard – if your names are a bit more complex than that, you have to resort
  to black magic like Make’s built-in string manipulation functions that don’t
  compare favorably to languages like Python or even Perl, or rely on external
  tools. In either case, your Makefiles become extremely hard to read, bugs
  slip in easily and the simplicity afforded by the declarative paradigm is
  largely lost.

Produce is thus designed as a tool that copies Make’s virtues and improves a
great deal on its deficiencies by using a still simple, but much more powerful
syntax for mapping targets to dependencies. Only the core of Make is mimicked –
advanced functions of Make such as built-in rules specific to compiling C
programs are not covered. Produce is general-purpose.

Build automation: basic requirements
------------------------------------

Let’s review the basic functionality we expect of a build automation tool:

* Allows you to run multiple steps of a workflow with a single command, in the
  right order.
* Notices when inputs have changed and runs exactly those steps again that are
  needed to bring the outputs up to speed, no more or less.
* Intermediate files can be deleted without affecting up-to-dateness – if the
  outputs are newer than the inputs, the workflow will not be re-run.

Make syntax vs. Produce syntax
------------------------------

When you run the `produce` command, Produce will look for a file in the current
directory, called `produce.ini` by default. This is the “Producefile”. Let’s
introduce Producefile syntax by comparing it with Makefile syntax.

### Rules and expansions

Here is a Makefile for the tiny C project depicted above:

TODO

And here is the corresponding `produce.ini`:

TODO

Easy enough, right? Produce syntax is a dialect of the widely known INI syntax,
consisting of sections with headings in square brackets, followed by
attribute-value pairs separated by `=`. In Produce’s case, the section headings
are targets to build, and the attribute-value pairs specify the target’s direct
dependencies and the recipe to run it.

Dependencies are typically listed each under one attribute of the form
`dep.name` where `name` stands for a name you give to the dependency – e.g.,
its file type. This way, you can refer to it in the recipe.

Expansions have the form `%{...}`. In the target, they are used as wildcards,
matching any string and assigning it the name specified between the curly
braces. In attribute values, they are used like variables, expanding to the
value associated with the name – no matter whether this name was assigned by
matching on the target or by an attribute-value-specification.

So far, so good – a readable syntax, I hope, but a bit more verbose than that
of Makefiles. What does this added verbosity buy us? We will see in the next
subsections.

### Named dependencies

TODO

Note that, as in many INI dialects, attribute values (here: the recipe) can
span multiple lines as long as each subsequent line is indented. See
[Multiline attributes](#Multiline_attributes) below for details.

### Multiple wildcards, regular expressions and matching conditions 

TODO

### Declarations vs. special attributes

TODO `type`

### Python expressions

TODO

Advanced `produce.ini` features
-------------------------------

### <a name="Multiline_attributes">Multiline attributes</a>

TODO

### `shell`: choosing the recipe interpreter

TODO

### The “global” section

TODO

### All special attributes at a glance

TODO

Running Produce
---------------

TODO

Internals
---------

### The build algorithm

TODO

Support
-------

TODO
