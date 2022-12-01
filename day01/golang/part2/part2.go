package main

import (
	"aoc/lib/jfile"
	"aoc/lib/jpy"
	"aoc/lib/jslice"
	"fmt"
	"sort"
	"strconv"
	"strings"
)

func main() {
	// fname := "example.txt"
	fname := "input.txt"

	content, _ := jfile.Read(fname)
	content = strings.TrimSpace(content)
	parts := strings.Split(content, "\n\n")
	sums := []int{}
	for _, part := range parts {
		lines := strings.Split(part, "\n")
		numbers := jpy.Map(lines, func(s string) int {
			number, _ := strconv.Atoi(s)
			return number
		})
		sums = append(sums, jpy.Sum(numbers))
	}
	sort.Ints(sums)
	jslice.Reverse(sums)

	result := jpy.Sum(sums[:3])
	fmt.Println(result)
}
