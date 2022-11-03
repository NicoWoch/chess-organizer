rem Compiling With Pyinstaller
mkdir dist
pyinstaller --noconfirm ^
             --onedir ^
             --windowed ^
             --icon ./images/logo.ico ^
             ./chess-organizer.py


rem Coping Essential Data
robocopy images dist\chess-organizer\images
copy license.md dist\chess-organizer
mkdir dist\chess-organizer\logs
mkdir dist\chess-organizer\db


rem Making Installator With InnoSetup
"C:\Program Files (x86)\Inno Setup 6\iscc" /OC:\Users\48502\PycharmProjects\chess-organizer-desktop C:\Users\48502\PycharmProjects\chess-organizer-desktop\installer-setup.iss


rem Zipping To Archive
cd dist/chess-organizer
7z a ../../chess-organizer.zip *
cd ../..


rem Cleaning
rmdir /S /Q build
rmdir /S /Q dist
rmdir /S /Q output
mkdir output
move chess-organizer.zip output
move chess-organizer-installer.exe output


echo Building Done
