#!/usr/bin/env python3
"""
안전한 로그인 뷰를 사용하는 메인
"""
import customtkinter as ctk
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from views.login_view_safe import LoginViewSafe
from views.main_view import MainView

class DentalLeaveApp(ctk.CTk):
    def __init__(self):
        print("[App] 초기화 시작")
        super().__init__()
        
        self.title("치과 연차관리 시스템")
        self.geometry("1500x950")
        self.minsize(1300, 850)
        
        # 테마 설정
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # 창 설정
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # 화면 중앙 배치
        self.center_window()
        
        # 에러 핸들러 설정
        self.report_callback_exception = self.handle_exception
        
        print("[App] 초기화 완료, 로그인 화면 표시")
        self.show_login()
    
    def center_window(self):
        """창을 화면 중앙에 배치"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """전역 예외 처리"""
        print(f"[App] 예외 발생: {exc_type.__name__}: {exc_value}")
        
        if exc_traceback:
            import traceback
            print("Traceback:")
            traceback.print_tb(exc_traceback)
        
        # 오류 화면 표시
        self.show_error_screen(str(exc_value))
    
    def show_error_screen(self, error_msg):
        """오류 화면 표시"""
        print("[App] 오류 화면 표시")
        
        # 기존 뷰 제거
        if hasattr(self, 'current_view'):
            self.current_view.destroy()
        
        # 오류 프레임
        error_frame = ctk.CTkFrame(self)
        error_frame.grid(row=0, column=0, padx=20, pady=20)
        
        ctk.CTkLabel(
            error_frame, 
            text="오류 발생", 
            font=("맑은 고딕", 24),
            text_color="red"
        ).pack(pady=20)
        
        ctk.CTkLabel(
            error_frame, 
            text=error_msg, 
            font=("맑은 고딕", 12),
            wraplength=600
        ).pack(pady=10)
        
        ctk.CTkButton(
            error_frame,
            text="다시 시도",
            command=self.show_login
        ).pack(pady=10)
        
        ctk.CTkButton(
            error_frame,
            text="종료",
            command=self.quit
        ).pack(pady=5)
    
    def show_login(self):
        """로그인 화면 표시"""
        try:
            print("[App] show_login 호출")
            
            if hasattr(self, 'current_view'):
                self.current_view.destroy()
                print("[App] 기존 뷰 제거")
            
            print("[App] LoginViewSafe 생성")
            self.current_view = LoginViewSafe(self, self.show_main)
            self.current_view.grid(row=0, column=0, sticky="nsew")
            print("[App] LoginViewSafe 배치 완료")
            
        except Exception as e:
            print(f"[App] show_login 오류: {e}")
            import traceback
            traceback.print_exc()
            self.show_error_screen(str(e))
    
    def show_main(self):
        """메인 화면 표시"""
        try:
            print("[App] show_main 호출")
            
            if hasattr(self, 'current_view'):
                self.current_view.destroy()
            
            self.current_view = MainView(self, self.show_login)
            self.current_view.grid(row=0, column=0, sticky="nsew")
            
        except Exception as e:
            print(f"[App] show_main 오류: {e}")
            self.show_error_screen(str(e))

if __name__ == "__main__":
    print("=== 치과 연차관리 시스템 (안전 모드) ===")
    print(f"Python: {sys.version}")
    print(f"작업 디렉토리: {os.getcwd()}")
    
    try:
        print("\n앱 생성 중...")
        app = DentalLeaveApp()
        
        print("메인루프 시작...")
        print("창이 표시되어야 합니다. 보이지 않으면 작업 표시줄을 확인하세요.")
        
        app.mainloop()
        
        print("프로그램 정상 종료")
        
    except Exception as e:
        print(f"\n최상위 오류: {e}")
        import traceback
        traceback.print_exc()
        
        # 오류 로그 저장
        with open("error_safe_login.txt", "w", encoding="utf-8") as f:
            f.write(f"오류: {e}\n\n")
            traceback.print_exc(file=f)
    
    input("\nEnter를 눌러 종료...")