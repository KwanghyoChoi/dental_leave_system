#!/usr/bin/env python3
"""
디버그용 스크립트 - 문제 진단
"""
import sys
import os

def check_environment():
    """환경 체크"""
    print("=== 환경 체크 ===")
    print(f"Python 버전: {sys.version}")
    print(f"현재 디렉토리: {os.getcwd()}")
    print(f"스크립트 위치: {os.path.abspath(__file__)}")
    print()

def check_packages():
    """패키지 체크"""
    print("=== 패키지 체크 ===")
    required_packages = [
        'customtkinter',
        'sqlite3', 
        'bcrypt',
        'tkinter'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'tkinter':
                import tkinter
            else:
                __import__(package)
            print(f"✓ {package}: 설치됨")
        except ImportError as e:
            print(f"❌ {package}: 설치되지 않음 - {e}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n누락된 패키지: {', '.join(missing_packages)}")
        print("다음 명령어로 설치하세요:")
        for pkg in missing_packages:
            if pkg != 'tkinter' and pkg != 'sqlite3':
                print(f"  pip install {pkg}")
        
        if 'tkinter' in missing_packages:
            print("  tkinter는 Python과 함께 설치되어야 합니다.")
    else:
        print("\n모든 필수 패키지가 설치되어 있습니다!")
    
    print()
    return len(missing_packages) == 0

def check_files():
    """파일 구조 체크"""
    print("=== 파일 구조 체크 ===")
    
    # src 폴더로 이동
    src_dir = os.path.join(os.path.dirname(__file__), 'src')
    if os.path.exists(src_dir):
        os.chdir(src_dir)
        print(f"src 디렉토리로 이동: {os.getcwd()}")
    
    required_files = [
        'main.py',
        'models/database.py',
        'utils/session.py',
        'utils/theme.py',
        'views/login_view.py',
        'views/main_view.py'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}: 존재")
        else:
            print(f"❌ {file_path}: 없음")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n누락된 파일: {', '.join(missing_files)}")
    else:
        print("\n모든 필수 파일이 존재합니다!")
    
    print()
    return len(missing_files) == 0

def test_database():
    """데이터베이스 테스트"""
    print("=== 데이터베이스 테스트 ===")
    try:
        sys.path.append(os.getcwd())
        from models.database import Database
        
        print("데이터베이스 모듈 import 성공")
        
        db = Database()
        print("데이터베이스 초기화 성공")
        
        employees = db.get_all_employees()
        print(f"직원 {len(employees)}명 조회 성공")
        
        print("✓ 데이터베이스 테스트 통과")
        return True
        
    except Exception as e:
        print(f"❌ 데이터베이스 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """메인 함수"""
    print("치과 연차관리 시스템 - 디버그 도구\n")
    
    check_environment()
    
    packages_ok = check_packages()
    files_ok = check_files()
    
    if packages_ok and files_ok:
        db_ok = test_database()
        
        if db_ok:
            print("🎉 모든 테스트 통과! 프로그램을 실행할 수 있습니다.")
            print("\n다음 명령어로 실행하세요:")
            print("  cd src")
            print("  python main.py")
        else:
            print("❌ 데이터베이스 테스트 실패")
    else:
        print("❌ 필수 구성 요소가 누락되었습니다.")
    
    print("\n" + "="*50)
    input("Enter를 눌러 종료...")

if __name__ == "__main__":
    main()