@echo off
setlocal enabledelayedexpansion

title 치과 연차관리 시스템

echo ============================================================
echo              치과 연차관리 시스템 실행
echo ============================================================
echo.

:: 현재 디렉토리를 스크립트 위치로 변경
cd /d "%~dp0"

:: Python 경로 자동 찾기
echo Python 실행 파일을 찾는 중...
set PYTHON_CMD=

:: 1. python 명령어 시도
where python >nul 2>&1
if %errorlevel%==0 (
    set PYTHON_CMD=python
    goto :found_python
)

:: 2. python3 명령어 시도
where python3 >nul 2>&1
if %errorlevel%==0 (
    set PYTHON_CMD=python3
    goto :found_python
)

:: 3. py 명령어 시도 (Python Launcher)
where py >nul 2>&1
if %errorlevel%==0 (
    set PYTHON_CMD=py
    goto :found_python
)

:: Python을 찾지 못함
echo ❌ Python을 찾을 수 없습니다!
echo.
echo Python을 설치하세요: https://www.python.org/downloads/
echo.
pause
exit /b 1

:found_python
echo ✓ Python 찾음: %PYTHON_CMD%
echo.

:: Python 버전 확인
echo Python 버전 확인 중...
%PYTHON_CMD% --version
echo.

:: 필요한 패키지 확인
echo 필요한 패키지 확인 중...
%PYTHON_CMD% -m pip show customtkinter >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  customtkinter가 설치되지 않았습니다.
    echo.
    set /p INSTALL="패키지를 설치하시겠습니까? (Y/N): "
    if /i "!INSTALL!"=="Y" (
        echo.
        echo 패키지 설치 중...
        %PYTHON_CMD% -m pip install customtkinter openpyxl bcrypt tkcalendar Pillow
        echo.
    ) else (
        echo.
        echo 패키지 설치가 취소되었습니다.
        echo 수동으로 설치하세요: pip install customtkinter openpyxl bcrypt tkcalendar Pillow
        echo.
        pause
        exit /b 1
    )
)

:: 프로그램 실행
echo ============================================================
echo                  프로그램을 시작합니다
echo ============================================================
echo.

cd src
%PYTHON_CMD% main.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ 프로그램 실행 중 오류가 발생했습니다.
    echo.
    echo 디버그 모드로 실행해 보세요:
    echo   %PYTHON_CMD% main_safe.py
    echo.
    pause
)

endlocal