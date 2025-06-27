#!/usr/bin/env python3
"""
최소한의 main.py - 문제 찾기용
"""
import sys
import os

def step1_test_basic_imports():
    """1단계: 기본 import 테스트"""
    print("[1단계] 기본 import 테스트...")
    try:
        import customtkinter as ctk
        print("✓ customtkinter")
        return ctk
    except Exception as e:
        print(f"❌ customtkinter 실패: {e}")
        raise

def step2_test_utils():
    """2단계: utils 모듈 테스트"""
    print("[2단계] utils 모듈 테스트...")
    try:
        from utils.session import Session
        print("✓ Session")
        
        from utils.theme import Theme
        print("✓ Theme")
        
        return Session, Theme
    except Exception as e:
        print(f"❌ utils 모듈 실패: {e}")
        raise

def step3_test_models():
    """3단계: models 모듈 테스트"""
    print("[3단계] models 모듈 테스트...")
    try:
        from models.database import Database
        print("✓ Database")
        
        db = Database()
        print("✓ Database 초기화")
        
        return Database
    except Exception as e:
        print(f"❌ models 모듈 실패: {e}")
        raise

def step4_test_login_view():
    """4단계: LoginView 테스트"""
    print("[4단계] LoginView 테스트...")
    try:
        from views.login_view import LoginView
        print("✓ LoginView import")
        return LoginView
    except Exception as e:
        print(f"❌ LoginView 실패: {e}")
        import traceback
        traceback.print_exc()
        raise

def step5_test_simple_app():
    """5단계: 간단한 앱 테스트"""
    print("[5단계] 간단한 앱 테스트...")
    try:
        ctk, (Session, Theme), Database, LoginView = step1_test_basic_imports(), step2_test_utils(), step3_test_models(), step4_test_login_view()
        
        print("간단한 앱 생성 중...")
        
        class MinimalApp(ctk.CTk):
            def __init__(self):
                super().__init__()
                self.title("최소 테스트 앱")
                self.geometry("800x600")
                
                # 간단한 로그인 화면만
                self.setup_simple_ui()
            
            def setup_simple_ui(self):
                frame = ctk.CTkFrame(self)
                frame.pack(fill="both", expand=True, padx=20, pady=20)
                
                label = ctk.CTkLabel(frame, text="치과 연차관리 시스템", 
                                   font=ctk.CTkFont(size=24, weight="bold"))
                label.pack(pady=50)
                
                button = ctk.CTkButton(frame, text="테스트 성공!", 
                                     command=self.quit, width=200, height=50)
                button.pack(pady=20)
                
                close_btn = ctk.CTkButton(frame, text="5초 후 자동 종료", 
                                        command=self.start_timer, width=200, height=30)
                close_btn.pack(pady=10)
                
            def start_timer(self):
                self.after(5000, self.quit)
        
        app = MinimalApp()
        print("✓ 앱 생성 성공")
        
        print("앱 실행 중... (창을 닫거나 5초 후 자동 종료)")
        app.mainloop()
        print("✓ 앱 정상 종료")
        
        return True
        
    except Exception as e:
        print(f"❌ 간단한 앱 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("최소한의 main.py 테스트")
    print("=" * 60)
    
    try:
        if step5_test_simple_app():
            print("\n🎉 최소 테스트 성공! 이제 전체 앱을 시도해보세요.")
            print("\n다음을 실행하세요:")
            print("  python main_safe.py")
        else:
            print("\n❌ 최소 테스트 실패")
    
    except Exception as e:
        print(f"\n❌ 테스트 중 오류: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nEnter를 눌러 종료...")

if __name__ == "__main__":
    main()