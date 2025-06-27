#!/usr/bin/env python3
"""
간단한 tkinter 버전 - customtkinter 없이 테스트용
"""
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from models.database import Database
    from utils.session import Session
except ImportError as e:
    print(f"모듈 import 오류: {e}")
    sys.exit(1)

class SimpleLoginView(tk.Frame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.db = Database()
        self.session = Session()
        self.on_login_success = on_login_success
        
        self.setup_ui()
    
    def setup_ui(self):
        # 제목
        title_label = tk.Label(self, text="치과 연차관리 시스템", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # 직원 선택
        tk.Label(self, text="직원 선택:").pack()
        
        try:
            employees = self.db.get_all_employees()
            employee_names = [emp['name'] for emp in employees]
        except:
            employee_names = ["관리자"]
        
        self.username_var = tk.StringVar()
        self.username_combo = ttk.Combobox(self, textvariable=self.username_var, values=employee_names)
        self.username_combo.pack(pady=5)
        self.username_combo.set("직원을 선택하세요")
        
        # 비밀번호
        tk.Label(self, text="비밀번호:").pack(pady=(10, 0))
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)
        
        # 로그인 버튼
        login_btn = tk.Button(self, text="로그인", command=self.login)
        login_btn.pack(pady=20)
        
        # 도움말
        tk.Label(self, text="관리자 계정: 관리자 / admin123", fg="gray").pack()
    
    def login(self):
        username = self.username_var.get().strip()
        password = self.password_entry.get()
        
        if not username or username == "직원을 선택하세요" or not password:
            messagebox.showwarning("입력 오류", "직원을 선택하고 비밀번호를 입력해주세요.")
            return
        
        user = self.db.authenticate_user(username, password)
        
        if user:
            self.session.login(user)
            messagebox.showinfo("성공", f"{username}님 로그인 성공!")
            self.on_login_success()
        else:
            messagebox.showerror("로그인 실패", "비밀번호가 올바르지 않습니다.")
            self.password_entry.delete(0, 'end')

class SimpleMainView(tk.Frame):
    def __init__(self, parent, on_logout):
        super().__init__(parent)
        self.session = Session()
        self.on_logout = on_logout
        
        self.setup_ui()
    
    def setup_ui(self):
        # 환영 메시지
        welcome_label = tk.Label(
            self, 
            text=f"{self.session.get_user_name()}님 환영합니다!", 
            font=("Arial", 14)
        )
        welcome_label.pack(pady=20)
        
        # 메뉴 버튼들
        tk.Button(self, text="연차 관리", width=20, height=2).pack(pady=5)
        tk.Button(self, text="달력 보기", width=20, height=2).pack(pady=5)
        
        if self.session.is_admin():
            tk.Button(self, text="전체 연차 현황", width=20, height=2).pack(pady=5)
            tk.Button(self, text="직원 관리", width=20, height=2).pack(pady=5)
            tk.Button(self, text="공통 연차 관리", width=20, height=2).pack(pady=5)
        
        tk.Button(self, text="통계", width=20, height=2).pack(pady=5)
        
        # 로그아웃 버튼
        logout_btn = tk.Button(self, text="로그아웃", command=self.logout, bg="lightcoral")
        logout_btn.pack(pady=20)
    
    def logout(self):
        if messagebox.askyesno("로그아웃", "정말 로그아웃하시겠습니까?"):
            self.session.logout()
            self.on_logout()

class SimpleDentalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("치과 연차관리 시스템 (Simple)")
        self.geometry("500x600")
        self.resizable(True, True)
        
        self.show_login()
    
    def show_login(self):
        if hasattr(self, 'current_view'):
            self.current_view.destroy()
        
        self.current_view = SimpleLoginView(self, self.show_main)
        self.current_view.pack(fill="both", expand=True)
    
    def show_main(self):
        if hasattr(self, 'current_view'):
            self.current_view.destroy()
        
        self.current_view = SimpleMainView(self, self.show_login)
        self.current_view.pack(fill="both", expand=True)

if __name__ == "__main__":
    try:
        print("간단한 버전을 시작합니다...")
        app = SimpleDentalApp()
        app.mainloop()
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()
        input("Enter를 눌러 종료...")