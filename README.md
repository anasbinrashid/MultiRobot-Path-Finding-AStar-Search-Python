# Multi-Robot Path Planning with Dynamic Obstacles

A Python implementation of multi-robot path planning using A* search algorithm with support for dynamic moving agents and obstacle avoidance.

## Overview

This project simulates multiple robots navigating through a grid-based environment while avoiding static obstacles and dynamic moving agents. Each robot uses the A* pathfinding algorithm to find optimal routes to their destinations while considering real-time positions of other agents.

## Features

- **Multi-Robot Navigation**: Supports multiple robots with individual start and goal positions
- **A* Pathfinding**: Implements A* search algorithm with Manhattan distance heuristic
- **Dynamic Obstacle Avoidance**: Handles moving agents that follow predefined cyclic paths
- **Collision Prevention**: Prevents robots from occupying the same cell simultaneously
- **Real-time Replanning**: Robots recompute paths when blocked by dynamic obstacles
- **Simulation Statistics**: Tracks completion times and identifies stuck robots

## Architecture

### Core Components

- **Robot Class**: Manages individual robot state, routes, and navigation
- **A* Search**: Pathfinding algorithm with temporal-spatial state space
- **Dynamic Agent System**: Handles moving obstacles with cyclic behavior
- **Simulation Engine**: Coordinates multi-robot movement and collision detection

### Key Algorithms

1. **Temporal A* Search**: Extended A* that considers time dimension for dynamic obstacles
2. **Manhattan Distance Heuristic**: Efficient distance estimation for grid-based navigation
3. **Cyclic Path Generation**: Dynamic agents follow forward-backward cyclic routes

## Getting Started

### Prerequisites

- Python 3.7+
- Required packages: `heapq`, `re` (built-in modules)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/multi-robot-pathfinding.git
cd multi-robot-pathfinding
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Input File Formats

#### Grid File (`data2.txt`)
```
20
####################
#..................#
#.X..X.............#
#..................#
####################
```
- First line: grid size
- Following lines: grid layout ('X' = obstacle, '.' = free space, '#' = wall)

#### Robot File (`Robots2.txt`)
```
Robot 1: Start (1, 1) End (18, 18)
Robot 2: Start (2, 2) End (17, 17)
```

#### Agent File (`Agent2.txt`)
```
Agent 1: [(5, 5), (6, 5), (7, 5)] at times [0, 1, 2]
Agent 2: [(10, 10), (11, 10)] at times [0, 1]
```

### Running the Simulation

```bash
python src/pathfinding.py
```

## Configuration

### Key Parameters

- **Maximum Iterations**: 10,000 (prevents infinite loops)
- **Search Limit**: 10,000 nodes (optimizes performance)
- **Failure Threshold**: 50 failed moves (identifies stuck robots)

### Customization

Modify file paths in `main()` function:
```python
with open('path/to/your/data2.txt', "r") as file:
```

## Output

The simulation provides:

- Grid visualization
- Dynamic agent paths and timing
- Robot start/goal positions
- Individual robot paths
- Completion times
- Overall simulation statistics

### Sample Output
```
Grid (20 x 20):
####################
#..................#
#.X..X.............#

Dynamic Agents:
- Agent 1: [(5, 5), (6, 5), (7, 5)] at times [0, 1, 2, 3, 4]

Robots:
- Robot 1: Start (1, 1), Goal (18, 18)

Robot 1 Path: [(1, 1), (2, 1), (3, 1), ..., (18, 18)]
Robot 1 Total Time: 34

Simulation finished at Iteration 35
```

## Algorithm Details

### A* Search with Time Dimension

The algorithm extends traditional A* search to include temporal constraints:

- **State**: (position, timestamp)
- **Cost Function**: f(n) = g(n) + h(n)
  - g(n): Actual path cost from start
  - h(n): Manhattan distance heuristic to goal
- **Dynamic Constraints**: Avoids positions occupied by moving agents at specific times

### Dynamic Agent Behavior

Moving agents follow cyclic patterns:
1. Forward path: follows specified waypoints
2. Backward path: reverses through waypoints
3. Continuous cycling throughout simulation

## Performance Optimizations

- **Early Termination**: Limits search depth for non-critical robots
- **Closed List Pruning**: Prevents revisiting explored states
- **Heuristic Guidance**: Manhattan distance provides efficient search direction
- **Memory Management**: Efficient state representation and storage

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- A* algorithm implementation based on classical pathfinding techniques
- Multi-agent coordination inspired by robotics research
- Grid-based navigation concepts from game AI development
