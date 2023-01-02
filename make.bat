@echo on
set PY_FILE=chants_ie.py
set PROJECT_NAME=Chants IE
set VERSION=1.0.0
set FILE_VERSION=file_version_info.txt
set ICO_DIR=pes_indie.ico

pyinstaller --onefile --window "%PY_FILE%" --icon="%ICO_DIR%" --name "%PROJECT_NAME%_%VERSION%" --version-file "%FILE_VERSION%"

cd dist
tar -acvf "%PROJECT_NAME%_%VERSION%.zip" * config
pause
