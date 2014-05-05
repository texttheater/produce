# A possible Makefile rule for .labeled files that could be used instead of the
# corresponding Produce rule. Serves to illustrate how much nicer this can be
# written using Produce.

.SECONDEXPANSION:
out/%.labeled : out/$$(subst test,train,$$(subst dev,train,$$*)).model out/$$(basename $$*).feat
	wapiti label -m $< out/$(basename $*).feat | sed -e 's/\t/ /g' > $@
