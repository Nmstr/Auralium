// main.js

const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let flaskProcess;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true
        }
    });

    // Point to Flask server URL
    mainWindow.loadURL('http://localhost:5000/');

    // Open DevTools for debugging
    mainWindow.webContents.openDevTools();

    mainWindow.on('closed', function () {
        mainWindow = null;
        flaskProcess.kill(); // Kill Flask server when closing the app
    });
}

app.on('ready', () => {
    // Start Flask server
    flaskProcess = spawn('.venv/bin/python', ['app.py'], { stdio: 'inherit' });

    // Wait for Flask server to start before creating window
    setTimeout(createWindow, 3000); // Adjust time as necessary
});

app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', function () {
    if (mainWindow === null) {
        createWindow();
    }
});