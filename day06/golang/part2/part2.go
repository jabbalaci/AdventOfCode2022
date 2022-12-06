package main

import (
	"aoc/lib/jfile"
	"fmt"
)

const SIZE = 14

func uniq(text string) bool {
	d := make(map[rune]struct{})
	for _, c := range text {
		_, found := d[c]
		if found {
			return false
		}
		// else
		d[c] = struct{}{}
	}
	return true
}

func process(text string) int {
	for i := 0; i < len(text)-SIZE+1; i++ {
		sub := text[i : i+SIZE]
		if uniq(sub) {
			return i + SIZE
		}
	}
	return -1
}

func main() {
	text, _ := jfile.Read("input.txt")
	result := process(text)
	fmt.Println(result)
}
