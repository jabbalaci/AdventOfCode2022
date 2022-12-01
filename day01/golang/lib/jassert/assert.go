// This package provides an assert function.

package jassert

import (
	"fmt"
)

// Assert mimics assert from other languages.
// It panics if the expression is false.
// If msg is given, it is printed as an error message.
func Assert(expr bool, msg string) {
	if !expr {
		panic(fmt.Sprintf("Assertion error: %s.", msg))
	}
}
