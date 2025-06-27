@echo off
title 디스플레이 문제 해결

echo ============================================================
echo          Windows 디스플레이 설정 문제 해결
echo ============================================================
echo.

:: DPI 인식 비활성화 (높은 DPI 설정에서 문제가 있을 수 있음)
echo 고DPI 설정 관련 환경변수 설정 중...
set QT_AUTO_SCREEN_SCALE_FACTOR=0
set QT_SCALE_FACTOR=1

:: Windows 디스플레이 스케일링 문제 해결
echo 디스플레이 스케일링 설정 중...
set GDK_SCALE=1
set GDK_DPI_SCALE=1

:: Python 경로 찾기
set PYTHON_CMD=
where python >nul 2>&1 && set PYTHON_CMD=python
if "%PYTHON_CMD%"=="" where python3 >nul 2>&1 && set PYTHON_CMD=python3
if "%PYTHON_CMD%"=="" where py >nul 2>&1 && set PYTHON_CMD=py

if "%PYTHON_CMD%"=="" (
    echo ❌ Python을 찾을 수 없습니다!
    pause
    exit /b 1
)

echo.
echo 다음 테스트를 실행합니다:
echo.

echo [1] 간단한 GUI 테스트...
cd src
%PYTHON_CMD% test_gui_simple.py

echo.
echo [2] 메인 프로그램 실행...
%PYTHON_CMD% main.py

cd ..
pause