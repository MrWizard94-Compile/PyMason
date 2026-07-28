const { app, BrowserWindow, Menu, dialog, ipcMain, Tray, nativeImage } = require('electron');
const path = require('path');
const fs = require('fs');

let mainWindow;
let tray = null;

function getAppVersion() {
    try {
        const pkg = JSON.parse(
            fs.readFileSync(path.join(__dirname, 'package.json'), 'utf-8')
        );
        return pkg.version || '0.0.0';
    } catch (e) {
        return '0.0.0';
    }
}

function getLicensePath() {
    return path.join(app.getPath('userData'), 'pymason-license.json');
}

function readLicense() {
    try {
        return JSON.parse(fs.readFileSync(getLicensePath(), 'utf-8'));
    } catch (e) {
        return null;
    }
}

function saveLicense(key) {
    const data = {
        key: String(key || '').trim(),
        activatedAt: new Date().toISOString(),
    };
    fs.writeFileSync(getLicensePath(), JSON.stringify(data, null, 2), 'utf-8');
    return data;
}

/** Basic local license format: PM-XXXX-XXXX-XXXX (not a full anti-piracy system) */
function isValidLicenseKey(key) {
    return /^PM-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$/i.test(String(key || '').trim());
}

/**
 * Optional Gumroad license verification.
 * Set env GUMROAD_PRODUCT_ID + network access; falls back to format check offline.
 * https://gumroad.com/api#verify-a-license
 */
async function verifyLicenseOnline(key) {
    const productId = process.env.GUMROAD_PRODUCT_ID || '';
    const url =
        process.env.GUMROAD_VERIFY_URL ||
        'https://api.gumroad.com/v2/licenses/verify';
    if (!productId || !key) return { ok: false, reason: 'no_product_or_key' };
    try {
        const body = new URLSearchParams({
            product_id: productId,
            license_key: String(key).trim(),
        });
        const res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: body.toString(),
        });
        const data = await res.json().catch(() => ({}));
        if (data && data.success) {
            return { ok: true, data };
        }
        return { ok: false, reason: data?.message || 'verify_failed', data };
    } catch (e) {
        return { ok: false, reason: String(e.message || e), offline: true };
    }
}

// Expose for menu activation flow
ipcMain.handle('pymason-verify-license', async (_evt, key) => {
    if (!isValidLicenseKey(key)) {
        return { ok: false, reason: 'invalid_format' };
    }
    const online = await verifyLicenseOnline(key);
    if (online.ok) {
        saveLicense(key);
        return { ok: true, source: 'gumroad' };
    }
    // Offline / no product id: accept valid format and store (craftsman mode)
    if (!process.env.GUMROAD_PRODUCT_ID || online.offline) {
        saveLicense(key);
        return { ok: true, source: 'local_format', note: online.reason };
    }
    return { ok: false, reason: online.reason || 'rejected' };
});

ipcMain.handle('pymason-get-license', async () => {
    const lic = readLicense();
    return lic
        ? { ok: true, key: lic.key, activatedAt: lic.activatedAt }
        : { ok: false };
});

function createTray() {
    const iconPath = path.join(__dirname, '..', 'PyMason.png');
    let image = nativeImage.createFromPath(iconPath);
    if (!image.isEmpty()) {
        image = image.resize({ width: 16, height: 16 });
    }
    tray = new Tray(image.isEmpty() ? nativeImage.createEmpty() : image);
    tray.setToolTip('PyMason');
    tray.setContextMenu(
        Menu.buildFromTemplate([
            {
                label: 'Show PyMason',
                click: () => {
                    if (mainWindow) {
                        mainWindow.show();
                        mainWindow.focus();
                    }
                },
            },
            {
                label: 'Run code',
                click: () => mainWindow?.webContents.send('menu-run'),
            },
            {
                label: 'Stop',
                click: () => mainWindow?.webContents.send('menu-stop'),
            },
            { type: 'separator' },
            { label: 'Quit', click: () => app.quit() },
        ])
    );
    tray.on('double-click', () => {
        if (mainWindow) {
            mainWindow.show();
            mainWindow.focus();
        }
    });
}

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1400,
        height: 900,
        minWidth: 900,
        minHeight: 600,
        icon: path.join(__dirname, '..', 'PyMason.png'),
        title: 'PyMason',
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false,
        },
        backgroundColor: '#0A0807', // WPAI forge background
    });

    mainWindow.loadFile(path.join(__dirname, '..', 'index.html'));

    const version = getAppVersion();

    const menuTemplate = [
        {
            label: 'File',
            submenu: [
                {
                    label: 'Save as .py',
                    accelerator: 'CmdOrCtrl+D',
                    click: () => mainWindow.webContents.send('menu-save-py'),
                },
                {
                    label: 'Open .py',
                    accelerator: 'CmdOrCtrl+O',
                    click: async () => {
                        const result = await dialog.showOpenDialog(mainWindow, {
                            filters: [{ name: 'Python Files', extensions: ['py'] }],
                            properties: ['openFile'],
                        });
                        if (!result.canceled && result.filePaths[0]) {
                            const content = fs.readFileSync(result.filePaths[0], 'utf-8');
                            mainWindow.webContents.send('file-opened', {
                                path: result.filePaths[0],
                                content,
                            });
                        }
                    },
                },
                { type: 'separator' },
                {
                    label: 'Export Workspace',
                    accelerator: 'CmdOrCtrl+Shift+S',
                    click: () => mainWindow.webContents.send('menu-export'),
                },
                {
                    label: 'Import Workspace',
                    click: () => mainWindow.webContents.send('menu-import'),
                },
                { type: 'separator' },
                {
                    label: 'Enter License Key…',
                    click: async () => {
                        const { response, checkboxChecked } = await dialog.showMessageBox(mainWindow, {
                            type: 'question',
                            buttons: ['Enter Key', 'Cancel'],
                            defaultId: 0,
                            cancelId: 1,
                            title: 'PyMason License',
                            message: 'Activate desktop license',
                            detail:
                                'Format: PM-XXXX-XXXX-XXXX\nStored locally in app user data. Full Gumroad validation can plug into this path later.',
                        });
                        if (response !== 0) return;
                        // Electron has no built-in prompt; use a simple input via dialog workaround
                        const promptWin = new BrowserWindow({
                            width: 420,
                            height: 160,
                            parent: mainWindow,
                            modal: true,
                            show: true,
                            resizable: false,
                            webPreferences: { nodeIntegration: true, contextIsolation: false },
                        });
                        promptWin.setMenu(null);
                        promptWin.loadURL(
                            'data:text/html,' +
                                encodeURIComponent(`<!DOCTYPE html><html><body style="font-family:sans-serif;padding:16px;background:#000;color:#0f0;">
<label>License key<br><input id="k" style="width:100%;padding:8px;margin:8px 0;" placeholder="PM-XXXX-XXXX-XXXX"></label>
<button id="ok">Activate</button>
<script>
document.getElementById('ok').onclick=()=>{
  const {ipcRenderer}=require('electron');
  ipcRenderer.send('license-key-entered', document.getElementById('k').value);
};
</script></body></html>`)
                        );
                    },
                },
                { type: 'separator' },
                { role: 'quit' },
            ],
        },
        {
            label: 'Edit',
            submenu: [
                { role: 'undo' },
                { role: 'redo' },
                { type: 'separator' },
                { role: 'cut' },
                { role: 'copy' },
                { role: 'paste' },
                { role: 'selectAll' },
            ],
        },
        {
            label: 'Run',
            submenu: [
                {
                    label: 'Run Code',
                    accelerator: 'CmdOrCtrl+Enter',
                    click: () => mainWindow.webContents.send('menu-run'),
                },
                {
                    label: 'Stop',
                    click: () => mainWindow.webContents.send('menu-stop'),
                },
            ],
        },
        {
            label: 'View',
            submenu: [
                { role: 'reload' },
                { role: 'toggleDevTools' },
                { type: 'separator' },
                { role: 'zoomIn' },
                { role: 'zoomOut' },
                { role: 'resetZoom' },
                { type: 'separator' },
                { role: 'togglefullscreen' },
            ],
        },
        {
            label: 'Help',
            submenu: [
                {
                    label: 'About PyMason',
                    click: () => {
                        const lic = readLicense();
                        dialog.showMessageBox(mainWindow, {
                            type: 'info',
                            title: 'About PyMason',
                            message: 'PyMason v' + version,
                            detail:
                                'Building Code. Logically.\n\nA visual, block-based Python coding platform.\n\n' +
                                '© 2026 Wizard Productions AI Studio. All Rights Reserved.\n\n' +
                                (lic?.key
                                    ? 'License: ' + lic.key + '\nActivated: ' + lic.activatedAt
                                    : 'License: not activated (optional)'),
                        });
                    },
                },
            ],
        },
    ];

    Menu.setApplicationMenu(Menu.buildFromTemplate(menuTemplate));
}

ipcMain.handle('save-py-file', async (event, { content, defaultName }) => {
    const result = await dialog.showSaveDialog(mainWindow, {
        defaultPath: defaultName || 'program.py',
        filters: [{ name: 'Python Files', extensions: ['py'] }],
    });
    if (!result.canceled && result.filePath) {
        fs.writeFileSync(result.filePath, content, 'utf-8');
        return { success: true, path: result.filePath };
    }
    return { success: false };
});

ipcMain.on('license-key-entered', (event, key) => {
    const win = BrowserWindow.fromWebContents(event.sender);
    if (isValidLicenseKey(key)) {
        saveLicense(key);
        dialog.showMessageBox(mainWindow, {
            type: 'info',
            title: 'License',
            message: 'License activated',
            detail: 'Key stored locally: ' + key.trim().toUpperCase(),
        });
    } else {
        dialog.showMessageBox(mainWindow, {
            type: 'warning',
            title: 'License',
            message: 'Invalid key format',
            detail: 'Expected PM-XXXX-XXXX-XXXX',
        });
    }
    if (win && !win.isDestroyed()) win.close();
});

app.whenReady().then(() => {
    createWindow();
    try {
        createTray();
    } catch (e) {
        console.warn('Tray unavailable:', e.message);
    }
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
});
