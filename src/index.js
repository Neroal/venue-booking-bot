const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
const { execFile } = require("child_process");

function createWindow() {
    const win = new BrowserWindow({
        width: 700,
        height: 700,
        webPreferences: {
            preload: path.join(__dirname, "preload.js"),
            contextIsolation: true,
            enableRemoteModule: false,
        },
        icon: path.join(__dirname, "logo.icns"),
    });

    win.loadFile("src/index.html");
    // win.webContents.openDevTools();
}

app.whenReady().then(() => {
    createWindow();

    // On OS X it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    app.on("activate", () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on("window-all-closed", function () {
    if (process.platform !== "darwin") app.quit();
});

ipcMain.on("run-python", (event, args) => {
    const { account, password, timeSlot, d2 } = args;
    console.log("args:", account, password, timeSlot, d2);

    const executeFilePath = path.join(__dirname, "../dist/main");
    execFile(executeFilePath, [
        "--account",
        account,
        "--password",
        password,
        "--time_slot",
        timeSlot,
        "--d2",
        d2,
    ]);

    process.on("close", (code) => {
        event.reply("python-output", `Process closed with code ${code}`);
    });
});
