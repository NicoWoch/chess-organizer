set APP_VERSION = "0.4"


@REM Cleaning Develop Temporary Files And Logs
del /Q data\temp\*
del /Q data\logs\*


@REM Removing old output folder
rmdir /S /Q output


@REM Compiling With Pyinstaller
pyinstaller --noconfirm ^
             --onedir ^
             --windowed ^
             --icon data\images\logo.ico ^
             chess-organizer.py


@REM Adding Essential Data
robocopy /e data dist\chess-organizer\data\
del /Q dist\chess-organizer\data\db\*
copy license.md dist\chess-organizer\


@REM Zipping To Archive
mkdir output
cd dist/chess-organizer
7z a ../../output/chess-organizer.zip *
cd ../..


@REM Making Installator With InnoSetup
"C:\Program Files (x86)\Inno Setup 6\iscc" /DMyAppVersion=%APP_VERSION% ^
                                           /OC:\Users\48502\PycharmProjects\chess-organizer-desktop\output ^
                                           C:\Users\48502\PycharmProjects\chess-organizer-desktop\installer-setup.iss


@REM Cleaning
rmdir /S /Q build
rmdir /S /Q dist
del chess-organizer.spec


echo Building Done
