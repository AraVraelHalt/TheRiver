const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js')
        }
    });

    win.loadFile('index.html');

    const py = spawn('python3', ['python/backend.py']);

    py.stdout.on('data', (data) => {
        console.log(`Python: ${data}`);
        win.webContents.send('fromPython', data.toString());
    });

    py.stderr.on('data', (data) => {
        console.error(`Python error: ${data}`);
    });

    py.on('close', (code) => {
        console.log(`Python process exited with code ${code}`);
    });
}

app.whenReady().then(() => {
    createWindow();
});
