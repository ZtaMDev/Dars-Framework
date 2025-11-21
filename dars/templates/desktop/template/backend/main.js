const { app, BrowserWindow, Menu, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs').promises;
const http = require('http');

function createWindow() {
  const win = new BrowserWindow({
    width: 1000, height: 700,
    webPreferences: {
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });
  Menu.setApplicationMenu(null);
  win.loadFile(path.join(__dirname, 'app', 'index.html'));
  // Open DevTools in development mode if enabled
  if (process.env.DARS_DEV === '1' && process.env.DARS_DEVTOOLS !== '0') {
    win.webContents.openDevTools();
  }
}

app.whenReady().then(() => {
  createWindow();
  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

// Utility to resolve paths: absolute paths are used as-is; relative paths resolve against process.cwd()
function resolvePath(p) {
  if (!p || typeof p !== 'string') throw new Error('filePath must be a string');
  if (path.isAbsolute(p)) return p;
  return path.resolve(process.cwd(), p);
}

function closeAllAndExit() {
  try {
    const wins = BrowserWindow.getAllWindows();
    wins.forEach(w => { try { w.close(); } catch (e) { } });
  } catch (e) { }
  setTimeout(() => { try { app.quit(); } catch (e) { } }, 300);
}

ipcMain.handle('dars::dev::shutdown', async () => {
  closeAllAndExit();
  return true;
});

const controlPort = process.env.DARS_CONTROL_PORT;
if (controlPort) {
  try {
    const server = http.createServer((req, res) => {
      if (req.method === 'POST' && req.url === '/__dars_shutdown') {
        closeAllAndExit();
        res.writeHead(200); res.end('ok');
        return;
      }
      res.writeHead(404); res.end('not-found');
    });
    server.listen(Number(controlPort), '127.0.0.1');
  } catch (e) { /* ignore */ }
}

// IPC handlers for Dars desktop API
ipcMain.handle('dars::FileSystem::read_text', async (_e, filePath, encoding = 'utf-8') => {
  const resolved = resolvePath(filePath);
  const content = await fs.readFile(resolved, { encoding });
  return content;
});

ipcMain.handle('dars::FileSystem::write_text', async (_e, filePath, data, encoding = 'utf-8') => {
  const resolved = resolvePath(filePath);
  if (typeof data !== 'string') data = String(data ?? '');
  await fs.mkdir(path.dirname(resolved), { recursive: true });
  await fs.writeFile(resolved, data, { encoding });
  return true;
});

ipcMain.handle('dars::FileSystem::read_file', async (_e, filePath) => {
  const resolved = resolvePath(filePath);
  try {
    const data = await fs.readFile(resolved);
    // Convert to array for JSON serialization
    return { data: Array.from(data) };
  } catch (error) {
    console.error('Error reading file:', error);
    throw error;
  }
});

ipcMain.handle('dars::FileSystem::write_file', async (_e, filePath, data) => {
  const resolved = resolvePath(filePath);
  try {
    await fs.mkdir(path.dirname(resolved), { recursive: true });
    await fs.writeFile(resolved, Buffer.from(data));
    return true;
  } catch (error) {
    console.error('Error writing file:', error);
    throw error;
  }
});

ipcMain.handle('dars::FileSystem::list_directory', async (_e, dirPath, pattern = '*', includeSize = false) => {
  const resolved = resolvePath(dirPath);
  try {
    const entries = await fs.readdir(resolved, { withFileTypes: true });
    const result = [];
    for (const entry of entries) {
      // Simple pattern matching (supports * wildcard)
      if (pattern !== '*') {
        const regex = new RegExp('^' + pattern.replace(/\*/g, '.*') + '$');
        if (!regex.test(entry.name)) continue;
      }
      const obj = {
        name: entry.name,
        isDirectory: entry.isDirectory()
      };
      if (includeSize) {
        const stats = await fs.stat(path.join(resolved, entry.name));
        obj.size = stats.size;
      }
      result.push(obj);
    }
    return result;
  } catch (error) {
    console.error('Error listing directory:', error);
    throw error;
  }
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});
