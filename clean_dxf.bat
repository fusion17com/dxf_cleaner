@echo off
REM Get the directory of the batch script
SET "SCRIPT_DIR=%~dp0"

REM Define Input and Output directories relative to the script directory
SET "INPUT_DIR=%SCRIPT_DIR%Input"
SET "OUTPUT_DIR=%SCRIPT_DIR%Output"
SET "PYTHON_SCRIPT=%SCRIPT_DIR%dxf_cleaner.py"

REM --- Sanity Checks ---
IF NOT EXIST "%PYTHON_SCRIPT%" (
    echo Error: Python script clean_main.py not found at:
    echo %PYTHON_SCRIPT%
    echo Please ensure dxf_cleaner.py is in the same directory as Launch.bat.
    pause
    exit /b 1
)

IF NOT EXIST "%INPUT_DIR%" (
    echo Error: Input directory not found at:
    echo %INPUT_DIR%
    echo Please create an 'Input' subfolder and place your DXF files there.
    pause
    exit /b 1
)

REM --- Prepare Output Directory ---
IF NOT EXIST "%OUTPUT_DIR%" (
    echo Creating output directory: %OUTPUT_DIR%
    mkdir "%OUTPUT_DIR%"
    IF ERRORLEVEL 1 (
        echo Error: Could not create output directory. Check permissions.
        pause
        exit /b 1
    )
)

echo Starting DXF cleaning process...
echo Input directory:  %INPUT_DIR%
echo Output directory: %OUTPUT_DIR%
echo Python script:    %PYTHON_SCRIPT%
echo.

REM --- Process Files ---
SET "FILES_FOUND=0"
FOR %%F IN ("%INPUT_DIR%\*.dxf") DO (
    SET "FILES_FOUND=1"
    echo Processing file: "%%~nxF"
    REM Call the python script, passing the full path to the input DXF file.
    REM The python script will handle saving to the Output directory.
    python "%PYTHON_SCRIPT%" "%%F"
    echo -----------------------------------
    echo.
)

IF "%FILES_FOUND%"=="0" (
    echo No .dxf files found in %INPUT_DIR%
)

echo.
echo All DXF files processed.
pause