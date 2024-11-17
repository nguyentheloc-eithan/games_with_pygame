
# Pygame Games Collection

A collection of games implemented using Pygame, starting with an exciting Space Shooter game! More games will be added in future updates.

## 🎮 Current Games

### Space Shooter
Navigate through space, dodge enemy ships, and blast your way to victory in this classic arcade-style space shooter game.

![Space Shooter Game](space-shooter/images/game_preview.png) 

## 🛠️ Project Structure

```
games_with_pygame/
├── space-shooter/
│   ├── audio/
│   │   ├── explosion.wav
│   │   ├── laser.wav
│   │   └── [other sound effects]
│   ├── code/
│   │   ├── main.py
│   │   └── [other game implementation files]
│   └── images/
│       ├── player.png
│       ├── enemy.png
│       └── [other game assets]
├── [future-game]/
│   ├── audio/
│   ├── code/
│   └── images/
├── requirements.txt
└── README.md
```

## 🔧 Prerequisites

Before running the games, make sure you have the following installed:
- Python 3.7 or higher
- pip (Python package installer)

## 📥 Installation

1. Clone the repository:
```bash
git clone https://github.com/nguyentheloc-eithan/games_with_pygame.git
cd games_with_pygame
```

2. Create a virtual environment (recommended):

### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## 🚀 Running the Games

### Space Shooter

Navigate to the game's code directory:

#### Windows:
```bash
cd space-shooter/code
python main.py
```

#### Linux/macOS:
```bash
cd space-shooter/code
python3 main.py
```

## 🎮 Game Controls

### Space Shooter
- Arrow keys: Move spaceship
- Spacebar: Shoot
- ESC: Pause game
- Q: Quit game

## 📝 Dependencies

- pygame==2.5.2

## 🔍 Troubleshooting

### Common Issues:

1. **Pygame installation fails**:
   - Windows: Try `pip install pygame --pre`
   - Linux: Install SDL dependencies first:
     ```bash
     sudo apt-get install python3-pygame
     ```
   - macOS: Use Homebrew:
     ```bash
     brew install pygame
     ```

2. **No sound on Linux**:
   ```bash
   sudo apt-get install python3-pygame pulseaudio
   ```

3. **Missing Assets Error**:
   - Make sure you're running the game from the correct directory (space-shooter/code)
   - Verify that all audio and image files are present in their respective folders

## 🚀 Coming Soon

Stay tuned for more exciting games that will be added to this collection! Each new game will follow the same organizational structure:
- Separate folder for each game
- Audio assets in the `audio` folder
- Source code in the `code` folder
- Visual assets in the `images` folder

## 🤝 Contributing

Feel free to contribute to this project:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/NewGame`)
3. Follow the project structure:
   - Create a new game folder with `audio`, `code`, and `images` subfolders
   - Place all assets in their respective folders
   - Include clear documentation in your code
4. Commit your changes (`git commit -m 'Add new game'`)
5. Push to the branch (`git push origin feature/NewGame`)
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgments

- Thanks to the Pygame community for their excellent documentation and resources
- Special thanks to all future contributors
