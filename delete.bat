@echo off
SETLOCAL

REM Get the directory of the batch script
SET "SCRIPT_DIR=%~dp0"

REM Define Input, Output, and Archive directories relative to the script directory
SET "INPUT_DIR=%SCRIPT_DIR%Input"
SET "OUTPUT_DIR=%SCRIPT_DIR%Output"
SET "ARCHIVE_DIR=%SCRIPT_DIR%Archive"

ECHO.
ECHO ================================================================
ECHO                         ACTION CONFIRMATION
ECHO ================================================================
ECHO This script will:
ECHO   1. CREATE the folder "%ARCHIVE_DIR%" if it doesn't exist.
ECHO   2. MOVE all .dxf files from "%INPUT_DIR%" to "%ARCHIVE_DIR%".
ECHO   3. MOVE all .dxf files from "%OUTPUT_DIR%" to "%ARCHIVE_DIR%".
ECHO.
ECHO This effectively CLEANS the Input and Output folders of .dxf files
ECHO by archiving them. You can manually manage/delete files from
ECHO the Archive folder later if you wish.
ECHO.
ECHO   --- IMPORTANT ---
ECHO   Press ENTER to continue with the actions listed above.
ECHO   To CANCEL, simply CLOSE this command window now.
ECHO ================================================================
ECHO.

REM MODIFIED LINE: Escaped parentheses in the prompt string
set /p "CONFIRM_ACTION=Waiting for Enter key to proceed ^(or close window to cancel^)... "

REM If the script reaches here, Enter was pressed or input was provided.
REM If the window was closed, the script would have terminated.

ECHO.
ECHO Proceeding with archiving and cleaning...
ECHO.

REM --- Create Archive Directory ---
IF NOT EXIST "%ARCHIVE_DIR%" (
    ECHO Creating Archive directory: "%ARCHIVE_DIR%"
    MKDIR "%ARCHIVE_DIR%"
    IF ERRORLEVEL 1 (
        ECHO   ERROR: Could not create Archive directory. Please check permissions.
        ECHO   Operation aborted.
        pause & REM Pause here so user sees the critical error
        EXIT /B 1
    ) ELSE (
        ECHO   Archive directory created successfully.
    )
) ELSE (
    ECHO Archive directory "%ARCHIVE_DIR%" already exists.
)
ECHO.

REM --- Archive from Input folder ---
ECHO Archiving .dxf files from Input folder: "%INPUT_DIR%"
IF EXIST "%INPUT_DIR%" (
    IF EXIST "%INPUT_DIR%\*.dxf" (
        ECHO   Moving .dxf files to "%ARCHIVE_DIR%"...
        MOVE /Y "%INPUT_DIR%\*.dxf" "%ARCHIVE_DIR%\" >NUL
        IF ERRORLEVEL 1 (
            ECHO     WARNING: One or more .dxf files from Input folder might not have been moved.
            ECHO     This could be due to files being in use or permission issues.
            ECHO     Please manually check "%INPUT_DIR%" and "%ARCHIVE_DIR%".
        ) ELSE (
            ECHO     Successfully moved .dxf files from Input folder to Archive.
        )
    ) ELSE (
        ECHO   No .dxf files found in Input folder to archive.
    )
) ELSE (
    ECHO   Input folder "%INPUT_DIR%" does not exist. Skipping.
)
ECHO.

REM --- Archive from Output folder ---
ECHO Archiving .dxf files from Output folder: "%OUTPUT_DIR%"
IF EXIST "%OUTPUT_DIR%" (
    IF EXIST "%OUTPUT_DIR%\*.dxf" (
        ECHO   Moving .dxf files to "%ARCHIVE_DIR%"...
        MOVE /Y "%OUTPUT_DIR%\*.dxf" "%ARCHIVE_DIR%\" >NUL
        IF ERRORLEVEL 1 (
            ECHO     WARNING: One or more .dxf files from Output folder might not have been moved.
            ECHO     This could be due to files being in use or permission issues.
            ECHO     Please manually check "%OUTPUT_DIR%" and "%ARCHIVE_DIR%".
        ) ELSE (
            ECHO     Successfully moved .dxf files from Output folder to Archive.
        )
    ) ELSE (
        ECHO   No .dxf files found in Output folder to archive.
    )
) ELSE (
    ECHO   Output folder "%OUTPUT_DIR%" does not exist. Skipping.
)
ECHO.

ECHO Archiving and cleaning process finished.
ECHO The window will close automatically.

REM No pause here, window will close upon script completion.
ENDLOCAL
EXIT /B 0