@echo off
title 치과 연차관리 시스템 - 단계별 디버그
echo ============================================================
echo 치과 연차관리 시스템 - 단계별 디버그
echo ============================================================
echo.

cd /d "%~dp0"

echo [1단계] 전체 환경 체크...
python debug.py
if errorlevel 1 (
    echo ❌ 환경 체크 실패
    pause
    exit /b 1
)
echo ✓ 환경 체크 통과
echo.

echo [2단계] 데이터베이스 단독 테스트...
python test_db.py
if errorlevel 1 (
    echo ❌ 데이터베이스 테스트 실패
    pause
    exit /b 1
)
echo ✓ 데이터베이스 테스트 통과
echo.

echo [3단계] main.py 단계별 테스트...
cd src
python test_main_step.py
if errorlevel 1 (
    echo ❌ main.py 단계별 테스트 실패
    pause
    exit /b 1
)
echo ✓ main.py 단계별 테스트 통과
echo.

echo [4단계] 최소 앱 테스트...
python minimal_main.py
if errorlevel 1 (
    echo ❌ 최소 앱 테스트 실패
    pause
    exit /b 1
)
echo ✓ 최소 앱 테스트 통과
echo.

echo [5단계] 안전 모드 앱 테스트...
python main_safe.py
if errorlevel 1 (
    echo ❌ 안전 모드 앱 테스트 실패
    pause
    exit /b 1
)
echo ✓ 안전 모드 앱 테스트 통과
echo.

echo [최종단계] 정식 앱 실행...
python main.py
if errorlevel 1 (
    echo ❌ 정식 앱 실행 실패
    echo 안전 모드를 사용하세요: python main_safe.py
    pause
    exit /b 1
)

echo.
echo ============================================================
echo 🎉 모든 테스트 완료! 프로그램이 정상 작동합니다.
echo ============================================================
pause