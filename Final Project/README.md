# Sokoban Game

A classic Sokoban (box-pusher) puzzle game built with Python and Pygame.

## 🎮 Game Description

Sokoban is a puzzle game where the player pushes boxes onto target locations. The goal is to move all boxes to their designated spots using the minimum number of moves. The game features multiple levels of increasing difficulty.

## ✨ Features

- **5 Challenging Levels**: Progressive difficulty from easy to expert
- **Undo Functionality**: Press `U` to undo your last move
- **Level Reset**: Press `R` to restart the current level
- **Player Animation**: Player sprite rotates based on movement direction
- **Background Music**: Enjoy music while playing
- **Victory Screen**: Special ending screen when all levels are completed
- **Custom Level Support**: Edit `levels.txt` to add your own levels
- **Easy Launch**: One-click launcher for Windows

## 📋 Requirements

- Python 3.x (3.7 or higher recommended)
- Pygame 2.6.1

## 🚀 Installation

### Method 1: Using the Launcher (Windows)

1. Double-click `START_GAME.bat`
2. The launcher will automatically:
   - Check for Python installation
   - Install required dependencies
   - Start the game

### Method 2: Manual Installation

1. **Install Python** (if not already installed)
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Game**
   ```bash
   python Sokoban.py
   ```
   or on Windows:
   ```bash
   py Sokoban.py
   ```

## 🎮 Controls

| Key | Action |
|-----|--------|
| **Arrow Keys** or **WASD** | Move player |
| **U** | Undo last move |
| **R** | Reset current level |
| **ESC** | Exit game |
| **N** | Next level (after completing a level) |
| **S** | Start game (in menu) |
| **Q** | Quit (in menu and ending screen) |

## 📁 Project Structure

```
Final Project/
│
├── Sokoban.py          # Main game file
├── levels.txt          # Level maps (customizable)
├── requirements.txt    # Python dependencies
├── START_GAME.bat      # Windows launcher
├── README.md           # This file
│
├── Picture/            # Image resources
│   └── Player.png      # Player sprite
│
└── BGM/                # Background music (optional)
    └── game-background-music.mp3
```

## 🗺️ Creating Custom Levels

You can create your own levels by editing `levels.txt`:

- Use `#` for walls
- Use ` ` (space) for floor
- Use `$` for boxes
- Use `.` for target locations
- Use `@` for player
- Use `*` for box on target
- Use `+` for player on target

Separate levels with `---` on a new line.

### Example Level Format:
```
########
#      #
#  $$  #
#  @   #
#      #
#  ..  #
########
---
#######
#     #
# $ $ #
...
```

## 🎯 Game Rules

1. Push boxes to target locations (marked with `.`)
2. Boxes can only be pushed, not pulled
3. You cannot push two boxes at once
4. Complete all levels to win!

## 🐛 Troubleshooting

### "Python not found" Error
- Install Python 3.x from https://www.python.org/downloads/
- Ensure "Add Python to PATH" is checked during installation

### "Module 'pygame' not found" Error
- Run: `pip install -r requirements.txt`
- Make sure you're using the correct Python interpreter

### Game Crashes or Resources Missing
- Ensure `Picture/Player.png` exists
- Ensure `levels.txt` exists in the same directory
- Check that all files are in the correct locations

### Font/Text Display Issues
- The game uses system fonts as fallback
- For best results, ensure your system has standard fonts installed

## 📝 Notes

- The game automatically saves your progress through levels
- Use the undo feature to experiment with different moves
- Background music is optional - the game works without it
- The game supports both English and will fallback gracefully for missing resources

## 👨‍💻 Development

This game was built using:
- **Python 3.x**
- **Pygame 2.6.1**

## 📄 License

This project is provided as-is for educational and personal use.

## 🙏 Credits

- Game concept based on the classic Sokoban puzzle game
- Built with Pygame framework

---

Enjoy playing! 🎉

