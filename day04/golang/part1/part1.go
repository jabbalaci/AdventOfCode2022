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

func one_contains_other(left, right string) bool {
	v1, v2 := get_values(left)
	v3, v4 := get_values(right)
	elf2_in_elf1 := (v1 <= v3) && (v4 <= v2)
	elf1_in_elf2 := (v3 <= v1) && (v2 <= v4)
	return elf2_in_elf1 || elf1_in_elf2
}

func main() {
	// fname := "example.txt"
	fname := "input.txt"

	lines, _ := jfile.ReadLines(fname)
	total := 0
	for _, line := range lines {
		parts := strings.Split(line, ",")
		left, right := parts[0], parts[1]
		if one_contains_other(left, right) {
			total++
		}
	}
	fmt.Println(total)
}
