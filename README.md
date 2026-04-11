# Checkers Engine

A checkers engine I created in Python.

## Description

The engine uses the minimax algorithm and bit masks for fast board operations using bit shifts.
Minimax is enhanced with the well-known alpha-beta pruning (the implementation can be seen in the alpha-beta file of the same name).
The engine also features a transposition table, which stores the evaluation for a position of a given depth using the Zobrist hash.
Further improvements will be added (maybe).

## Usage

The engine is designed for playing against it in the terminal, but you can use and rebuild it however you wish.

An example of a game against it is given below:
The engine is designed for playing against it in the terminal, but you can use and rebuild it however you wish. An example of a game against it is given below:
```text
Hi, input 1/2/3/4/5
1: EASY
2: NORMAL
4: IMPOSSIBLE
5: CUSTOM
4: IMPOSSIBLE
4: IMPOSSIBLE
5: CUSTOM
4
Play from chosen position? Y/n: n
Time: 14.63s, Nodes: 1,146,558, NPS: 78,363
(10, 14)
1:  (20, 16)
2:  (20, 17)
4:  (21, 18)
5:  (22, 18)
6:  (22, 19)
7:  (23, 19)
```
