# 🎲 Snake and Ladders — Android Game

A fully playable **Snake and Ladders** game for Android, built with **Python + Kivy**.  
Players enter their own names, roll dice, climb ladders, and dodge snakes!

---

## 📱 Screenshots

> *(Add screenshots here after building)*

---

## ✨ Features

- 🎮 **2-player local multiplayer**
- ✏️ **Custom player names** — enter before starting
- 🎲 **Animated dice rolling**
- 🪜 **Ladders** to climb up (4→14, 9→31, 20→38, 28→84, 40→59, 51→67, 63→81, 71→91)
- 🐍 **Snakes** to slide down (25→7, 36→3, 52→42, 70→55, 99→54)
- 🏆 **Win screen** with replay option
- 📱 **Portrait mode**, mobile-first layout
- 🌙 **Dark theme** UI

---

## 🗂 Project Structure

```
snake_ladders_android/
├── main.py               # Full game code (Python + Kivy)
├── buildozer.spec        # Android build configuration
├── requirements.txt      # Python dependencies
├── .github/
│   └── workflows/
│       └── build.yml     # GitHub Actions — auto-build APK on push
├── assets/
│   └── icon.png          # App icon (512×512, add your own)
└── README.md
```

---

## 🚀 How to Build the APK

### Option A — Build Locally (Linux / WSL)

**1. Install system dependencies:**
```bash
sudo apt-get update
sudo apt-get install -y git zip unzip openjdk-17-jdk \
  python3-pip autoconf libtool pkg-config \
  zlib1g-dev libncurses5-dev cmake libffi-dev libssl-dev
```

**2. Install Python packages:**
```bash
pip install buildozer==1.5.0 Cython==3.0.0
```

**3. Clone this repo:**
```bash
git clone https://github.com/YOUR_USERNAME/snake-ladders-android.git
cd snake-ladders-android
```

**4. Build the APK:**
```bash
buildozer android debug
```

The APK will be in the `bin/` folder.  
Transfer it to your phone and install (enable "Install from unknown sources" in settings).

---

### Option B — Build via GitHub Actions (no local setup needed!)

1. **Fork** this repository on GitHub
2. Go to **Actions** tab → select **Build Android APK**
3. Click **Run workflow**
4. Wait ~15–20 minutes for the build to complete
5. Download the APK from the **Artifacts** section of the completed run

---

### Option C — Run on Desktop (for testing)

```bash
pip install kivy==2.3.0
python main.py
```

---

## 🎮 How to Play

1. Launch the app on your Android device
2. Enter names for **Player 1** (Red) and **Player 2** (Blue)
3. Tap **START GAME**
4. Take turns tapping **Roll Dice**
5. Move forward by the number rolled
6. Land on a **ladder bottom** → climb up 🪜
7. Land on a **snake head** → slide down 🐍
8. First player to reach **Square 100** wins! 🏆

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11 |
| UI Framework | [Kivy 2.3](https://kivy.org) |
| Android packaging | [Buildozer](https://buildozer.readthedocs.io) |
| CI/CD | GitHub Actions |

---

## 📦 Customisation

**Change snakes / ladders** — edit these dicts in `main.py`:
```python
SNAKES  = {99: 54, 70: 55, 52: 42, 25: 7, 36: 3}
LADDERS = {4: 14, 9: 31, 20: 38, 28: 84, 40: 59, 51: 67, 63: 81, 71: 91}
```

**Change app name / package** — edit `buildozer.spec`:
```ini
title = Snake and Ladders
package.name = snakeladders
package.domain = com.yourusername
```

**Add your own icon** — place a 512×512 PNG at `assets/icon.png`  
then uncomment this line in `buildozer.spec`:
```ini
icon.filename = %(source.dir)s/assets/icon.png
```

---

## 🤝 Contributing

Pull requests welcome! Open an issue first for major changes.

---

## 📄 License

MIT License — free to use, modify, and distribute.
