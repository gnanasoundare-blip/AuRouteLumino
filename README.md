# AuRouteLumino

**An interactive pathfinding visualizer built with Python and Pygame.**

AuRouteLumino demonstrates how pathfinding algorithms explore a grid and find routes between two points while navigating around obstacles.

## Features

- Interactive 20 × 20 grid.
- Start and destination placement.
- Obstacle placement for creating custom maze-like environments.
- Breadth-First Search (BFS) pathfinding.
- A* Search pathfinding.
- Animated exploration and path reconstruction.
- No-path detection when the destination cannot be reached.
- Visual interface with a legend and algorithm controls.

## Technologies Used

- Python
- Pygame

## Getting Started

### Prerequisites

- Python 3.13 or a compatible Python 3 version.
- pip, Python's package installer.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/gnanasoundare-blip/AuRouteLumino.git
   ```

2. Navigate to the project directory:

   ```bash
   cd AuRouteLumino
   ```

3. Create a virtual environment (recommended):

   ```bash
   python -m venv .venv
   ```

4. Activate the virtual environment on Windows:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

5. Install the required dependency:

   ```bash
   pip install -r requirements.txt
   ```

6. Run the application:

   ```bash
   python main.py
   ```

## Controls

| Key | Action |
|---|---|
| Space | Run Breadth-First Search (BFS) |
| A | Run A* Search |
| R | Reset the grid |

## Algorithms

**Breadth-First Search (BFS):** Explores the grid systematically and finds a shortest path when movement costs are equal.

**A* Search:** Uses a heuristic to guide its exploration toward the destination, helping it find a shortest path efficiently when the heuristic is appropriate.

## Author

**Gnanasoundare S**

## License

See the [LICENSE](LICENSE) file for licensing information.
