const { app, BrowserWindow, ipcMain } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

let mainWindow;
let flaskProcess = null;

function createWindow() {
    mainWindow = new BrowserWindow({
        // ... other window configuration
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: false,
            nodeIntegration: true,
            // other webPreferences
        }
    });

    // Point to Flask server URL
    mainWindow.loadURL('http://localhost:5000/');

    // Open DevTools for debugging (optional)
    mainWindow.webContents.openDevTools();

    ipcMain.on('load-page', (event, page) => {
        // Load the content of the page into the mainWindow without a full reload
        const content = fs.readFileSync(path.join(__dirname, page), 'utf8');
        mainWindow.webContents.send('display-content', content);
      });

    mainWindow.on('closed', function () {
        mainWindow = null;
        if (flaskProcess != null) {
            flaskProcess.kill(); // Kill Flask server when closing the app
        }
    });
}

app.on('ready', () => {
    // Construct the relative path to the Python executable within your venv
    const pythonPath = path.join(__dirname, '.venv', 'bin', 'python3');

    // Start Flask server
    flaskProcess = spawn(pythonPath, ['main.py']);

    // Wait for Flask server to start before creating window
    setTimeout(createWindow, 3000); // Adjust time as necessary
});

app.on('window-all-closed', () => {
    // On macOS, it is common for applications and their menu bar to stay active until the user quits explicitly with Cmd + Q
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    // On macOS, recreate a window in the app when the dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

app.on('quit', () => {
    // Kill Flask server when quitting the app
    if (flaskProcess != null) {
        flaskProcess.kill();
    }
});