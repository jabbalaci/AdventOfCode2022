package main

import (
	"aoc/lib/jfile"
	"fmt"
)

const SIZE = 4

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
	// ex := "mjqjpqmgbljsphdztnvjfqwrcgsmlb" // 7
	// ex := "bvwbjplbgvbhsrlpgdmjqwftvncz" // 5
	// ex := "nppdvjthqldpwncqszvftbrmjlhg" // 6
	// ex := "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg" // 10
	// ex := "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw" // 11

	// text := ex

	text, _ := jfile.Read("input.txt")
	result := process(text)
	fmt.Println(result)
}
