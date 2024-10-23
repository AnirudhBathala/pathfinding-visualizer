# Pathfinding Visualizer

This project is a **Pathfinding Visualizer** that helps demonstrate how various pathfinding algorithms work. It provides an interactive interface to visualize how algorithms explore and find paths in a grid.

## Features

- **Grid-based Visualization**: Visualize pathfinding in a grid layout.
- **Multiple Algorithms**: Includes popular pathfinding algorithms.
- **Customizable Grid**: Adjust grid size and obstacles as needed.
- **User Interaction**: Allows setting of start and end points along with walls/obstacles.
- **Real-time Visualization**: See the algorithm explore the grid step-by-step.

## Supported Algorithms

- **Dijkstra's Algorithm**: A weighted algorithm that guarantees the shortest path.
- **A* (A-star)**: A weighted algorithm that uses heuristics to find the optimal path faster than Dijkstra's.
- **Breadth-First Search (BFS)**: An unweighted algorithm that guarantees the shortest path.
- **Depth-First Search (DFS)**: An unweighted algorithm that explores as far as possible before backtracking, does not guarantee the shortest path.

## How to Use

1. **Set Start and End Points**: Click on the grid to place the start (green) and end (red) points.
2. **Add Obstacles**: Click on grid cells to toggle walls (black cells), which the algorithm will avoid.
3. **Select Algorithm**: Choose an algorithm from the provided options.
4. **Run the Visualizer**: Start the visualizer to see the chosen algorithm in action.
5. **Clear Grid**: Reset the grid to try different configurations.

## Installation

### Clone the repository

```bash
git clone https://github.com/AnirudhBathala/pathfinding-visualizer.git
cd pathfinding-visualizer
