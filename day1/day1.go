package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

func puzzle1(lines []string, part string) {
	total := 0
	matcher, _ := regexp.Compile("\\d")
	for _, line := range lines {
		matches := matcher.FindAllString(line, -1)
		value := matches[0] + matches[len(matches)-1]
		intVal, _ := strconv.Atoi(value)
		total = total + intVal
	}
	fmt.Println("Answer for part", part, total)
}

func puzzle2(lines []string) {
	newLines := []string{}

	replaceMap := make(map[string]string)
	replaceMap["one"] = "o1e"
	replaceMap["two"] = "t2o"
	replaceMap["three"] = "t3e"
	replaceMap["four"] = "f4r"
	replaceMap["five"] = "f5e"
	replaceMap["six"] = "s6x"
	replaceMap["seven"] = "s7n"
	replaceMap["eight"] = "e8t"
	replaceMap["nine"] = "n9e"

	for _, line := range lines {
		newLine := line
		for old, new := range replaceMap {
			newLine = strings.ReplaceAll(newLine, old, new)
		}
		newLines = append(newLines, newLine)
	}

	puzzle1(newLines, "2")
}

func main() {
	file, err := os.Open("../Inputs/day1.txt")
	if err != nil {
		fmt.Printf("error opening file: %v\n", err)
		os.Exit(1)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)

	lines := []string{}
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		fmt.Printf("error processing file: %v\n", err)
		os.Exit(1)
	}

	puzzle1(lines, "1")
	puzzle2(lines)

}
