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

The `target` variable is automatically available when the rule is invoked,
containing the target matched by the target pattern.

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

The ability to use more than one wildcard in target patterns is Produce’s
killer feature because to this date I have not been able to find a single other
build automation tool that offers it. Rake and others do offer full regular
expressions which are strictly more powerful but not as easy to read. Don’t
worry, Produce supports them too and more, we will come to that. But first
consider the following Produce rule, which might stem from the third example
project we saw in the introduction, the machine learning one:

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
should explain three fine points:

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

#### The prelude

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
