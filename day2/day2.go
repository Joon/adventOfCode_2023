package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

type Turn struct {
	red   int
	blue  int
	green int
}

type Game struct {
	gameId int
	turns  []Turn
}

func parseGame(line string) Game {
	result := Game{}
	parts := strings.Split(line, " ")
	result.gameId, _ = strconv.Atoi(parts[0])
	return result
}

func main() {
	content, err := ioutil.ReadFile("inputs/day2.txt")
	if err != nil {
		fmt.Println("Error reading file:", err)
		return
	}

	lines := strings.Split(string(content), "\n")

	for _, line := range lines {
		game := parseGame(line)
		fmt.Println(game)
	}
}
