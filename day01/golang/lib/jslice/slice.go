// Package jslice facilitates the work with slices.
package jslice

import "sort"

// Returns the index of an element.
// If not found, -1 is returned.
func Index[T comparable](haystack []T, needle T) int {
	for i, curr := range haystack {
		if curr == needle {
			return i
		}
	}
	return -1
}

// Returns true if the element is found in the slice.
// Returns false if not found.
func Contains[T comparable](haystack []T, needle T) bool {
	return Index(haystack, needle) > -1
}

// Reverses the order of elements in place.
func Reverse[T any](li []T) []T {
	for i, j := 0, len(li)-1; i < j; i, j = i+1, j-1 {
		li[i], li[j] = li[j], li[i]
	}
	return li
}

// Returns a sorted copy of the int slice.
func SortedInts(li []int) []int {
	result := make([]int, len(li))
	copy(result, li)
	sort.Ints(result)
	return result
}

// Returns a sorted copy of the float64 slice.
func SortedFloat64s(li []float64) []float64 {
	result := make([]float64, len(li))
	copy(result, li)
	sort.Float64s(result)
	return result
}

// Returns a sorted copy of the string slice.
func SortedStrings(li []string) []string {
	result := make([]string, len(li))
	copy(result, li)
	sort.Strings(result)
	return result
}
