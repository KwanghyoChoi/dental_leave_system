#!/usr/bin/env python3
"""
main.py를 단계별로 테스트
"""
import sys
import os

print("=== main.py 단계별 테스트 ===")

# 1단계: 기본 import 테스트
print("\n[1단계] 기본 모듈 import 테스트...")
try:
    import customtkinter as ctk
    print("✓ customtkinter import 성공")
except Exception as e:
    print(f"❌ customtkinter import 실패: {e}")
    input("Enter를 눌러 종료...")
    sys.exit(1)

# 2단계: 프로젝트 모듈 import 테스트
print("\n[2단계] 프로젝트 모듈 import 테스트...")
try:
    from views.login_view import LoginView
    print("✓ LoginView import 성공")
except Exception as e:
    print(f"❌ LoginView import 실패: {e}")
    import traceback
    traceback.print_exc()
    input("Enter를 눌러 종료...")
    sys.exit(1)

try:
    from views.main_view import MainView
    print("✓ MainView import 성공")
except Exception as e:
    print(f"❌ MainView import 실패: {e}")
    import traceback
    traceback.print_exc()
    input("Enter를 눌러 종료...")
    sys.exit(1)

# 3단계: 앱 클래스 생성 테스트
print("\n[3단계] 앱 클래스 정의 테스트...")
try:
    class TestApp(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.title("테스트")
            self.geometry("400x300")
            print("✓ 기본 앱 클래스 생성 성공")
    print("✓ 앱 클래스 정의 성공")
except Exception as e:
    print(f"❌ 앱 클래스 정의 실패: {e}")
    import traceback
    traceback.print_exc()
    input("Enter를 눌러 종료...")
    sys.exit(1)

# 4단계: 실제 DentalLeaveApp 클래스 테스트
print("\n[4단계] DentalLeaveApp 클래스 테스트...")
try:
    class DentalLeaveApp(ctk.CTk):
        def __init__(self):
            print("  DentalLeaveApp 초기화 시작...")
            super().__init__()
            print("  부모 클래스 초기화 완료")
            
            self.title("치과 연차관리 시스템")
            print("  제목 설정 완료")
            
            self.geometry("1500x950")
            print("  창 크기 설정 완료")
            
            self.minsize(1300, 850)
            print("  최소 크기 설정 완료")
            
            ctk.set_appearance_mode("light")
            ctk.set_default_color_theme("blue")
            print("  테마 설정 완료")
            
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)
            print("  그리드 설정 완료")
            
            print("  로그인 화면 표시 시작...")
            self.show_login()
            print("  로그인 화면 표시 완료")
            
        def show_login(self):
            try:
                print("    LoginView 생성 시작...")
                if hasattr(self, 'current_view'):
                    self.current_view.destroy()
                
                self.current_view = LoginView(self, self.show_main)
                print("    LoginView 생성 완료")
                
                self.current_view.grid(row=0, column=0, sticky="nsew")
                print("    LoginView 배치 완료")
            except Exception as e:
                print(f"    ❌ show_login 오류: {e}")
                import traceback
                traceback.print_exc()
                raise
                
        def show_main(self):
            print("    MainView로 전환...")
            
    print("✓ DentalLeaveApp 클래스 정의 성공")
except Exception as e:
    print(f"❌ DentalLeaveApp 클래스 정의 실패: {e}")
    import traceback
    traceback.print_exc()
    input("Enter를 눌러 종료...")
    sys.exit(1)

# 5단계: 앱 인스턴스 생성 테스트
print("\n[5단계] 앱 인스턴스 생성 테스트...")
try:
    print("앱 인스턴스 생성 중...")
    app = DentalLeaveApp()
    print("✓ 앱 인스턴스 생성 성공")
    
    print("3초 후 자동 종료...")
    app.after(3000, app.quit)
    
    print("메인루프 시작...")
    app.mainloop()
    
    print("앱 종료 중...")
    app.destroy()
    print("✓ 앱 정상 종료")
    
except Exception as e:
    print(f"❌ 앱 실행 실패: {e}")
    import traceback
    traceback.print_exc()
    input("Enter를 눌러 종료...")
    sys.exit(1)

print("\n🎉 모든 단계 테스트 통과!")
print("main.py가 정상적으로 실행될 수 있습니다.")
input("Enter를 눌러 종료...")