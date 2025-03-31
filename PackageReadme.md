# Packaging the Therapy Bookkeeper Application

This application is packaged into a single executable file using PyInstaller.

## Prerequisites

-   Python installed
-   Pip installed

## Installation Steps

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2.  **Navigate to Project Directory:**
    Open your terminal or command prompt and navigate to the root directory of the Therapy Bookkeeper project (the one containing `main.py`).

3.  **Run PyInstaller:**
    Execute the following command:

    ```bash
    python -m PyInstaller --onefile --windowed --name TherapyBookkeeper --add-data "therapist_bookkeeping.db:." --add-data "templates:templates" --add-data "config.py:." --add-data "static:static" main.py
    ```

    **Explanation of Flags:**
    *   `--onefile`: Creates a single executable file.
    *   `--windowed`: Prevents a console window from appearing when the application runs.
    *   `--name TherapyBookkeeper`: Sets the name of the output executable.
    *   `--add-data "therapist_bookkeeping.db:."`: Includes the database file *within* the executable.
    *   `--add-data "templates:templates"`: Includes the templates directory *within* the executable.
    *   `--add-data "config.py:."`: Includes the configuration file *within* the executable.
    *   `--add-data "static:static"`: Includes the static assets directory (CSS, JS, images) *within* the executable.
    *   `main.py`: Your main application script.

4.  **Find the Executable:**
    PyInstaller will create a `dist` folder. Inside `dist`, you will find `TherapyBookkeeper.exe`. Data files like the database, templates, and config are bundled *inside* the `.exe` itself and extracted to a temporary location when the app runs.

5.  **Prepare for Distribution:**
    *   Copy the generated `TherapyBookkeeper.exe` from the `dist` folder to your desired distribution location.
    *   **Manually copy** the `BackupInstructions.md` file from your project directory and place it in the **same folder** as the `TherapyBookkeeper.exe`.
    *   You can now distribute this folder containing the `.exe` and the `.md` file to the user.
