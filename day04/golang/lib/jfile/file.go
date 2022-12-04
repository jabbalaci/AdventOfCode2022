package jfile

import (
	"io"
	"log"
	"os"
	"strconv"
	"strings"
)

// Read the content of a text file and return it as a string.
func Read(fname string) (string, error) {
	f, err := os.Open(fname)
	if err != nil {
		log.Fatal(err)
		return "", err
	}
	defer f.Close()
	content, err := io.ReadAll(f)
	if err != nil {
		log.Fatal(err)
		return "", err
	}
	return string(content), nil
}

// Read the content of a text file and return it as a list of strings.
func ReadLines(fname string) ([]string, error) {
	content, err := Read(fname)
	if err != nil {
		log.Fatal(err)
		return []string{}, err
	}
	content = strings.TrimSpace(content)
	return strings.Split(content, "\n"), nil
}

// The input file contains integers, one per line.
// This function returns them as a list if integers.
func ReadLinesAsInts(fname string) ([]int, error) {
	lines, err := ReadLines(fname)
	if err != nil {
		log.Fatal(err)
		return []int{}, err
	}
	result := make([]int, 0, len(lines))
	for _, line := range lines {
		number, _ := strconv.Atoi(line)
		result = append(result, number)
	}
	return result, nil
}
