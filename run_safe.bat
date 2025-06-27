@echo off
title 치과 연차관리 시스템
echo ============================================================
echo 치과 연차관리 시스템 - 안전 시작 도구
echo ============================================================
echo.

cd /d "%~dp0"

echo [1단계] Python 환경 확인...
python --version
if errorlevel 1 (
    echo ❌ Python이 설치되지 않았거나 PATH에 없습니다.
    echo    Python 3.8 이상을 설치해주세요.
    pause
    exit /b 1
)
echo ✓ Python 설치 확인
echo.

echo [2단계] 데이터베이스 테스트...
python test_db.py
if errorlevel 1 (
    echo ❌ 데이터베이스 테스트 실패
    pause
    exit /b 1
)
echo ✓ 데이터베이스 테스트 통과
echo.

echo [3단계] 필요한 패키지 확인...
python -c "import customtkinter" 2>nul
if errorlevel 1 (
    echo ❌ customtkinter가 설치되지 않았습니다.
    echo 설치를 시작합니다...
    pip install customtkinter Pillow tkcalendar bcrypt python-dateutil
    if errorlevel 1 (
        echo ❌ 패키지 설치 실패
        pause
        exit /b 1
    )
)
echo ✓ 모든 패키지 설치 확인
echo.

echo [4단계] 프로그램 시작...
cd src
python main.py

echo.
echo ============================================================
echo 프로그램이 종료되었습니다.
echo ============================================================
pause