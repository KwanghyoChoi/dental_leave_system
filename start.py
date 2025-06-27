#!/usr/bin/env python3
"""
안전한 시작 스크립트
"""
import sys
import os
import subprocess

def check_packages():
    """필요한 패키지 체크 및 설치"""
    required_packages = [
        'customtkinter',
        'Pillow', 
        'tkcalendar',
        'bcrypt',
        'python-dateutil'
    ]
    
    missing_packages = []
    
    print("필요한 패키지를 확인하는 중...")
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package}: 설치됨")
        except ImportError:
            print(f"❌ {package}: 설치되지 않음")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n누락된 패키지: {', '.join(missing_packages)}")
        
        install = input("지금 설치하시겠습니까? (y/n): ").lower()
        if install == 'y':
            for package in missing_packages:
                print(f"\n{package} 설치 중...")
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                    print(f"✓ {package} 설치 완료")
                except subprocess.CalledProcessError as e:
                    print(f"❌ {package} 설치 실패: {e}")
                    return False
        else:
            print("패키지 설치가 필요합니다.")
            return False
    
    return True

def test_database():
    """데이터베이스 테스트"""
    try:
        # src 폴더로 경로 추가
        src_path = os.path.join(os.path.dirname(__file__), 'src')
        sys.path.insert(0, src_path)
        
        from models.database import Database
        
        print("\n데이터베이스를 테스트하는 중...")
        db = Database()
        employees = db.get_all_employees()
        print(f"✓ 데이터베이스 테스트 성공 (직원 {len(employees)}명)")
        return True
        
    except Exception as e:
        print(f"❌ 데이터베이스 테스트 실패: {e}")
        return False

def start_application():
    """애플리케이션 시작"""
    try:
        # src 폴더로 이동
        src_path = os.path.join(os.path.dirname(__file__), 'src')
        os.chdir(src_path)
        
        print("\n치과 연차관리 시스템을 시작합니다...")
        
        # main.py 실행
        import main
        
    except KeyboardInterrupt:
        print("\n프로그램이 사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 프로그램 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        input("\nEnter를 눌러 종료...")

def main():
    print("=" * 60)
    print("치과 연차관리 시스템 - 안전 시작 도구")
    print("=" * 60)
    
    # 1단계: 패키지 체크
    if not check_packages():
        print("\n패키지 설치를 완료한 후 다시 실행해주세요.")
        input("Enter를 눌러 종료...")
        return
    
    # 2단계: 데이터베이스 테스트
    if not test_database():
        print("\n데이터베이스 문제를 해결한 후 다시 실행해주세요.")
        input("Enter를 눌러 종료...")
        return
    
    # 3단계: 애플리케이션 시작
    start_application()

if __name__ == "__main__":
    main()