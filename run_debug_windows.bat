@echo off
setlocal enabledelayedexpansion

title 치과 연차관리 시스템 - 디버그 모드

echo ============================================================
echo          치과 연차관리 시스템 - 디버그 모드
echo ============================================================
echo.

:: 현재 디렉토리를 스크립트 위치로 변경
cd /d "%~dp0"

:: Python 찾기
set PYTHON_CMD=
where python >nul 2>&1 && set PYTHON_CMD=python
if "!PYTHON_CMD!"=="" where python3 >nul 2>&1 && set PYTHON_CMD=python3
if "!PYTHON_CMD!"=="" where py >nul 2>&1 && set PYTHON_CMD=py

if "!PYTHON_CMD!"=="" (
    echo ❌ Python을 찾을 수 없습니다!
    pause
    exit /b 1
)

echo Python: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

:: 단계별 실행 선택
echo 실행할 테스트를 선택하세요:
echo.
echo [1] 전체 환경 체크 (debug.py)
echo [2] 데이터베이스 테스트 (test_db.py)
echo [3] Theme 모듈 테스트 (test_theme.py)
echo [4] main.py 단계별 테스트 (test_main_step.py)
echo [5] 최소 앱 테스트 (minimal_main.py)
echo [6] 안전 모드 실행 (main_safe.py)
echo [7] 정식 앱 실행 (main.py)
echo [8] 단계별 디버그 실행 (debug_step.bat)
echo [0] 종료
echo.

set /p CHOICE="선택 (0-8): "

if "%CHOICE%"=="0" exit /b 0

if "%CHOICE%"=="1" (
    echo.
    echo === 전체 환경 체크 ===
    %PYTHON_CMD% debug.py
) else if "%CHOICE%"=="2" (
    echo.
    echo === 데이터베이스 테스트 ===
    %PYTHON_CMD% test_db.py
) else if "%CHOICE%"=="3" (
    echo.
    echo === Theme 모듈 테스트 ===
    cd src
    %PYTHON_CMD% test_theme.py
    cd ..
) else if "%CHOICE%"=="4" (
    echo.
    echo === main.py 단계별 테스트 ===
    cd src
    %PYTHON_CMD% test_main_step.py
    cd ..
) else if "%CHOICE%"=="5" (
    echo.
    echo === 최소 앱 테스트 ===
    cd src
    %PYTHON_CMD% minimal_main.py
    cd ..
) else if "%CHOICE%"=="6" (
    echo.
    echo === 안전 모드 실행 ===
    cd src
    %PYTHON_CMD% main_safe.py
    cd ..
) else if "%CHOICE%"=="7" (
    echo.
    echo === 정식 앱 실행 ===
    cd src
    %PYTHON_CMD% main.py
    cd ..
) else if "%CHOICE%"=="8" (
    echo.
    echo === 단계별 디버그 실행 ===
    call debug_step.bat
) else (
    echo.
    echo ❌ 잘못된 선택입니다.
)

echo.
pause

:: 다시 메뉴로
goto :eof

endlocal