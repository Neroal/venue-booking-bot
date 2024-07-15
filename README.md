# Venue Booking Bot

This project is an Electron application that automates the process of booking venues. It uses a Python script for the automation logic and an HTML interface for user input.

## Project Setup

### Prerequisites

- Node.js and npm
- Python 3.x
- pip (Python package installer)
- PyInstaller (for packaging the Python script)

### Step 1: Clone the Repository

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/yourusername/venue-booking-bot.git
cd venue-booking-bot
```

### Step 2: Set Up the Python Environment
Create and activate a virtual environment:

```bash
python3 -m venv bot_env
source bot_env/bin/activate
```

Install the required Python packages:
```bash
pip install git+https://github.com/g1879/DrissionPage.git
pip install pyinstaller
```

### Step 3: Package the Python Script
Use PyInstaller to package the Python script into a standalone executable:
```bash
pyinstaller --onefile main.py
```
This will create a dist directory with the packaged executable (main or main.exe).

### Step 4: Set Up the Electron Application
Install the necessary Node.js packages:
```bash
npm install
```

### Step 5: Run the Application
Start the Electron application:
```bash
npm start
```

## Project Structure
```
venue-booking-bot
├── dist
│   └── main           # Packaged Python executable
├── src
│   ├── index.html     # HTML file for user interface
│   ├── main.js        # Main process script for Electron
│   ├── preload.js     # Preload script for Electron
│   └── renderer.js    # Renderer process script for Electron
├── main.py            # Python script for automation logic
├── package.json       # Project configuration for npm
└── README.md          # Project documentation
```

## Files

`main.py`
This is the Python script containing the automation logic. It uses the DrissionPage library to interact with the website.

`src/main.js`
This is the main process script for the Electron application. It creates the browser window and handles communication between the renderer process and the Python script.

`src/preload.js`
This script is used to securely expose Node.js functionality to the renderer process.

`src/renderer.js`
This script handles the front-end logic and communicates with the main process.

`src/index.html`
This is the HTML file that defines the user interface for the application.

## Configuration
In src/main.js, ensure the path to the Python executable is correct:

```
const pythonExecutablePath = path.join(__dirname, '../dist/main'); // Adjust this path if necessary
```
In main.py, ensure the script logic is correct for your booking needs

## Usage
1. Fill in the account and password fields.
2. Select the desired time slot from the dropdown menu.
3. Click the "Submit" button to start the booking process.

## Troubleshooting
If you encounter issues with the Python script not being found, ensure the path in src/main.js is correct and that the Python script has been packaged correctly with PyInstaller.

If you encounter other issues, check the developer tools console for error messages and ensure all dependencies are installed correctly.