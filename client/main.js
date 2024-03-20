const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
const http = require('http');

let mainWindow;
let flaskProcess;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
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

function pingServer() {
    http.get('http://localhost:5000/ping/', (res) => {
        const { statusCode } = res;
        if (statusCode === 200) {
            console.log('Server is up!');
            createWindow(); // Replace with your actual function to create the window
        } else {
            console.log('Server responded with status code:', statusCode);
            setTimeout(pingServer, 300); // Retry after 300 milliseconds
        }
    }).on('error', (err) => {
        console.log('Error pinging server:', err.message);
        setTimeout(pingServer, 300); // Retry after 300 milliseconds
    });
}

app.on('ready', () => {
    // Start Flask server
    flaskProcess = spawn('.venv/bin/python', ['app.py'], { stdio: 'inherit' });

    // Start pinging the server after a short initial delay
    setTimeout(pingServer, 300);
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