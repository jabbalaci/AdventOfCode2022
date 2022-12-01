package jpy

// Map operation. Transform each element.
func Map[T, U any](data []T, f func(T) U) []U {
	result := make([]U, 0, len(data))
	for _, e := range data {
		result = append(result, f(e))
	}
	return result
}
