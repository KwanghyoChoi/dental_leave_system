import customtkinter as ctk
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class DentalLeaveApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("치과 연차관리 시스템")
        self.geometry("1500x950")
        self.minsize(1300, 850)
        
        # 테마 설정
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # 윈도우 아이콘 설정 (가능한 경우)
        try:
            self.iconify()
            self.deiconify()
        except:
            pass
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # 창 닫기 이벤트 처리
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 임시 로딩 화면 표시
        temp_label = ctk.CTkLabel(self, text="초기화 중...", font=("Arial", 24))
        temp_label.grid(row=0, column=0, pady=50)
        self.update()
        
        # 지연된 초기화
        self.after(100, self.delayed_init)
    
    def delayed_init(self):
        """지연된 초기화"""
        try:
            self.show_login()
        except Exception as e:
            print(f"초기화 오류: {e}")
            import traceback
            traceback.print_exc()
    
    def on_closing(self):
        """창 닫기 이벤트"""
        self.quit()
    
    def show_login(self):
        try:
            print("로그인 화면을 표시합니다...")
            # 기존 위젯 제거
            for widget in self.winfo_children():
                widget.destroy()
            
            # 늦은 import를 통해 초기화 타이밍 문제 해결
            from views.login_view import LoginView
            
            self.current_view = LoginView(self, self.show_main)
            self.current_view.grid(row=0, column=0, sticky="nsew")
            print("로그인 화면 표시 완료")
        except Exception as e:
            print(f"로그인 화면 생성 오류: {e}")
            import traceback
            traceback.print_exc()
            # 오류 발생 시에도 앱이 종료되지 않도록 빈 프레임 표시
            error_frame = ctk.CTkFrame(self)
            error_label = ctk.CTkLabel(error_frame, text=f"오류 발생: {str(e)}", text_color="red")
            error_label.pack(pady=20)
            error_frame.grid(row=0, column=0, sticky="nsew")
            self.current_view = error_frame
    
    def show_main(self):
        if hasattr(self, 'current_view'):
            self.current_view.destroy()
        
        from views.main_view import MainView
        self.current_view = MainView(self, self.show_login)
        self.current_view.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    try:
        print("치과 연차관리 시스템을 시작합니다...")
        print("Python 버전:", sys.version)
        print("작업 디렉토리:", os.getcwd())
        
        # 패키지 체크
        try:
            import customtkinter
            print("✓ customtkinter 모듈 로드 성공")
        except ImportError as e:
            print(f"❌ customtkinter 모듈 로드 실패: {e}")
            print("다음 명령어로 설치하세요: pip install customtkinter")
            input("Enter를 눌러 종료...")
            sys.exit(1)
        
        print("앱을 초기화합니다...")
        app = DentalLeaveApp()
        print("✓ 앱 초기화 완료")
        
        # 창을 화면 중앙에 배치
        app.update_idletasks()
        width = app.winfo_width()
        height = app.winfo_height()
        x = (app.winfo_screenwidth() // 2) - (width // 2)
        y = (app.winfo_screenheight() // 2) - (height // 2)
        app.geometry(f'{width}x{height}+{x}+{y}')
        
        # 창을 최상위로 가져오기
        app.lift()
        app.attributes('-topmost', True)
        app.after(100, lambda: app.attributes('-topmost', False))
        app.focus_force()
        
        print("메인루프를 시작합니다...")
        print("GUI 창이 열려야 합니다. 창이 보이지 않으면:")
        print("- 작업 표시줄을 확인하세요")
        print("- Alt+Tab으로 창 전환을 시도하세요")
        print("- 다른 창 뒤에 숨어있을 수 있습니다")
        
        app.mainloop()
        print("프로그램이 정상 종료되었습니다.")
        
    except Exception as e:
        print(f"\n❌ 오류가 발생했습니다: {e}")
        print("\n상세 오류 정보:")
        import traceback
        traceback.print_exc()
        print("\n" + "="*50)
        print("문제 해결 방법:")
        print("1. 필요한 패키지 설치: pip install customtkinter Pillow tkcalendar bcrypt")
        print("2. Python 3.8 이상 버전 사용")
        print("3. src 폴더에서 실행: cd src && python main.py")
        print("="*50)
        input("\nEnter를 눌러 종료하세요...")