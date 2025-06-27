#!/usr/bin/env python3
"""
GUI만 표시하는 버전 (콘솔 창 없음)
.pyw 확장자로 실행하면 콘솔 창이 나타나지 않습니다.
"""
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
        
        # 창을 화면 중앙에 배치
        self.center_window()
        
        # 창을 최상위로 가져오기 (잠시만)
        self.lift()
        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))
        self.focus_force()
        
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
            # 콘솔 없이 실행될 때는 메시지박스로 오류 표시
            import tkinter.messagebox as messagebox
            import traceback
            error_details = traceback.format_exc()
            messagebox.showerror("오류", f"초기화 중 오류가 발생했습니다:\n{str(e)}\n\n자세한 내용:\n{error_details}")
    
    def on_closing(self):
        """창 닫기 이벤트"""
        self.quit()
    
    def center_window(self):
        """창을 화면 중앙에 배치"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def show_login(self):
        try:
            # 기존 위젯 제거
            for widget in self.winfo_children():
                widget.destroy()
            
            # 늦은 import를 통해 초기화 타이밍 문제 해결
            from views.login_view import LoginView
            
            self.current_view = LoginView(self, self.show_main)
            self.current_view.grid(row=0, column=0, sticky="nsew")
        except Exception as e:
            # 콘솔 없이 실행될 때는 메시지박스로 오류 표시
            import tkinter.messagebox as messagebox
            import traceback
            error_details = traceback.format_exc()
            messagebox.showerror("오류", f"로그인 화면 생성 중 오류가 발생했습니다:\n{str(e)}\n\n자세한 내용:\n{error_details}")
            # quit() 대신 창을 유지하고 오류 메시지만 표시
            # self.quit()
    
    def show_main(self):
        if hasattr(self, 'current_view'):
            self.current_view.destroy()
        
        from views.main_view import MainView
        self.current_view = MainView(self, self.show_login)
        self.current_view.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    try:
        app = DentalLeaveApp()
        app.mainloop()
    except Exception as e:
        # 오류 발생시 파일로 로그 저장
        with open("error_log.txt", "w", encoding="utf-8") as f:
            import traceback
            f.write(f"오류 발생: {str(e)}\n\n")
            f.write("상세 정보:\n")
            traceback.print_exc(file=f)
        
        # 메시지박스로 알림
        import tkinter
        import tkinter.messagebox
        root = tkinter.Tk()
        root.withdraw()
        tkinter.messagebox.showerror(
            "치과 연차관리 시스템", 
            f"프로그램 실행 중 오류가 발생했습니다.\n\n{str(e)}\n\n자세한 내용은 error_log.txt 파일을 확인하세요."
        )
        root.destroy()