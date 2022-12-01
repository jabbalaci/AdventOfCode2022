package jinterfaces

// taken from https://pkg.go.dev/golang.org/x/exp@v0.0.0-20221026153819-32f3d567a233/constraints

type Signed interface {
	~int | ~int8 | ~int16 | ~int32 | ~int64
}

type Unsigned interface {
	~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 | ~uintptr
}

type Integer interface {
	Signed | Unsigned
}

type Float interface {
	~float32 | ~float64
}

type Complex interface {
	~complex64 | ~complex128
}

// Supports the order operators such as > and < .
type Ordered interface {
	Integer | Float | ~string
}

type NumberTypes interface {
	Integer | Float
}
