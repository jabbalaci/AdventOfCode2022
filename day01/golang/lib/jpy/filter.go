package jpy

// Filter operation. Keep elements that
// satisfy the condition.
func Filter[T any](data []T, f func(T) bool) []T {
	result := make([]T, 0, len(data))
	for _, e := range data {
		if f(e) {
			result = append(result, e)
		}
	}
	return result
}
