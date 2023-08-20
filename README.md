![Produce logo](https://raw.githubusercontent.com/texttheater/produce/master/img/logo/Produce_Logo_300.png)
==============================================

Produce is an incremental build system for the command line, like Make or redo,
but different: it is scriptable in Python and it supports multiple variable
parts in file names. This makes it ideal for doing things beyond compiling
code, like setting up replicable scientific experiments.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents** 

- [Requirements](#requirements)
- [Installing Produce](#installing-produce)
- [Usage](#usage)
- [Motivation](#motivation)
- [Build automation: basic requirements](#build-automation-basic-requirements)
- [Make syntax vs. Produce syntax and a tour of the basic features](#make-syntax-vs-produce-syntax-and-a-tour-of-the-basic-features)
  - [Rules, expansions, escaping and comments](#rules-expansions-escaping-and-comments)
  - [Named and unnamed dependencies](#named-and-unnamed-dependencies)
  - [Multiple wildcards, regular expressions and matching conditions](#multiple-wildcards-regular-expressions-and-matching-conditions)
  - [Special targets vs. special attributes](#special-targets-vs-special-attributes)
  - [Python expressions and global variables](#python-expressions-and-global-variables)
- [Running Produce](#running-produce)
  - [Status and debugging messages](#status-and-debugging-messages)
  - [Error handling and aborting](#error-handling-and-aborting)
  - [How targets are matched against rules](#how-targets-are-matched-against-rules)
- [Advanced usage](#advanced-usage)
  - [Whitespace and indentation in values](#whitespace-and-indentation-in-values)
  - [The prelude](#the-prelude)
  - [`shell`: choosing the recipe interpreter](#shell-choosing-the-recipe-interpreter)
  - [Running jobs in parallel](#running-jobs-in-parallel)
  - [Dependency files](#dependency-files)
  - [Rules with multiple outputs](#rules-with-multiple-outputs)
    - [“Sideways” dependencies](#sideways-dependencies)
  - [Producing the outputs for all inputs](#producing-the-outputs-for-all-inputs)
- [All special attributes at a glance](#all-special-attributes-at-a-glance)
  - [In rules](#in-rules)
  - [In the global section](#in-the-global-section)
- [Getting in touch](#getting-in-touch)
- [Acknowledgments](#acknowledgments)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Requirements
------------

* A Unix-like operating system such as Linux or Mac OS X. Windows Subsystem for
  Linux may also work.
* Python 3.6 or higher
* Git (for downloading Produce)

Installing Produce
------------------

Install the latest release using pip:

    pip3 install produce

Or get the development version by running the following command in a convenient
location:

    git clone https://github.com/texttheater/produce

This will create a directory called `produce`. To update to the latest version
of Produce later, you can just go into that directory and run:

    git pull

The `produce` directory contains an executable Python script also called
`produce`. This is all you need to run Produce. Just make sure it is in your
`PATH`, e.g. by copying it to `/usr/local/bin` or by linking to it from your
`$HOME/bin` directory.

Usage
-----

When invoked, Produce will first look for a file called `produce.ini` in the
current working directory. Its format is documented in this document. If you
want a quick start, have a look at
[an example project](https://github.com/texttheater/produce/tree/master/doc/samples/tokenization).

You may also have a look at the
[PyGrunn 2014 slides](https://texttheater.github.io/produce-pygrunn2014)
for a quick introduction.

Motivation
----------

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

* *Make’s syntax.* Although the basic syntax is extremely simple, as soon as
  you want to go a _little bit_ beyond what it offers and use more advanced
  features, things get quite arcane very quickly.
* *Wildcards are quite limited.* If you want to match on the name of a specific
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

Produce is written in Python 3 and scriptable in Python 3. Whenever I write
Python below, I mean Python 3.

Build automation: basic requirements
------------------------------------

Let’s review the basic functionality we expect of a build automation tool:

* Allows you to run multiple steps of a workflow with a single command, in the
  right order.
* Notices when inputs have changed and runs exactly those steps again that are
  needed to bring the outputs up to speed, no more or less.

In addition, some build automation tools satisfy the following requirement
(Produce currently doesn’t):

* Intermediate files can be deleted without affecting up-to-dateness – if the
  outputs are newer than the inputs, the workflow will not be re-run.

Make syntax vs. Produce syntax and a tour of the basic features
---------------------------------------------------------------

When you run the `produce` command (usually followed by the targets you want
built), Produce will look for a file in the current directory, called
`produce.ini` by default. This is the “Producefile”. Let’s introduce
Producefile syntax by comparing it to Makefile syntax.

### Rules, expansions, escaping and comments

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
_rules_, the section headings are _target patterns_ matching _targets_ to
build, and the attribute-value pairs specify the target’s direct dependencies
and the recipe to run it.

Dependencies are typically listed each as one attribute of the form `dep.name`
where `name` stands for a name you give to the dependency – e.g., its file
type. This way, you can refer to it in the recipe using an _expansion_.

Expansions have the form `%{...}`. In the target pattern, they are used as
wildcards. When the rule is invoked on a specific target, they match any string
and assign it to the variable name specified between the curly braces. In
attribute values, they are used like variables, expanding to the value
associated with the variable name. Besides target matching, values can also be
assigned to variable names by attribute-value pairs, as with e.g.
`dep.c = %{name}.c`. Here, `c` is the variable name; the `dep.` prefix just
tells Produce that this particular value is also a dependency.

If you need a literal percent sign in some attribute value, you need to escape
it as `%%`.

The `target` variable is automatically available when the rule is invoked,
containing the target matched by the target pattern.

Lines starting with `#` are for comments and ignored.

So far, so good – a readable syntax, I hope, but a bit more verbose than that
of Makefiles. What does this added verbosity buy us? We will see in the next
subsections.

### Named and unnamed dependencies

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
can also mix `dep.*` attributes and `deps` in one rule.

Note that, as in many INI dialects, attribute values (here: the recipe) can
span multiple lines as long as each line after the first is indented. See
[Whitespace and indentation in values](#whitespace-and-indentation-in-values)
below for details.

Note also that dependency lists can also be generated dynamically – see the
section on [dependency files](#dependency-files) below.

### Multiple wildcards, regular expressions and matching conditions

The ability to use more than one wildcard in target patterns is Produce’s
killer feature because not many other build automations tools offer it.
The only one I know of so far is [plmake](https://github.com/cmungall/plmake).
Rake and others do offer full regular expressions which are strictly more
powerful but not as easy to read. Don’t worry, Produce supports them too and
more, we will come to that. But first consider the following Produce rule,
which might stem from the third example project we saw in the introduction,
the machine learning one:

    [out/%{corpus}.%{portion}.%{fset}.labeled]
    dep.model = out/%{corpus}.train.%{fset}.model
    dep.input = out/%{corpus}.%{portion}.feat
    recipe = wapiti label -m %{model} %{input} > %{target}

Labeled output files here follow a certain naming convention: four parts,
separated by periods. The first one specifies the data collection (e.g. a
linguistic corpus), the second one the portion of the data that is
automatically labeled in this step (either the development portion or the test
portion), the third one specifies the feature set used and the fourth one is
the extension `labeled`. For each of the three first parts, we use a wildcard
to match it. We can then freely use these three wildcards to specify the
dependencies: the model we use for labelling depends on the corpus and on the
feature set but not on the portion to label: the portion used for training the
model is always the training portion. The input to labelling is a file
containing the data portion to label, together with the extracted features. We
assume that this file always contains all features we can extract even if we’re
not going to use them in a particular model, so this dependency does not depend
on the feature set.

A Makefile rule to achieve something similar would look something like this:

    .SECONDEXPANSION:
    out/%.labeled : out/$$(subst test,train,$$(subst dev,train,$$*)).model \
                    out/$$(basename $$*).feat
            wapiti label -m $< out/$(basename $*).feat > $@

If you are like me, this is orders of magnitude less readable than the Produce
version. Getting a Makefile rule like this to function properly will certainly
make you feel smart, but hopefully also feel miserable about the brain cycles
wasted getting your head around the bizarre syntax, the double dollars and the
second expansion.

A wildcard will match _anything_. If you need more control about which targets
are matched, you can use a
[Python regular expression](https://docs.python.org/3/library/re.html?highlight=re#module-re)
between slashes as the target pattern. For example, if we want to make sure
that our rule only matches targets where the second part of the filename is
either `dev` or `test`, we could do it like this:

    [/out/(?P<corpus>.*)\.(?P<portion>dev|test)\.(?P<fset>.*)\.labeled/]
    dep.model = out/%{corpus}.train.%{fset}.model
    dep.input = out/%{corpus}.%{portion}.feat
    recipe = wapiti label -m %{model} %{input} > %{target}

The regular expression in this rule’s header is almost precisely what the above
header with three wildcards is translated to by Produce internally, with the
difference that the subexpression matching the second part is now `dev|test`
rather than `.*`. We are using a little-known feature of regular expressions
here, namely the `(?P<...>)` syntax that allows us to assign names to
subexpressions by which you can refer to the matched part later.

Note the slashes at the beginning and end are just a signal to Produce to
interpret what is in-between as a regular expressions. You do not have to
escape slashes within your regular expression.

While regular expressions are powerful, they make your Producefile less
readable. A better way to write the above rule is by sticking to ordinary
wildcards and using a separate _matching condition_ to check for `dev|test`:

    [out/%{corpus}.%{portion}.%{fset}.labeled]
    cond = %{portion in ('dev', 'test')}
    dep.model = out/%{corpus}.train.%{fset}.model
    dep.input = out/%{corpus}.%{portion}.feat
    recipe = wapiti label -m %{model} %{input} > %{target}

A matching condition is specified as the `cond` attribute. We can use any
Python expression. It is evaluated only if the target pattern matches the
requested target. If it evaluates to a “truthy” value, the rule matches and
the recipe is executed. If it evaluates to a “falsy” value, the rule does
not match, and Produce moves on, trying to match the next rule in the
Producefile.

Note that the Python expression is given as an expansion. At this point we
should explain a few fine points:

1. Whenever we used expansions so far, the variable names inside were actually
   Python expressions, albeit of a simple kind: single variable names. But as
   we see now, we can use arbitrary Python expressions. Expansions used as
   wildcards in the target pattern are an exception, of course: they can only
   consist of a single variable name.
2. The variables we use in rules are actually Python variables.
3. Attribute values are always strings, so if a Python expression is used to
   generate (part of) an attribute value, not the value of the expression
   itself is used but whatever its `__str__` method returns. Thus, in the
   above rule, the value of the `cond` variable is not `True` or `False`, but
   `'True'` or `'False'`. In order to interpret the value as a Boolean, Produce
   calls
   [ast.literal\_eval](https://docs.python.org/3/library/ast.html?highlight=literal_eval#ast.literal_eval)
   on the string. So if the string contains anything other than a literal
   Python expression, this is an error.

As an exception to what we said about `__str__`, if an expansion evaluates to
something that is not a string but has an `__iter__` method, it will be treated
as a sequence and rendered as a white-space separated list, the elements
properly shell-quoted and escaped. Note also that parentheses are automatically
added around an expansion so it is very convenient to use generator expressions
for expansions. All of this is illustrated in the following rule:

    [Whole.txt]
    deps = %{'Part {}.txt'.format(i) for i in range(4)}
    recipe = cat %{deps} > %{target}

### Special targets vs. special attributes

Besides not naming all dependencies, there is another reason why Make’s syntax
is too simple for its own good. When some rule needs to have a special
property, Make usually requires a “special target” that syntactically looks
like a target but is actually a declaration and has no obvious visual
connection to the rule(s) it applies to. We have already seen an example of the
dreaded `.SECONDEXPANSION`. Another common special target is `.PHONY`, marking
targets that are just jobs to be run, without producing an output file. For
example:

    .PHONY: clean
    clean:
    	rm *.o temp

It would be easier and more logical if the “phoniness” was declared as part of
the rule rather than some external declaration. This is was Produce does. The
Produce equivalent of declaring targets phony is to set the `type` attribute of
their rule to `task` (the default is `file`). With this the rule above is
written as follows:

    [vacuum]
    type = task
    recipe = rm *.o temp

Note that since it is ungrammatical to “produce a clean”, I invented a naming
convention according to which the task that cleans up your project directory is
called `vacuum` because it produces a vacuum. It’s silly, I know.

For other special attributes besides `task`, see [All special attributes at a
glance](#all-special-attributes-at-a-glance) below.

### Python expressions and global variables

As we have already seen, Produce’s expansions can contain arbitrary Python
expressions. This is not only useful for specifying Boolean matching
conditions, but also for string manipulation, in particular for playing with
dependencies. This is a pain in Make, because Make implements its own string
manipulation language which from today’s perspective (since we have Python)
not only reinvents the wheel, but reinvents it poorly, with a rather dangerous
syntax. Consider the following (contrived) example from the GNU Make manual
where you have a list of dependencies in a global variable and filter them to
retain only those ending in `.c` or `.s`:

    sources := foo.c bar.c baz.s ugh.h
    foo: $(sources)
    	cc $(filter %.c %.s,$(sources)) -o foo

With Produce, we can just hand the string manipulation to Python, a language
we already know and (hopefully) like:

    []
    sources = foo.c bar.c baz.s ugh.h

    [foo]
    deps = %{sources}
    recipe = cc %{f for f in sources.split() \
    		if f.endswith('.c') or f.endswith('.s')}

This example also introduces the _global section_, a section headed by `[]`,
thus named with the empty string. The attributes here define global variables
accessible from all rules. The global section may only appear once and only at
the beginning of a Producefile.

Running Produce
---------------

Produce is invoked from the command line by the command `produce`, usually
followed by the target(s) to produce. These can be omitted if the Producefile
specifies one or more default targets. By default, Produce will look for
`produce.ini` in the current working directory and complain if it does not
exist.

A number of options can be used to control Produce’s behavior, as listed in its
help message:

usage: produce [-h] [-B | -b] [-d] [-f FILE] [-j JOBS] [-n] [-u PATTERN]
               [target ...]

positional arguments:
  target                The target(s) to produce - if omitted, default target
                        from Producefile is used

options:
  -h, --help            show this help message and exit
  -B, --always-build    Unconditionally build all specified targets and their
                        dependencies
  -b, --always-build-specified
                        Unconditionally build all specified targets, but treat
                        their dependencies normally (only build if out of
                        date)
  -d, --debug           Print debugging information. Give this option multiple
                        times for more information.
  -f FILE, --file FILE  Use FILE as a Producefile
  -j JOBS, --jobs JOBS  Specifies the number of jobs (recipes) to run
                        simultaneously
  -n, --dry-run         Print status messages, but do not run recipes
  -u PATTERN, --pretend-up-to-date PATTERN
                        Do not rebuild targets matching PATTERN or their
                        dependencies (unless the latter are also depended on
                        by other targets) even if out of date, but make sure
                        that future invocations of Produce will still treat
                        them as out of date by increasing the modification
                        times of their changed dependencies as necessary.
                        PATTERN can be a Produce pattern or a regular
                        expression enclosed in forward slashes, as in rules.

### Status and debugging messages

When it starts (re)building a target, Produce will tell you so with a status
message in green where the target is indented according to how deep in the
dependency graph it is. On successful completion of a target, a similar message
with `complete` is printed. If an error occurs while a target is being built,
Produce instead prints an `incomplete` message in red. The latter indicates
controlled shutdown: the recipe has been killed and incomplete outputs have
been renamed (see below). If you see a `(re)building` message but no
`(in)complete` message for some target, something went really wrong – this
should never happen. In that case, better check for yourself if any incomplete
outputs are still hanging around.

Giving the `-d`/`--debug` option one, two or three times will cause Produce to
additionally flood your terminal with a few, some more or lots of messages that
may be helpful for debugging.

### Error handling and aborting

When a recipe fails, i.e. its interpreter returns an exit status other than 0,
the corresponding target file (if any) may already have been created or
touched, potentially leading the next invocation of Produce to believe that it
is up to date, even though it probably doesn’t have the correct contents. Such
inconsistencies can lead to users tearing their hair out. In order to avoid
this, Produce will, when a recipe fails, make sure that the target file does
not stay there. It could just delete it, but that might be unwise because the
user might want to inspect the output file of the erroneous recipe for
debugging. So, Produce renames the target file by appending a `~` to the
filename (a common naming convention for short-lived “backups”).

If multiple recipes are running in parallel and one fails, Produce will kill
all of them, do the renaming and abort immediately.

The same is true if Produce receives an interrupt signal. So you can safely
abort a production process in your terminal by pressing `Ctrl+C`.

### How targets are matched against rules

When producing a target, either because asked to by the user or because the
target is required by another one, Produce will always work through the
Producefile from top to bottom and use the first rule that matches the target.
A rule matches a target if both the target pattern matches and the matching
condition (if any) subsequently evaluates to true.

Note that unlike most INI dialects, Produce allows for multiple sections with
the same heading. It makes sense to have the same target pattern multiple times
when there are matching conditions to make subdistinctions.

If no rule matches a target, Produce aborts with an error message.

Advanced usage
--------------

### Whitespace and indentation in values

An attribute value can span multiple lines as long as each line after the first
is indented with some whitespace. The recommended indentation is either one tab
or four spaces. If you make use of this, it is recommended to leave the first
line (after the attribute name and the `=`) blank so all lines of the value are
consistently aligned.

The _second_ line of a value (i.e. the first indented one) determines the kind
and amount of whitespace expected to start each subsequent line. This
whitespace will _not_ be part of the attribute value. _Additional_ whitespace
after the initial amount is, however, preserved. This is important e.g. for
Python code and the reason why Produce is no longer using Python’s
`configparser` module.

All whitespace at the very beginning and at the very end of an attribute value
will be stripped away.

For example, in the following rule, the recipe spans two lines:

    [paper.pdf]
    dep.tex = paper.tex
    dep.bib = paper.bib
    recipe =
        pdflatex paper
        pdflatex paper

### The prelude

If you use Python expressions in your recipes, you will often need to import
Python modules or define functions to use in these expressions. You can do this
by putting the imports, function definitions and other Python code into the
special `prelude` attribute in the [global
section](#python-expressions-and-global-variables). For example, put this at
the beginning of your Producefile to import the `errno`, `glob` and `os`
modules and define a helper function for creating directories.

    []
    prelude =
        import errno
        import glob
        import os

        def makedirs(path):
            try:
                os.makedirs(path)
            except OSError, error:
                if error.errno != errno.EEXIST:
                    raise error

### `shell`: choosing the recipe interpreter

By default, recipes are (after doing expansions) handed to the `bash` command
for execution. If you would rather write your recipe in `zsh`, `perl`, `python`
or any other language, that’s no problem. Just specify the interpreter in the
`shell` attribute of the rule.

### Running jobs in parallel

Use the `-j JOBS` command line option to specify the number of jobs Produce
runs in parallel. By default, Produce reserves one job slot for each recipe.
For recipes that run multiple parallel jobs themselves, it is recommended to
specify the number of jobs via the `jobs` attribute. Produce will then reserve
that many job slots for this recipe (but no more than `JOBS`).

Here is an example where the target `b` is created by a recipe that runs in
parallel:

    [a]
    deps = b c d
    recipe = touch %{target}

    [b]
    dep.input = input.txt
    dep.my_script = ./my_script.sh
    jobs = 8
    recipe = parallel --gnu -n %{jobs} -k %{my_script} %{input} > %{target}

    [c]
    dep.my_script = ./my_script.sh
    recipe = %{my_script} c > %{target}

    [d]
    dep.my_script = ./my_script.sh
    recipe = %{my_script} d > %{target}

Running `produce -j 8 a` will run up to 8 jobs in parallel. In this example,
the recipes for `c` and `d` may run in parallel. The recipe for `b` will not
run in parallel with any other recipe because it uses all 8 job slots.

### Dependency files

Sometimes the question which other files a file depends on is more complex and
may change frequently over the lifetime of a project, e.g. in the cases of
source files that import other header files, modules etc. In such cases, it
would be nice to have the dependencies automatically listed by a script.
Produce supports this via the `depfile` attribute in rules: here, you can
specify the name of a _dependency file_, a text file that contains
dependencies, one per line. Produce will read them and add them to the list of
dependencies for the matched target. Also, Produce will try to produce the
dependency file (i.e. make it up to date) _prior_ to reading it. So you can
write another rule that tells Produce how to generate each dependency file, and
the rest is automatic.

For example, the following rule might be used to generate a dependency file
listing the source file and header files required for compiling a C object.
This example uses `.d` as the extension for dependency files. It runs `cc -MM`
to use the C compiler’s dependency discovery feature and then some shell magic
to convert the output from a Makefile rule into a simple dependency list:

    [%{name}.d]
    dep.c = %{name}.c
    recipe =
        cc -MM -I. %{name} | sed -e 's/.*: //' | sed -e 's/^ *//' | \
        perl -pe 's/ (\\\n)?/\n/g' > %{target}

The following rule could then be used to create the actual object file. The
`depfile` attribute makes sure that whenever an included header file changes,
the object file will be rebuilt:

    [%{name}.o]
    dep.src = %{name}.c
    depfile = %{name}.d
    recipe =
        cc -c -o %{target} %{src}

Note that the `.c` file will end up in the dependency list twice, once from
`dep.src` and once from the dependency file. This does not matter, Produce is
smart enough not to do the same thing twice.

Warning: dependency files are made up to date even in dry-run mode!

### Rules with multiple outputs

Sometimes you have a command that creates multiple files at once because their
creation is inherently linked to the same process – it wouldn’t make sense to
try and create them in neatly separated steps. Splitting a file up into
multiple chunks is such a case:

    split -n 4 data.txt

This command creates four files called `xaa`, `xab`, `xac` and `xad`. It gets
complicated when these output files individually are dependencies of further
targets, as in this example:

    [split_and_zip]
    type = task
    deps = xaa.zip xab.zip xac.zip xad.zip

    [%{name}.zip]
    dep.file = %{name}
    recipe = zip %{target} %{file}

    [%{chunk}]
    dep.txt = data.txt
    recipe = split -n 4 %{txt}

If we run the task `split_and_zip`, it will try to create its (indirect)
dependencies `xaa`, `xab`, `xac` and `xad` independently of each other. Each
time, the last rule will match, and each time, the exact same recipe will be
executed. This is unncecessary work, one time would be sufficient because it
creates all four files in each case. Worse, if we run Produce in parallel,
multiple instances of the recipe may run in parallel and corrupt the data.

The solution is to explicitly declare which files a rule produces, other than
the target. The `outputs` attribute serves this purpose. With it, the last rule
is rewritten as follows:

    [%{chunk}]
    outputs = xaa xab xac xad
    dep.txt = data.txt
    recipe = split -n 4 %{txt}

Additionally, it is good style to add a matching condition to prevent that the
rule accidentally matches something that is not its output:

    [%{chunk}]
    outputs = xaa xab xac xad
    cond = %{target in outputs.split()}
    dep.txt = data.txt
    recipe = split -n 4 %{txt}

Instead of a single `outputs` attribute, separate attributes with the `out.`
prefix can be used, and both styles can also be mixed, similar to
`dep.`/`deps`. Here is an example of a rule using the `out.` style to declare
that while producing a `.pdf` file it will also produce an `.aux` file:

    [%{name}.pdf]
    dep.tex = %{name}.tex
    out.aux = %{name}.aux
    recipe =
        pdflatex %{tex}

#### “Sideways” dependencies

Suppose there is a target A that has some additional output file B. What if a
target C wants to declare a dependency on B? For this to work, there must be a
rule matching B. B, of course, is produced when A is produced. So, effectively,
in order to produce B, A must be produced. We can express this as a dependency:
B depends on A. You can write a rule that will tell Produce to produce A when B
is requested:

    [B]
    dep.a = A

(TODO: What if A is up to date but B does not exist?)

Such a rule only serves to “guide” Produce from B to A. It cannot contain its
own recipe. This would not make the sense as it is the rule for A that creates
B. If you included a recipe, Produce would complain about a cyclic dependency.

Here is a more concrete example: the rule for `paper.pdf` produces an
additional output `paper.aux`. Another rule, for `paper.info`, depends on
`paper.aux`. In order for Produce to be able to satisfy this dependency,
`paper.aux` is declared as depending on `paper.pdf`.

    [paper.info]
    dep.aux = paper.aux
    recipe = cat %{aux} | ./my_tool > %{target}

    [paper.aux]
    dep.pdf = paper.pdf

    [paper.pdf]
    dep.tex = paper.tex
    outputs = paper.aux
    recipe =
        pdflatex paper

There is one final problem here: after running the recipe for `paper.pdf`, the
modification time of `paper.pdf` may well be greater than that of `paper.aux`.
Since we declared `paper.aux` dependent on `paper.pdf`, this means that
`paper.aux` appears as out of date to Produce even though we just produced it.
A simple and effective way to prevent this is to include `touch %{outputs}` as 
the last line of any rule with multiple outputs. The last rule above thus
becomes:

    [paper.pdf]
    dep.tex = paper.tex
    outputs = paper.aux
    recipe =
        pdflatex paper
        touch %{outputs}

### Producing the outputs for all inputs

Suppose you have a number of input files (say `inputs/input001.txt` to
`inputs/input100.txt`). Each input can be processed to yield an output file
(say `models/model001` to `models/model100`) – for example, by the following
rule:

    [models/model%{num}]
    dep.input = inputs/input%{num}.txt
    dep.train = bin/train
    recipe = ./%{train} %{input} %{target}

Now you would like to automatically produce the model for every input that is
there. You can do this by writing a _task_, i.e., a rule for a target that is
not a file but is just invoked. The task for the example might look like this:

    [all_models]
    type = task
    deps = %{'models/{}'.format(i.replace('input', 'model').replace('.txt, \
             '') for i in os.listdir('inputs')}

This task does not need a recipe because all it does is pull in all the models
through its dependencies. The dependencies are specified through an arbitrary
Python expression, in this case it looks at the inputs directory and returns
the names of the models corresponding to each input. It uses the `os` module,
which needs to be imported. So let’s add a global section with a prelude to do
this. The whole Producefile then looks like this:

    []
    prelude =
        import os

    [models/model%{num}]
    dep.input = inputs/input%{num}.txt
    dep.train = bin/train
    recipe = ./%{train} %{input} %{target}

    [all_models]
    type = task
    deps = %{'models/{}'.format(i.replace('input', 'model').replace('.txt, \
             '') for i in os.listdir('inputs')}

And to produce all models, all you need to do is tell Produce to produce the
`all_models` task:

    $ produce all_models

## All special attributes at a glance

For your reference, here are all the rule attributes that currently have a
special meaning to Produce:

### In rules

<dl>
    <dt><code>target</code></dt>
    <dd>When a rule matches a target, this variable is always set to that
    target, mainly so you can refer to it in the recipe. It is illegal to set
    the <code>target</code> attribute yourself. Also see
    <a href="#rules-expansions-escaping-and-comments">Rules, expansions, escaping and comments</a>.</dd>
    <dt><code>cond</code></dt>
    <dd>Allows to specify a _matching condition_ in addition to the target
    pattern. Typically it is given as a single expansion with a boolean Python
    expression. It is expanded immediately after a target matches the rule. The
    resulting string must be a Python literal. If “truthy”, the rule matches
    and its expansion/execution continues. If “falsy”, the rule does not match
    the target and Produce proceeds with the next rule, trying to match the
    target. Also see <a href="#multiple-wildcards-regular-expressions-and-matching-conditions">Multiple wildcards, regular expressions and matching conditions</a>.</dd>
    <dt><code>dep.*</code></dt>
    <dd>The asterisk stands for a name chosen by you, which is the actual name
    of the variable the attribute value will be assigned to. The <code>dep.</code> prefix,
    not part of the variable name, tells Produce that this is a dependency,
    i.e. that the target given by the value must be made up to date before the
    recipe of this rule can be run. Also see
    <a href="#named-and-unnamed-dependencies">Named an unnamed depenencies</a>.</dd>
    <dt><code>deps</code></dt>
    <dd>Like <code>dep.*</code>, but allows for specifying multiple unnamed dependencies
    in one attribute value. The format is roughly a space-separated list. For
    details, see
    <a href="https://docs.python.org/3/library/shlex.html?highlight=shlex#shlex.split"><code>shlex.split</code></a>.
    Also see <a href="#named-and-unnamed-dependencies">Named an unnamed depenencies</a>.</dd>
    <dt><code>depfile</code></dt>
    <dd>Another way to specify (additional) dependencies: the name of a file
    from which dependencies are read, one per line. Additionally, Produce will
    try to make that file up to date prior to reading it. Also see
    <a href="#dependency-files">Dependency files</a>.</dd>
    <dt><code>type</code></dt>
    <dd>Is either <code>file</code> (default) or <code>task</code>. If <code>file</code>, the target is supposed
    to be a file that the recipe creates/updates if it runs successfully. If
    <code>task</code>, the target is an arbitrary name given to some task that the recipe
    executes. Crucially, task-type targets are always assumed to be out of
    date, regardless of the possible existence and age of a file with the same
    name. Also see
    <a href="#special-targets-vs-special-attributes">Special targets vs. special attributes</a></dd>
    <dt><code>recipe</code></dt>
    <dd>The command(s) to run to build the target, typically a single shell
    command or a short shell script. Unlike Make, each line is not run in
    isolation, but the whole script is passed to the interpreter as a whole,
    after doing expansions. This way, you can e.g. define a shell variable
    on one line and use it on the next. Also see
    <a href="#rules-expansions-escaping-and-comments">Rules, expansions, escaping and comments</a>.</dd>
    <dt><code>shell</code></dt>
    <dd>See <a href="#shell-choosing-the-recipe-interpreter"><code>shell</code>: choosing the recipe interpreter</a></dd>
    <dt><code>out.*</code></dt>
    <dd>See <a href="#rules-with-multiple-outputs">Rules with multiple outputs</a></dd>
    <dt><code>outputs</code></dt>
    <dd>See <a href="#rules-with-multiple-outputs">Rules with multiple outputs</a></dd>
    <dt><code>jobs</code></dt>
    <dd>See <a href="#running-jobs-in-parallel">Running jobs in parallel</a></dd>
</dl>

### In the global section

<dl>
    <dt><code>default</code></dt>
    <dd>A list
    (parsed by <a href="https://docs.python.org/3/library/shlex.html?highlight=shlex#shlex.split"><code>shlex.split</code></a>)
    of default targets that are produced if the user does not specify any
    targets when calling Produce.</dd>
    <dt><code>prelude</code></dt>
    <dd>See <a href="#the-prelude">The prelude</a></dd>
</dl>

Getting in touch
----------------

Produce is being developed by Kilian Evang <%{firstname}@%{lastname}.name>.
I would love to hear from you if you find it useful, if you have questions, bug
reports or feature requests.

Acknowledgments
---------------

The Produce logo was designed by [Valerio Basile](https://valeriobasile.github.io).
