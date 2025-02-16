# Grid World
[< Games](./README.md)

Grid World is a single player game in which an agent will begin at a predetermined grid coordinate and learn the optimal path (sequence of actions) to reach the "goal square".

## Initialization

Initializing a Grid World game requires particular parameters, but are not required by the user, as they will all be defined by defaults values:

* `rows`:       Number of rows with which grid will be initialized. Defaults to 3.
* `columns`:    Number of columns with which grid will be initialized. Defaults to 4.
* `goal`:       Row column coordinate at which goal square will be initialized. Defaults to (3, 4).
* `start`:      Coordinate at which agent should begin the game. Defaults to (0, 0).
* `loss`:       Row, column coordinate at which loss square will be located.
* `walls`:      List of row,column coordinates at which wall squares will be located.

## Configuration

If one were to initialize the game with the following arguments:

* `rows`:       3
* `columns`:    4
* `goal`:       (3, 4)
* `start`:      (0, 0)
* `loss`:       (1, 2)
* `walls`:      [(2, 2)]

The game environment ought to appear as:

```
   ┌───┬───┬───┬───┐
 2 │   │   │ ╳ │ ◉ │
   ├───┼───┼───┼───┤
 1 │   │   │ ◎ │   │
   ├───┼───┼───┼───┤
 0 │ A │   │   │   │
   └───┴───┴───┴───┘
     0   1   2   3 
```

Where:

* `A` is the current agent position.
* `◉` (solid target) is the goal square.
* `◎` (hollow target) is the loss square.
* `╳`'s are wall squares, to which the agent cannot move to.