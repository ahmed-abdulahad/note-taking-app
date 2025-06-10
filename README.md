# Note-Taking App

A simple note-taking app, built with Python and PyQt5.  
Designed to be clean, minimal, and focused on usability — perfect for personal use.

## 🚀 Features

- 📝 Write and edit notes
- 💾 Local storage (JSON-based)
- 🖥️ Built for desktop

## 📁 Project Structure

```
note-taking-app/
├── README.md
├── LICENSE  
├── main.py
├── .gitignore
├── venv/
├── ui/
│   └── main_window.py
│   └── themes.py
├── models/
│   └── note.py
├── data/
│   └── notes.json
├── assets/
└── requirements.txt
```

## 🛠️ Tech Stack

- Python 3.12.6
- PyQt5 (GUI)
- VS Code (IDE)
- Git for version control

## ⏳ Timeline

This is a 1 – 2 week learning project. (However I have not been consistent for various reasons...)

## 🛠️ Setting up the Environment

1. **Clone this repository to your local machine:**
   
   ```git clone https://github.com/ahmed-abdulahad/note-taking-app.git```

2. **Navigate to the project directory:**

   ```cd note-taking-app```

3. **Create a virtual environment:**

   ```python -m venv venv```

4. **Activate the virtual environment:**

      On windows:
  
   ```.\venv\Scripts\activate```

     On macOS/Linux:

   ```source venv/bin/activate```

5. **Install the required dependencies:**

   ```pip install -r requirements.txt```

6. **Run the app:**

    ```python main.py```

## 🎨 Assets

The project uses the following assets:

- `assets/note-taking-app_icon.png`: Window icon shown in the title bar.
- `assets/dark_mode_moon_icon.png`: Theme icon shown in the theme toggle button.
- `assets/light_mode_sun_icon.png`: Theme icon shown in the theme toggle button.

All assets are stored in the `assets/` directory.

## 🔖 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with 💡 and Python.
