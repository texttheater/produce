#include <stdio.h>
#include <fib.h>

int main() {
	for (int i = 0; i < 50; i++) {
		printf("%lli\n", fibonacci());
	}
}
