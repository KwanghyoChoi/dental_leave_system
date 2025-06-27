#!/usr/bin/env python3
"""
안전한 main.py - 더 많은 에러 처리
"""
import sys
import os

def safe_import():
    """안전한 import"""
    try:
        print("필수 모듈을 불러오는 중...")
        
        import customtkinter as ctk
        print("✓ customtkinter")
        
        from views.login_view import LoginView
        print("✓ LoginView")
        
        from views.main_view import MainView
        print("✓ MainView")
        
        return ctk, LoginView, MainView
        
    except ImportError as e:
        print(f"❌ 모듈 import 오류: {e}")
        print("\n해결 방법:")
        print("1. 필요한 패키지 설치: pip install customtkinter Pillow tkcalendar bcrypt")
        print("2. 올바른 디렉토리에서 실행: cd src")
        input("\nEnter를 눌러 종료...")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 예상치 못한 import 오류: {e}")
        import traceback
        traceback.print_exc()
        input("\nEnter를 눌러 종료...")
        sys.exit(1)

class SafeDentalLeaveApp:
    """안전한 치과 연차관리 앱"""
    
    def __init__(self, ctk, LoginView, MainView):
        self.ctk = ctk
        self.LoginView = LoginView
        self.MainView = MainView
        self.app = None
        self.current_view = None
        
    def create_app(self):
        """앱 생성"""
        try:
            print("앱을 생성하는 중...")
            
            self.app = self.ctk.CTk()
            print("✓ 기본 앱 생성 성공")
            
            self.app.title("치과 연차관리 시스템")
            self.app.geometry("1500x950")
            self.app.minsize(1300, 850)
            print("✓ 창 설정 완료")
            
            # 테마 설정
            self.ctk.set_appearance_mode("light")
            self.ctk.set_default_color_theme("blue")
            print("✓ 테마 설정 완료")
            
            # 그리드 설정
            self.app.grid_rowconfigure(0, weight=1)
            self.app.grid_columnconfigure(0, weight=1)
            print("✓ 레이아웃 설정 완료")
            
            return True
            
        except Exception as e:
            print(f"❌ 앱 생성 실패: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def show_login(self):
        """로그인 화면 표시"""
        try:
            print("로그인 화면을 생성하는 중...")
            
            if self.current_view:
                print("기존 화면 제거 중...")
                self.current_view.destroy()
            
            print("LoginView 인스턴스 생성 중...")
            self.current_view = self.LoginView(self.app, self.show_main)
            print("✓ LoginView 생성 성공")
            
            print("LoginView 배치 중...")
            self.current_view.grid(row=0, column=0, sticky="nsew")
            print("✓ LoginView 배치 성공")
            
            return True
            
        except Exception as e:
            print(f"❌ 로그인 화면 생성 실패: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def show_main(self):
        """메인 화면 표시"""
        try:
            print("메인 화면을 생성하는 중...")
            
            if self.current_view:
                self.current_view.destroy()
            
            self.current_view = self.MainView(self.app, self.show_login)
            self.current_view.grid(row=0, column=0, sticky="nsew")
            print("✓ 메인 화면 생성 성공")
            
        except Exception as e:
            print(f"❌ 메인 화면 생성 실패: {e}")
            import traceback
            traceback.print_exc()
    
    def run(self):
        """앱 실행"""
        try:
            if not self.create_app():
                return False
                
            if not self.show_login():
                return False
            
            print("\n🎉 앱이 성공적으로 시작되었습니다!")
            print("메인루프를 시작합니다...")
            
            # 종료 핸들러 등록
            self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            self.app.mainloop()
            print("✓ 앱이 정상 종료되었습니다.")
            return True
            
        except KeyboardInterrupt:
            print("\n사용자가 프로그램을 중단했습니다.")
            return True
            
        except Exception as e:
            print(f"\n❌ 앱 실행 중 오류: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def on_closing(self):
        """앱 종료 처리"""
        try:
            print("앱을 종료하는 중...")
            if self.app:
                self.app.quit()
                self.app.destroy()
        except:
            pass

def main():
    """메인 함수"""
    print("=" * 60)
    print("치과 연차관리 시스템 (안전 모드)")
    print("=" * 60)
    print(f"Python 버전: {sys.version}")
    print(f"작업 디렉토리: {os.getcwd()}")
    print()
    
    try:
        # 1단계: 모듈 import
        ctk, LoginView, MainView = safe_import()
        
        # 2단계: 앱 생성 및 실행
        app = SafeDentalLeaveApp(ctk, LoginView, MainView)
        success = app.run()
        
        if not success:
            print("\n앱 실행에 실패했습니다.")
            input("Enter를 눌러 종료...")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {e}")
        import traceback
        traceback.print_exc()
        print("\n" + "="*50)
        print("문제 해결을 위해 다음을 시도해보세요:")
        print("1. python debug.py 실행")
        print("2. python test_main_step.py 실행")
        print("3. 필요한 패키지 재설치")
        print("="*50)
        input("\nEnter를 눌러 종료...")
        sys.exit(1)

if __name__ == "__main__":
    main()