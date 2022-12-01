package main

import (
	"aoc/lib/jfile"
	"aoc/lib/jpy"
	"fmt"
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
	result := jpy.Max(sums)
	fmt.Println(result)
}
