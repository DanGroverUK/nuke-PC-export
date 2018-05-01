@echo off
echo "Copying Files to London Current Tools Dir"
robocopy "C:\git\nuke-PC-export" "\\files.taylorjames.com\Library$\Nuke\python" *.py
