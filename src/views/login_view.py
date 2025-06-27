import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from models.database import Database
from utils.session import Session
from utils.theme import Theme

class LoginView(ctk.CTkFrame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent, fg_color=Theme.COLORS['bg_primary'])
        try:
            print("데이터베이스 초기화 중...")
            self.db = Database()
            print("세션 초기화 중...")
            self.session = Session()
            self.on_login_success = on_login_success
            print("UI 설정 중...")
            self.setup_ui()
            print("로그인 뷰 초기화 완료")
        except Exception as e:
            print(f"로그인 뷰 초기화 오류: {e}")
            import traceback
            traceback.print_exc()
    
    def setup_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # 중앙 컨테이너
        center_frame = ctk.CTkFrame(self, fg_color="transparent")
        center_frame.grid(row=0, column=0, sticky="")
        
        # 로고/아이콘 영역
        logo_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        logo_frame.grid(row=0, column=0, pady=(0, 30))
        
        # 치과 이름
        clinic_name = ctk.CTkLabel(
            logo_frame,
            text="아너스치과교정과",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=Theme.COLORS['primary']
        )
        clinic_name.pack(pady=(0, 10))
        
        # 치과 아이콘 (이모지 사용)
        icon_label = ctk.CTkLabel(
            logo_frame,
            text="🦷",
            font=ctk.CTkFont(size=60)
        )
        icon_label.pack()
        
        # 로그인 카드
        login_frame = ctk.CTkFrame(center_frame, corner_radius=16, border_width=2, 
                                  border_color=Theme.COLORS['medium_gray'])
        login_frame.grid(row=1, column=0, padx=20, pady=20)
        
        # 제목
        title_label = ctk.CTkLabel(
            login_frame, 
            text="치과 연차관리 시스템", 
            font=Theme.get_font('title'),
            text_color=Theme.COLORS['primary']
        )
        title_label.grid(row=0, column=0, columnspan=2, padx=40, pady=(40, 30))
        
        # 입력 필드 컨테이너
        input_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        input_frame.grid(row=1, column=0, columnspan=2, padx=40, pady=(0, 20))
        input_frame.grid_columnconfigure(0, weight=1)
        
        # 직원 선택
        username_label = ctk.CTkLabel(
            input_frame, 
            text="직원 선택", 
            font=Theme.get_font('body_bold'),
            text_color=Theme.COLORS['text_primary']
        )
        username_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        # 직원 목록 가져오기
        try:
            employees = self.db.get_all_employees()
            employee_names = [emp['name'] for emp in employees]
            if not employee_names:
                employee_names = ["관리자"]
            print(f"직원 목록 로드 완료: {len(employee_names)}명")
        except Exception as e:
            print(f"직원 목록 로드 오류: {e}")
            employee_names = ["관리자"]  # 기본값
        
        self.username_combo = ctk.CTkComboBox(
            input_frame,
            values=employee_names,
            width=330,
            height=40,
            font=Theme.get_font('body'),
            corner_radius=8,
            dropdown_font=Theme.get_font('body')
        )
        self.username_combo.grid(row=1, column=0, columnspan=2, pady=(0, 15))
        self.username_combo.set("직원을 선택하세요")
        
        # 새로고침 버튼 (직원 목록 갱신용) - 숨김
        # refresh_btn = ctk.CTkButton(
        #     input_frame,
        #     text="🔄",
        #     width=40,
        #     height=40,
        #     font=ctk.CTkFont(size=16),
        #     command=self.refresh_employee_list,
        #     fg_color=Theme.COLORS['secondary'],
        #     hover_color=Theme.COLORS['primary']
        # )
        # refresh_btn.grid(row=1, column=1, padx=(10, 0), pady=(0, 15))
        
        # 비밀번호 입력
        password_label = ctk.CTkLabel(
            input_frame, 
            text="비밀번호", 
            font=Theme.get_font('body_bold'),
            text_color=Theme.COLORS['text_primary']
        )
        password_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(
            input_frame, 
            width=330, 
            height=40,
            font=Theme.get_font('body'),
            corner_radius=8,
            show="*",
            placeholder_text="비밀번호를 입력하세요"
        )
        self.password_entry.grid(row=3, column=0, columnspan=2, pady=(0, 20))
        
        # 로그인 버튼
        login_button = ctk.CTkButton(
            input_frame,
            text="로그인",
            command=self.login,
            width=330,
            height=45,
            font=Theme.get_font('button'),
            fg_color=Theme.COLORS['primary'],
            hover_color=Theme.COLORS['primary_hover'],
            corner_radius=8
        )
        login_button.grid(row=4, column=0, columnspan=2, pady=(0, 20))
        
        # 도움말 텍스트 삭제됨
        
        # 키보드 이벤트
        self.password_entry.bind("<Return>", lambda e: self.login())
        self.username_combo.bind("<Return>", lambda e: self.password_entry.focus())
        
        self.username_combo.focus()
    
    def refresh_employee_list(self):
        """직원 목록 새로고침"""
        try:
            employees = self.db.get_all_employees()
            employee_names = [emp['name'] for emp in employees]
            self.username_combo.configure(values=employee_names)
            if employee_names:
                self.username_combo.set("직원을 선택하세요")
            print(f"직원 목록 새로고침 완료: {len(employee_names)}명")
        except Exception as e:
            print(f"직원 목록 새로고침 오류: {e}")
            messagebox.showerror("오류", "직원 목록을 불러오는데 실패했습니다.")
    
    def login(self):
        username = self.username_combo.get().strip()
        password = self.password_entry.get()
        
        if not username or username == "직원을 선택하세요" or not password:
            messagebox.showwarning("입력 오류", "직원을 선택하고 비밀번호를 입력해주세요.")
            return
        
        user = self.db.authenticate_user(username, password)
        
        if user:
            self.session.login(user)
            self.on_login_success()
        else:
            messagebox.showerror("로그인 실패", "선택한 직원의 비밀번호가 올바르지 않습니다.")
            self.password_entry.delete(0, 'end')
            self.password_entry.focus()