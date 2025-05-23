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
}

function startBackend() {
    return new Promise((resolve, reject) => {
        const py = spawn('python3', ['python/backend.py'], { stdio: ['pipe', 'pipe', 'pipe'] });

        let backendReady = false;

        py.stdout.on('data', (data) => {
            data = data.toString().trim();

            if (data === "__READY__") {
                backendReady = true;
                resolve();  // Trigger the Electron window
                return;
            }

            if (!backendReady) {
                process.stdout.write(data + "\n");  // Spinner and initial output
            }
        });

        py.stderr.on('data', (err) => {
            if (!backendReady) {
                console.error(`Python error: ${err}`);
            }
        });

        py.on('close', (code) => {
            if (code !== 0) {
                console.log("Backend exited with code:", code);
            }
        });
    });
}

app.whenReady().then(() => {
    startBackend().then(() => {
        createWindow();
    }).catch(err => {
        console.error('Backend failed:', err);
        app.quit();
    });
});

