#!/usr/bin/env python3
"""
GUI 디버그 버전 - 창이 바로 닫히는 문제 진단
"""
import customtkinter as ctk
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_print(msg):
    """디버그 메시지 출력 및 파일 저장"""
    timestamp = time.strftime("%H:%M:%S")
    debug_msg = f"[{timestamp}] {msg}"
    print(debug_msg)
    
    with open("debug_gui_log.txt", "a", encoding="utf-8") as f:
        f.write(debug_msg + "\n")

class DentalLeaveApp(ctk.CTk):
    def __init__(self):
        debug_print("DentalLeaveApp.__init__ 시작")
        try:
            super().__init__()
            debug_print("CTk 초기화 완료")
            
            self.title("치과 연차관리 시스템")
            self.geometry("1500x950")
            self.minsize(1300, 850)
            debug_print("창 설정 완료")
            
            # 테마 설정
            ctk.set_appearance_mode("light")
            ctk.set_default_color_theme("blue")
            debug_print("테마 설정 완료")
            
            # 윈도우 아이콘 설정 (가능한 경우)
            try:
                self.iconify()
                self.deiconify()
                debug_print("아이콘 설정 완료")
            except Exception as e:
                debug_print(f"아이콘 설정 실패 (무시): {e}")
            
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)
            debug_print("그리드 설정 완료")
            
            # 창 닫기 이벤트 가로채기
            self.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            # 임시 라벨 표시 (로그인 화면 대신)
            debug_print("임시 화면 표시 시작")
            temp_label = ctk.CTkLabel(self, text="초기화 중...", font=("Arial", 24))
            temp_label.grid(row=0, column=0, pady=50)
            self.update()  # 화면 업데이트
            debug_print("임시 화면 표시 완료")
            
            # 0.5초 대기
            self.after(500, self.delayed_init)
            
        except Exception as e:
            debug_print(f"초기화 중 오류: {e}")
            import traceback
            debug_print(traceback.format_exc())
            
    def delayed_init(self):
        """지연된 초기화"""
        debug_print("delayed_init 시작")
        try:
            self.show_login()
            debug_print("로그인 화면 표시 완료")
        except Exception as e:
            debug_print(f"delayed_init 오류: {e}")
            import traceback
            debug_print(traceback.format_exc())
            self.show_error_screen(str(e))
    
    def show_error_screen(self, error_msg):
        """오류 화면 표시"""
        debug_print("오류 화면 표시")
        
        # 기존 위젯 제거
        for widget in self.winfo_children():
            widget.destroy()
        
        # 오류 메시지 표시
        error_frame = ctk.CTkFrame(self)
        error_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        ctk.CTkLabel(error_frame, text="오류 발생", 
                    font=("Arial", 24, "bold"), text_color="red").pack(pady=20)
        
        ctk.CTkLabel(error_frame, text=error_msg, 
                    font=("Arial", 12), wraplength=800).pack(pady=10)
        
        ctk.CTkLabel(error_frame, text="debug_gui_log.txt 파일을 확인하세요", 
                    font=("Arial", 10), text_color="gray").pack(pady=5)
        
        ctk.CTkButton(error_frame, text="종료", command=self.quit).pack(pady=20)
    
    def on_closing(self):
        """창 닫기 이벤트"""
        debug_print("창 닫기 이벤트 발생")
        self.quit()
    
    def show_login(self):
        debug_print("show_login 시작")
        try:
            if hasattr(self, 'current_view'):
                self.current_view.destroy()
                debug_print("기존 뷰 제거")
            
            # LoginView import를 여기서 시도
            debug_print("LoginView import 시작")
            from views.login_view import LoginView
            debug_print("LoginView import 완료")
            
            debug_print("LoginView 인스턴스 생성 시작")
            self.current_view = LoginView(self, self.show_main)
            debug_print("LoginView 인스턴스 생성 완료")
            
            self.current_view.grid(row=0, column=0, sticky="nsew")
            debug_print("LoginView 그리드 배치 완료")
            
        except Exception as e:
            debug_print(f"show_login 오류: {e}")
            import traceback
            debug_print(traceback.format_exc())
            raise
    
    def show_main(self):
        debug_print("show_main 호출됨")
        if hasattr(self, 'current_view'):
            self.current_view.destroy()
        
        from views.main_view import MainView
        self.current_view = MainView(self, self.show_login)
        self.current_view.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    # 로그 파일 초기화
    with open("debug_gui_log.txt", "w", encoding="utf-8") as f:
        f.write("=== GUI 디버그 로그 시작 ===\n")
    
    debug_print("프로그램 시작")
    debug_print(f"Python 버전: {sys.version}")
    debug_print(f"작업 디렉토리: {os.getcwd()}")
    
    try:
        debug_print("앱 생성 시작")
        app = DentalLeaveApp()
        debug_print("앱 생성 완료")
        
        debug_print("메인루프 시작")
        app.mainloop()
        debug_print("메인루프 종료")
        
    except Exception as e:
        debug_print(f"최상위 오류: {e}")
        import traceback
        debug_print(traceback.format_exc())
        
        # 오류 메시지박스
        import tkinter.messagebox as messagebox
        messagebox.showerror("치과 연차관리 시스템", 
                            f"프로그램 실행 중 오류:\n{str(e)}\n\ndebug_gui_log.txt 확인")
    
    debug_print("프로그램 종료")
    print("\n디버그 로그가 debug_gui_log.txt에 저장되었습니다.")
    input("Enter를 눌러 종료...")