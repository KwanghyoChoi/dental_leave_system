#!/usr/bin/env python3
import sys
import os

# 경로 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """각 모듈을 하나씩 테스트"""
    try:
        print("1. customtkinter 테스트...")
        import customtkinter as ctk
        print("   ✓ customtkinter 성공")
        
        print("2. utils.theme 테스트...")
        from utils.theme import Theme
        print("   ✓ theme 성공")
        
        print("3. utils.session 테스트...")
        from utils.session import Session
        print("   ✓ session 성공")
        
        print("4. models.database 테스트...")
        from models.database import Database
        print("   ✓ database 성공")
        
        print("5. 데이터베이스 초기화 테스트...")
        db = Database()
        print("   ✓ 데이터베이스 초기화 성공")
        
        print("6. 직원 목록 조회 테스트...")
        employees = db.get_all_employees()
        print(f"   ✓ 직원 {len(employees)}명 조회 성공")
        
        print("7. views.login_view 테스트...")
        from views.login_view import LoginView
        print("   ✓ login_view 성공")
        
        print("8. views.main_view 테스트...")
        from views.main_view import MainView
        print("   ✓ main_view 성공")
        
        print("\n모든 import 테스트 통과!")
        return True
        
    except Exception as e:
        print(f"   ❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_app():
    """간단한 앱 테스트"""
    try:
        print("\n간단한 앱 테스트 시작...")
        import customtkinter as ctk
        
        app = ctk.CTk()
        app.title("테스트")
        app.geometry("400x300")
        
        label = ctk.CTkLabel(app, text="테스트 성공!")
        label.pack(pady=50)
        
        button = ctk.CTkButton(app, text="종료", command=app.quit)
        button.pack(pady=20)
        
        print("간단한 앱 생성 성공. 3초 후 자동 종료...")
        app.after(3000, app.quit)
        app.mainloop()
        app.destroy()
        
        print("✓ 간단한 앱 테스트 성공")
        return True
        
    except Exception as e:
        print(f"❌ 간단한 앱 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_full_app():
    """전체 앱 테스트"""
    try:
        print("\n전체 앱 테스트 시작...")
        from main import DentalLeaveApp
        
        app = DentalLeaveApp()
        print("앱 생성 성공. 5초 후 자동 종료...")
        app.after(5000, app.quit)
        app.mainloop()
        app.destroy()
        
        print("✓ 전체 앱 테스트 성공")
        return True
        
    except Exception as e:
        print(f"❌ 전체 앱 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== 치과 연차관리 시스템 디버그 테스트 ===\n")
    
    # 1단계: Import 테스트
    if not test_imports():
        print("\nImport 테스트 실패. 프로그램을 종료합니다.")
        input("Enter를 눌러 종료...")
        sys.exit(1)
    
    # 2단계: 간단한 앱 테스트
    if not test_simple_app():
        print("\n간단한 앱 테스트 실패. 프로그램을 종료합니다.")
        input("Enter를 눌러 종료...")
        sys.exit(1)
    
    # 3단계: 전체 앱 테스트
    if not test_full_app():
        print("\n전체 앱 테스트 실패.")
        input("Enter를 눌러 종료...")
        sys.exit(1)
    
    print("\n🎉 모든 테스트 통과! 프로그램이 정상적으로 작동합니다.")
    input("Enter를 눌러 종료...")