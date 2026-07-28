const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('pymasonElectron', {
    // File operations
    savePyFile: (content, defaultName) =>
        ipcRenderer.invoke('save-py-file', { content, defaultName }),

    // Menu event listeners
    onMenuSavePy: (callback) => ipcRenderer.on('menu-save-py', callback),
    onMenuExport: (callback) => ipcRenderer.on('menu-export', callback),
    onMenuImport: (callback) => ipcRenderer.on('menu-import', callback),
    onMenuRun: (callback) => ipcRenderer.on('menu-run', callback),
    onMenuStop: (callback) => ipcRenderer.on('menu-stop', callback),
    onFileOpened: (callback) => ipcRenderer.on('file-opened', (_, data) => callback(data)),

    // License (Gumroad optional online verify via main process)
    verifyLicense: (key) => ipcRenderer.invoke('pymason-verify-license', key),
    getLicense: () => ipcRenderer.invoke('pymason-get-license'),

    // Detect Electron
    isElectron: true,
});
