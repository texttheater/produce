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

![example dependency chart for compiling a C program](img/compiling.png)

But build automation is also useful in other areas, such as science. For
example, in the [Groningen Meaning Bank](http://gmb.let.rug.nl/) project, a
Natural Language Processing pipeline is combined with corrections from human
experts to build a collection of texts with linguistic annotations in a
bootstraping fashion.

In the following simplified setup, processing starts with a text file
(`en.txt`) which is first part-of-speech-tagged (`en.pos`), then analyzed
syntactically (`en.syn`) by a parser and finally analyzed semantically
(`en.sem`). Each step is first carried out automatically by an NLP tool
(`*.auto`) but then corrections by human annotators (`*.corr`) are applied
to build the main version of the file which then serves as input to further
processing. Every time a new human correction is added, parts of the
pipeline must be re-run:

![example dependency chart for running an NLP pipeline](img/pipeline.png)

Or take running machine learning experiments: we have a collection of labeled
data, split into a training portion and testing portions. We have various
feature sets and want to know which one produces the best model. So we train a
separate model based on each feature set and on the training data, and generate
corresponding labeled outputs and evaluation reports based on the development
test data:

![example dependency chart for running machine learning experiments](img/ml.png)

A [number](http://kbroman.github.io/minimal_make/)
[of](http://bost.ocks.org/mike/make/) [articles](http://zmjones.com/make/)
point out that build automation is an invaluable help in setting up experiments
in a self-documenting manner, so that they can still be understood, replicated
and modified months or years later, by you, your colleagues or other
researchers. Many people use Make for this purpose, and so did I, for a while.
I specifically liked:

* *The declarative notation.* Every step of the workflow is expressed as a
  _rule_, listing the _target_, its direct dependencies and the command to run
  (the _recipe_). Together with a good file naming scheme, this almost
  eliminates the need for documentation.
* *The Unix philosophy.* Make is, at its core, a thin wrapper around shell
  scripts. For orchestrating the steps, you use Make, and for executing them,
  you use the full power of shell scripts. Each tool does one thing, and does
  it well. This reliance on shell scripts is something that sets Make apart
  from specialized build tools such as Ant or A-A-P.
* *The wide availability.* Make is installed by default on almost every Unix
  system, making it ideal for disseminating and exchanging code because the
  Makefile format is widely known and can be run everywhere.

So, if Make has so many advantages, why yet another build automation tool?
There are two reasons:

* Make’s syntax. Although the basic syntax is extremely simple, as soon as you
  want to go a _little bit_ beyond what it offers and use more advanced
  features, things get quite arcane very quickly.
* Wildcards are quite limited. If you want to match on the name of a specific
  target to generate its dependencies dynamically, you can only use one
  wildcard. If your names are a bit more complex than that, you have to resort
  to black magic like Make’s built-in string manipulation functions that don’t
  compare favorably to languages like Python or even Perl, or rely on external
  tools. In either case, your Makefiles become extremely hard to read, bugs
  slip in easily and the simplicity afforded by the declarative paradigm is
  largely lost.

Produce is thus designed as a tool that copies Make’s virtues and improves a
great deal on its deficiencies by using a still simple, but much more powerful
syntax for mapping targets to dependencies. Only the core functionality of Make
is mimicked – advanced functions of Make such as built-in rules specific to
compiling C programs are not covered. Produce is general-purpose.

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

When you run the `produce` command (usually followed by the targets you want
built), Produce will look for a file in the current directory, called
`produce.ini` by default. This is the “Producefile”. Let’s introduce
Producefile syntax by comparing it to Makefile syntax.

### The basics: rules, expansions and comments

Here is a Makefile for a tiny C project:

    # Compile
    %.o : %.c
    	cc -c $<
    
    # Link
    % : %.o
    	cc -o $@ $<

And here is the corresponding `produce.ini`:

    # Compile
    [%{name}.o]
    dep.c = %{name}.c
    recipe = cc -c %{c}
    
    # Link
    [%{name}]
    dep.o = %{name}.o
    recipe = cc -o %{target} %{o}

Easy enough, right? Produce syntax is a dialect of the widely known INI syntax,
consisting of sections with headings in square brackets, followed by
attribute-value pairs separated by `=`. In Produce’s case, sections represent
_rules_, the section headings are _targets_ to build, and the attribute-value
pairs specify the target’s direct dependencies and the recipe to run it.

Dependencies are typically listed each as one attribute of the form `dep.name`
where `name` stands for a name you give to the dependency – e.g., its file
type. This way, you can refer to it in the recipe using an _expansion_.

Expansions have the form `%{...}`. In the target, they are used as wildcards.
When the rule is invoked on a specific target, they match any string and assign
it to the variable name specified between the curly braces. In attribute
values, they are used like variables, expanding to the value associated with
the variable name. Besides target matching, values can also be assigned to
variable names by attribute-value pairs, as with e.g. `dep.c = %{name}.c`.
Here, `c` is the variable name; the `dep.` prefix just tells Produce that this
particular value is also a dependency.

Lines starting with `#` are for comments and ignored.

So far, so good – a readable syntax, I hope, but a bit more verbose than that
of Makefiles. What does this added verbosity buy us? We will see in the next
subsections.

### Named dependencies

To see why naming dependencies is a good idea, consider the following Makefile
rule:

    out/%.pos : out/%.pos.auto out/%.pos.corr
    	./src/scripts/apply_corrections $< \
            --corrections out/$*.pos.corr > $@

This could be from the Natural Language Processing project we saw as the second
example above: the rule is for making the final `pos` file from the
automatically generated `pos.auto` file and the `pos.corr` file with manual
corrections, thus it has two direct dependencies, specified on the first line.
The recipe refers to the first dependency using the shorthand `$<`, but there
is no such shorthand for other dependencies. So we have to type out the second
dependency again in the recipe, taking care to replace the wildcard `%` with
the magic variable `$*`. This is ugly because it violates the golden principle
“Don’t repeat yourself!” If we write something twice in a Makefile, not only is
it more work to type, but also if we want to change it later, we have to change
it in two places, and there’s a good chance we’ll forget that.

Produce’s named dependencies avoid this problem: once specified, you can refer
to every dependency using its name. Here is the Produce rule corresponding to
the above Makefile rule:

    [out/%{name}.pos]
    dep.auto = %{name}.pos.auto
    dep.corr = %{name}.pos.corr
    recipe = ./src/scripts/apply_corrections %{auto} %{corr} > %{target}

Note that you don’t _have_ to name dependencies. Sometimes you don’t need to
refer back to them. Here is an example rule that compiles a LaTeX document:

    [%{name}.pdf]
    deps = %{name}.tex bibliography.bib
    recipe =
    	pdflatex %{name}
    	bibtex %{name}
    	pdflatex %{name}
    	pdflatex %{name}

The TeX tools are smart enough to fill in the file name extension if we just
give them the basename that we got by matching the target. In such cases, it
can be more convenient not to name the dependencies and list them all on one
line. This is what the `deps` attribute is for. It is parsed using Python’s
[`shlex.split`](https://docs.python.org/3/library/shlex.html?highlight=shlex#shlex.split)
function – consult the Python documentation for escaping rules and such. You
can also mix `deps.*` attributes and `deps` in one rule.

Note that, as in many INI dialects, attribute values (here: the recipe) can
span multiple lines as long as each line after the first is indented. See
[Multiline attributes](#multiline-attributes) below for details.

### Multiple wildcards, regular expressions and matching conditions 

TODO

### Declarations vs. special attributes

TODO `type`

### Python expressions

TODO

Advanced `produce.ini` features
-------------------------------

### Multiline attributes

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
