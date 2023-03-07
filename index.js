const { app, BrowserWindow } = require('electron')

app.disableHardwareAcceleration()


const createWindow = () => {

    const win = new BrowserWindow({
        width: 1200,
        height: 800
    })

    win.loadURL("http://localhost:8501/")
    win.removeMenu()

}

app.whenReady().then(createWindow)