const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('DarsIPC', {
  invoke: (channel, ...args) => ipcRenderer.invoke(channel, ...args)
});
// Also expose a minimal DarsDesktopAPI for renderer convenience
contextBridge.exposeInMainWorld('DarsDesktopAPI', {
  FileSystem: {
    read_text: (...args) => ipcRenderer.invoke('dars::FileSystem::read_text', ...args),
    write_text: (...args) => ipcRenderer.invoke('dars::FileSystem::write_text', ...args),
    read_file: (...args) => ipcRenderer.invoke('dars::FileSystem::read_file', ...args),
    write_file: (...args) => ipcRenderer.invoke('dars::FileSystem::write_file', ...args)
  }
});
// Dev helpers: request graceful shutdown from Python dev launcher
contextBridge.exposeInMainWorld('DarsDev', {
  shutdown: () => ipcRenderer.invoke('dars::dev::shutdown')
});
