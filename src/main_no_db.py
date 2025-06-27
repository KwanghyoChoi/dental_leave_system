#!/usr/bin/env python3
"""
데이터베이스 없이 GUI만 테스트
"""
import customtkinter as ctk
import sys
import os

class MockDatabase:
    """가짜 데이터베이스"""
    def __init__(self):
        print("MockDatabase 초기화")
    
    def get_all_employees(self):
        return [{'name': '테스트직원1'}, {'name': '테스트직원2'}]
    
    def authenticate_user(self, username, password):
        if password == "test":
            return {'id': 1, 'name': username, 'is_admin': 1}
        return None

class MockSession:
    """가짜 세션"""
    def __init__(self):
        self.user = None
    
    def login(self, user):
        self.user = user
    
    def logout(self):
        self.user = None
    
    def get_user_name(self):
        return self.user['name'] if self.user else "Unknown"
    
    def is_admin(self):
        return self.user and self.user.get('is_admin', 0) == 1

class SimpleLoginView(ctk.CTkFrame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.db = MockDatabase()
        self.session = MockSession()
        self.on_login_success = on_login_success
        
        # 간단한 UI
        ctk.CTkLabel(self, text="치과 연차관리 시스템", 
                    font=("Arial", 24, "bold")).pack(pady=30)
        
        ctk.CTkLabel(self, text="직원 선택:").pack(pady=5)
        self.username_combo = ctk.CTkComboBox(self, values=["테스트직원1", "테스트직원2"])
        self.username_combo.pack(pady=5)
        self.username_combo.set("테스트직원1")
        
        ctk.CTkLabel(self, text="비밀번호:").pack(pady=5)
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.pack(pady=5)
        
        ctk.CTkButton(self, text="로그인 (비밀번호: test)", 
                     command=self.login).pack(pady=20)
        
        ctk.CTkLabel(self, text="비밀번호는 'test' 입니다", 
                    text_color="gray").pack(pady=5)
    
    def login(self):
        username = self.username_combo.get()
        password = self.password_entry.get()
        
        user = self.db.authenticate_user(username, password)
        if user:
            self.session.login(user)
            print(f"로그인 성공: {username}")
            self.on_login_success()
        else:
            print("로그인 실패")

class SimpleMainView(ctk.CTkFrame):
    def __init__(self, parent, on_logout):
        super().__init__(parent)
        self.on_logout = on_logout
        
        ctk.CTkLabel(self, text="메인 화면", 
                    font=("Arial", 24, "bold")).pack(pady=30)
        
        ctk.CTkLabel(self, text="로그인 성공! GUI가 정상 작동합니다.", 
                    font=("Arial", 16)).pack(pady=20)
        
        ctk.CTkButton(self, text="로그아웃", 
                     command=on_logout).pack(pady=20)

class TestApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("치과 연차관리 시스템 - DB 없음")
        self.geometry("800x600")
        
        # 화면 중앙 배치
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 400
        y = (self.winfo_screenheight() // 2) - 300
        self.geometry(f'800x600+{x}+{y}')
        
        self.show_login()
        
        print("앱 초기화 완료 - 창이 표시되어야 합니다")
    
    def show_login(self):
        if hasattr(self, 'current_view'):
            self.current_view.destroy()
        
        self.current_view = SimpleLoginView(self, self.show_main)
        self.current_view.pack(fill="both", expand=True, padx=20, pady=20)
    
    def show_main(self):
        if hasattr(self, 'current_view'):
            self.current_view.destroy()
        
        self.current_view = SimpleMainView(self, self.show_login)
        self.current_view.pack(fill="both", expand=True, padx=20, pady=20)

if __name__ == "__main__":
    print("데이터베이스 없이 GUI 테스트 시작...")
    
    try:
        app = TestApp()
        app.mainloop()
        print("프로그램 정상 종료")
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nEnter를 눌러 종료...")