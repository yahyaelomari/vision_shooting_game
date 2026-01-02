# Cyber Shooter - Vision Controlled Game

A computer vision-based shooting game where you control the crosshair with your hand and shoot by winking!

## Features

-   **Hand Tracking Aim**: Move your index finger to control the crosshair on screen.
-   **Wink to Shoot**: Wink either eye to fire a shot.
-   **Dynamic Gameplay**: Shoot shapes to score points, avoid missing!
-   **Leaderboard**: Track your high scores.
-   **Neon Aesthetics**: Cyberpunk-inspired visual style.

## Prerequisites

-   Python 3.8+
-   Webcam

## Installation

1.  **Clone the repository** (if applicable) or download the source code.
2.  **Set up a virtual environment** (recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

You can easily start the game using the provided helper script:

```bash
./run_game.sh
```

Or manually:

```bash
python3 main.py
```

## How to Play

1.  **Start the Game**: Click "START" on the main menu using your hand cursor (hover over the button).
2.  **Enter Name**: Type your name and press ENTER.
3.  **Aim**: Hold up your hand. The crosshair follows your **index finger tip**.
4.  **Shoot**: **Wink** (close one eye briefly) to shoot at the target.
5.  **Score**:
    -   Hit shapes to gain points.
    -   Don't miss! Missing a shot results in GAME OVER.
    -   The game lasts for 2 minutes.
6.  **Pause**: Press `P` to pause/unpause.
7.  **Menu**: Press `SPACE` to return to the menu from the Game Over screen.

## Controls

-   **Mouse/Hand**: Aim
-   **Wink**: Shoot
-   **P**: Pause Game
-   **SPACE**: Return to Menu / Resume

## Troubleshooting

-   **Camera not working?** Ensure your webcam is connected and not being used by another application.
-   **Laggy?** Ensure you have good lighting for the camera to track your hand and face effectively.

## Credits

Developed by Yahya Ismail.
