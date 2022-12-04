package main

import (
	"aoc/lib/jfile"
	"fmt"
	"strconv"
	"strings"
)

func get_values(text string) (int, int) {
	parts := strings.Split(text, "-")
	a, _ := strconv.Atoi(parts[0])
	b, _ := strconv.Atoi(parts[1])
	return a, b
}

func overlap(left, right string) bool {
	v1, v2 := get_values(left)
	v3, v4 := get_values(right)
	case1 := (v1 <= v3) && (v3 <= v2) && (v2 <= v4)
	case2 := (v3 <= v1) && (v1 <= v4) && (v4 <= v2)
	case3 := (v3 <= v1) && (v1 <= v2) && (v2 <= v4)
	case4 := (v1 <= v3) && (v3 <= v4) && (v4 <= v2)
	return case1 || case2 || case3 || case4
}

func main() {
	// fname := "example.txt"
	fname := "input.txt"

	lines, _ := jfile.ReadLines(fname)
	total := 0
	for _, line := range lines {
		parts := strings.Split(line, ",")
		left, right := parts[0], parts[1]
		if overlap(left, right) {
			total++
		}
	}
	fmt.Println(total)
}
