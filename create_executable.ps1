python -m PyInstaller `
app.py `
--onefile `
--windowed `
--noconsole `
--clean `
--add-data "assets/icon.gif;./assets/" `
--icon=assets/icon.ico