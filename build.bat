set APP_VERSION=V0.3


rem Compiling

pyinstaller --noconfirm ^
             --onedir ^
             --windowed ^
             --icon ./images/logo.ico ^
             ./chess-organizer.py

robocopy images dist\chess-organizer\images
copy license.md dist\chess-organizer

mkdir dist\chess-organizer\logs
echo . > dist\chess-organizer\logs\empty.txt

mkdir dist\chess-organizer\db
echo . > dist\chess-organizer\db\empty.txt


rem Cleaning

rmdir /S /Q build
rmdir /S /Q dist\chess-organizer-%APP_VERSION%
rename dist\chess-organizer chess-organizer-%APP_VERSION%


echo COMPILED SUCCESSFUL
