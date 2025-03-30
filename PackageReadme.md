# Packaging the Therapy Bookkeeper Application

This document outlines the steps to package the Therapy Bookkeeper Flask application into a single executable file using PyInstaller.

## Prerequisites

1.  **Python:** Ensure you have Python installed on your system.
2.  **Pip:** Python's package installer, usually included with Python.
3.  **Project Dependencies:** Make sure all required Python packages are installed. You can usually install them using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```
4.  **PyInstaller:** Install PyInstaller if you haven't already:
    ```bash
    pip install pyinstaller
    ```

## Packaging Command

Navigate to the root directory of the project (the one containing `main.py`) in your terminal or command prompt. Then, run the following command:

```bash
python -m PyInstaller --onefile --windowed --name TherapyBookkeeper --add-data "templates:templates" --add-data "static:static" --add-data "therapist_bookkeeping.db:." --add-data "config.py:." main.py
```

### Command Breakdown:

*   `python -m PyInstaller`: Runs PyInstaller as a module.
*   `--onefile`: Creates a single executable file instead of a folder containing multiple files.
*   `--windowed` (or `--noconsole`): Prevents the console window from appearing when the application runs. Use this for GUI applications.
*   `--name TherapyBookkeeper`: Sets the name of the output executable (e.g., `TherapyBookkeeper.exe` on Windows).
*   `--add-data "<source>:<destination>"`: Tells PyInstaller to bundle additional data files or folders. This is crucial for including templates, static assets (CSS, JS, images), the database file, and configuration files.
    *   `templates:templates`: Bundles the `templates` folder into the executable, making it available at the path `templates` within the packaged app.
    *   `static:static`: Bundles the `static` folder.
    *   `therapist_bookkeeping.db:.`: Bundles the database file into the root directory (`.`) within the packaged app.
    *   `config.py:.`: Bundles the configuration file into the root directory (`.`) within the packaged app.
*   `main.py`: Specifies the main entry point script for your application.

## Output

After the command finishes successfully, PyInstaller will create a few folders:

*   `build`: Contains intermediate build files. You can usually delete this after a successful build.
*   `dist`: Contains the final packaged application. Your executable (`TherapyBookkeeper.exe` or similar) will be inside this folder.
*   A `.spec` file (`TherapyBookkeeper.spec`): This file stores the configuration used by PyInstaller. You can modify this file for more advanced packaging options and rerun PyInstaller using `pyinstaller TherapyBookkeeper.spec`.

## Running the Packaged Application

Navigate to the `dist` folder and simply double-click the `TherapyBookkeeper` executable to run the application. It should start the server and open the application in your default web browser. Use the "Shutdown Application" button within the app to close it properly.
