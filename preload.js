const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
    ipcRenderer: {
        send: ipcRenderer.send,
        on: (channel, func) => {
            ipcRenderer.on(channel, (event, ...args) => func(...args));
        },
        once: ipcRenderer.once,
        removeListener: ipcRenderer.removeListener,
        removeAllListeners: ipcRenderer.removeAllListeners
    }
});