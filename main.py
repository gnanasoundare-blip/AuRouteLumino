import pygame
from collections import deque
import heapq

pygame.init()

WIDTH = 800
HEIGHT = 700
GRID_HEIGHT = 600

ROWS = 20
COLS = 20

CELL_SIZE = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AuRouteLumino")

clock = pygame.time.Clock()

# --------------------------------------------------
# COLORS
# --------------------------------------------------

BACKGROUND = (30, 30, 30)
GRID_COLOR = (80, 80, 80)

START_COLOR = (0, 255, 0)
END_COLOR = (255, 0, 0)

OBSTACLE_COLOR = (0, 0, 0)
VISITED_COLOR = (70, 100, 180)
PATH_COLOR = (255, 255, 0)

TEXT_COLOR = (240, 240, 240)
SUBTEXT_COLOR = (190, 190, 190)
WARNING_COLOR = (255, 120, 120)

# --------------------------------------------------
# FONTS
# --------------------------------------------------

title_font = pygame.font.SysFont("Arial", 26, bold=True)
subtitle_font = pygame.font.SysFont("Arial", 17)
info_font = pygame.font.SysFont("Arial", 17)
small_font = pygame.font.SysFont("Arial", 15)

# --------------------------------------------------
# GRID STATE
# --------------------------------------------------

start = None
end = None
obstacles = set()

visited = set()
path = []

# --------------------------------------------------
# SEARCH STATE
# --------------------------------------------------

queue = deque()
open_set = []

came_from = {}
cost_so_far = {}

searching = False
showing_path = False

path_index = 0

last_search_time = 0
last_path_time = 0

SEARCH_DELAY = 60
PATH_DELAY = 120

algorithm = None
message = ""

# --------------------------------------------------
# GET NEIGHBORS
# --------------------------------------------------

def get_neighbors(cell):

    row, col = cell

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    neighbors = []

    for dr, dc in directions:

        new_row = row + dr
        new_col = col + dc

        if 0 <= new_row < ROWS and 0 <= new_col < COLS:

            neighbor = (new_row, new_col)

            if neighbor not in obstacles:
                neighbors.append(neighbor)

    return neighbors


# --------------------------------------------------
# MANHATTAN HEURISTIC
# --------------------------------------------------

def heuristic(cell):

    row, col = cell
    end_row, end_col = end

    return abs(row - end_row) + abs(col - end_col)


# --------------------------------------------------
# START BFS
# --------------------------------------------------

def start_bfs():

    global queue
    global came_from
    global visited
    global path
    global searching
    global showing_path
    global path_index
    global last_search_time
    global algorithm
    global message

    queue = deque([start])

    came_from = {
        start: None
    }

    visited = set()
    path = []

    searching = True
    showing_path = False

    path_index = 0

    algorithm = "BFS"
    message = ""

    last_search_time = pygame.time.get_ticks()


# --------------------------------------------------
# START A*
# --------------------------------------------------

def start_astar():

    global open_set
    global came_from
    global cost_so_far
    global visited
    global path
    global searching
    global showing_path
    global path_index
    global last_search_time
    global algorithm
    global message

    open_set = []

    heapq.heappush(
        open_set,
        (heuristic(start), start)
    )

    came_from = {
        start: None
    }

    cost_so_far = {
        start: 0
    }

    visited = set()
    path = []

    searching = True
    showing_path = False

    path_index = 0

    algorithm = "A*"
    message = ""

    last_search_time = pygame.time.get_ticks()


# --------------------------------------------------
# BUILD FINAL PATH
# --------------------------------------------------

def build_path():

    global path
    global path_index
    global searching
    global showing_path
    global last_path_time

    if end not in came_from:

        searching = False
        showing_path = False

        return

    current = end
    new_path = []

    while current is not None:

        new_path.append(current)
        current = came_from[current]

    new_path.reverse()

    path = new_path

    path_index = 0

    searching = False
    showing_path = True

    last_path_time = pygame.time.get_ticks()


# --------------------------------------------------
# NO PATH FOUND
# --------------------------------------------------

def no_path_found():

    global searching
    global showing_path
    global message

    searching = False
    showing_path = False

    message = "No path found!"


# --------------------------------------------------
# UPDATE BFS
# --------------------------------------------------

def update_bfs():

    if not queue:

        no_path_found()
        return

    current = queue.popleft()

    visited.add(current)

    if current == end:

        build_path()
        return

    for neighbor in get_neighbors(current):

        if neighbor not in came_from:

            came_from[neighbor] = current
            queue.append(neighbor)


# --------------------------------------------------
# UPDATE A*
# --------------------------------------------------

def update_astar():

    if not open_set:

        no_path_found()
        return

    current_priority, current = heapq.heappop(open_set)

    if current in visited:
        return

    visited.add(current)

    if current == end:

        build_path()
        return

    for neighbor in get_neighbors(current):

        new_cost = cost_so_far[current] + 1

        if (
            neighbor not in cost_so_far
            or new_cost < cost_so_far[neighbor]
        ):

            cost_so_far[neighbor] = new_cost

            priority = (
                new_cost
                + heuristic(neighbor)
            )

            heapq.heappush(
                open_set,
                (priority, neighbor)
            )

            came_from[neighbor] = current


# --------------------------------------------------
# UPDATE PATH ANIMATION
# --------------------------------------------------

def update_path():

    global path_index
    global showing_path

    if path_index < len(path):

        path_index += 1

    else:

        showing_path = False


# --------------------------------------------------
# RESET
# --------------------------------------------------

def reset():

    global start
    global end
    global obstacles
    global visited
    global path
    global queue
    global open_set
    global came_from
    global cost_so_far
    global searching
    global showing_path
    global path_index
    global algorithm
    global message

    start = None
    end = None

    obstacles.clear()

    visited.clear()
    path.clear()

    queue.clear()
    open_set.clear()

    came_from.clear()
    cost_so_far.clear()

    searching = False
    showing_path = False

    path_index = 0

    algorithm = None
    message = ""


# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

running = True

while running:

    current_time = pygame.time.get_ticks()

    # --------------------------------------------------
    # EVENTS
    # --------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # --------------------------------------------------
        # KEYBOARD
        # --------------------------------------------------

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:

                reset()

            if event.key == pygame.K_SPACE:

                if (
                    start is not None
                    and end is not None
                    and not searching
                    and not showing_path
                ):

                    start_bfs()

            if event.key == pygame.K_a:

                if (
                    start is not None
                    and end is not None
                    and not searching
                    and not showing_path
                ):

                    start_astar()

        # --------------------------------------------------
        # MOUSE
        # --------------------------------------------------

        if event.type == pygame.MOUSEBUTTONDOWN:

            if searching or showing_path:
                continue

            mouse_x, mouse_y = event.pos

            if mouse_y >= GRID_HEIGHT:
                continue

            row = mouse_y // CELL_SIZE
            col = mouse_x // CELL_SIZE

            cell = (row, col)

            # LEFT CLICK
            if event.button == 1:

                if start is None:

                    if cell not in obstacles:
                        start = cell

                elif end is None:

                    if (
                        cell != start
                        and cell not in obstacles
                    ):

                        end = cell

                else:

                    if cell != start and cell != end:

                        obstacles.add(cell)

                message = ""

            # RIGHT CLICK
            elif event.button == 3:

                obstacles.discard(cell)

                if cell == start:
                    start = None

                if cell == end:
                    end = None

                message = ""

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    if searching:

        if current_time - last_search_time >= SEARCH_DELAY:

            if algorithm == "BFS":

                update_bfs()

            elif algorithm == "A*":

                update_astar()

            last_search_time = current_time

    # --------------------------------------------------
    # PATH ANIMATION
    # --------------------------------------------------

    if showing_path:

        if current_time - last_path_time >= PATH_DELAY:

            update_path()

            last_path_time = current_time

    # --------------------------------------------------
    # DRAW BACKGROUND
    # --------------------------------------------------

    screen.fill(BACKGROUND)

    # --------------------------------------------------
    # DRAW VISITED
    # --------------------------------------------------

    for row, col in visited:

        pygame.draw.rect(
            screen,
            VISITED_COLOR,
            (
                col * CELL_SIZE,
                row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
        )

    # --------------------------------------------------
    # DRAW PATH
    # --------------------------------------------------

    for row, col in path[:path_index]:

        pygame.draw.rect(
            screen,
            PATH_COLOR,
            (
                col * CELL_SIZE,
                row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
        )

    # --------------------------------------------------
    # DRAW OBSTACLES
    # --------------------------------------------------

    for row, col in obstacles:

        pygame.draw.rect(
            screen,
            OBSTACLE_COLOR,
            (
                col * CELL_SIZE,
                row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
        )

    # --------------------------------------------------
    # DRAW START
    # --------------------------------------------------

    if start is not None:

        row, col = start

        pygame.draw.rect(
            screen,
            START_COLOR,
            (
                col * CELL_SIZE,
                row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
        )

    # --------------------------------------------------
    # DRAW END
    # --------------------------------------------------

    if end is not None:

        row, col = end

        pygame.draw.rect(
            screen,
            END_COLOR,
            (
                col * CELL_SIZE,
                row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
        )

    # --------------------------------------------------
    # DRAW GRID
    # --------------------------------------------------

    for x in range(0, WIDTH, CELL_SIZE):

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (x, 0),
            (x, GRID_HEIGHT)
        )

    for y in range(0, GRID_HEIGHT, CELL_SIZE):

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (0, y),
            (WIDTH, y)
        )

    # --------------------------------------------------
    # INFORMATION PANEL
    # --------------------------------------------------

    pygame.draw.rect(
        screen,
        (20, 20, 20),
        (0, GRID_HEIGHT, WIDTH, HEIGHT - GRID_HEIGHT)
    )

    # PRODUCT NAME
    title = title_font.render(
        "AuRouteLumino",
        True,
        TEXT_COLOR
    )

    screen.blit(
        title,
        (24, GRID_HEIGHT + 8)
    )

    # SUBTITLE
    subtitle = subtitle_font.render(
        "Pathfinding & Algorithm Visualizer",
        True,
        SUBTEXT_COLOR
    )

    screen.blit(
        subtitle,
        (24, GRID_HEIGHT + 40)
    )

    # AUTHOR
    author = small_font.render(
        "by Gnanasoundare S",
        True,
        SUBTEXT_COLOR
    )

    screen.blit(
        author,
        (24, GRID_HEIGHT + 62)
    )

    # CONTROLS
    controls = info_font.render(
        "[SPACE] BFS     [A] A*     [R] Reset",
        True,
        TEXT_COLOR
    )

    screen.blit(
        controls,
        (370, GRID_HEIGHT + 12)
    )

    # LEGEND
    legend = small_font.render(
        "Green = Start   Red = End   Black = Wall   Blue = Explored   Yellow = Path",
        True,
        TEXT_COLOR
    )

    screen.blit(
        legend,
        (370, GRID_HEIGHT + 45)
    )

    # CURRENT ALGORITHM
    if algorithm is not None:

        algorithm_text = info_font.render(
            "Algorithm: " + algorithm,
            True,
            TEXT_COLOR
        )

        screen.blit(
            algorithm_text,
            (370, GRID_HEIGHT + 70)
        )

    # MESSAGE
    if message:

        message_text = info_font.render(
            message,
            True,
            WARNING_COLOR
        )

        screen.blit(
            message_text,
            (WIDTH - 180, GRID_HEIGHT + 70)
        )

    pygame.display.flip()

    clock.tick(60)


pygame.quit()