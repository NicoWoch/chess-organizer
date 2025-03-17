set APP_VERSION="1.1"


@REM Cleaning Develop Files
del data\fonts\Roboto.cw127.pkl
del data\fonts\Roboto.pkl


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
copy license.md dist\chess-organizer\


@REM Zipping To Archive
mkdir output
cd dist/chess-organizer
7z a ../../output/chess-organizer.zip *
cd ../..


@REM Making Installator With InnoSetup
"C:\Program Files (x86)\Inno Setup 6\iscc" /DMyRootDir=%cd% ^
                                           /DMyAppVersion=%APP_VERSION% ^
                                           /O%cd%\output ^
                                           %cd%\installer-setup.iss


@REM Cleaning
rmdir /S /Q build
rmdir /S /Q dist
del chess-organizer.spec


echo Building Done, output should be in ./output directory
