import customtkinter as ctk
from tkinter import messagebox

class LoginViewSafe(ctk.CTkFrame):
    """안전한 로그인 뷰 - 최소한의 기능만 포함"""
    def __init__(self, parent, on_login_success):
        print("[LoginViewSafe] 초기화 시작")
        super().__init__(parent)
        
        self.on_login_success = on_login_success
        
        # 데이터베이스와 세션은 나중에 초기화
        self.db = None
        self.session = None
        
        # UI 먼저 설정
        self.setup_minimal_ui()
        
        # 데이터베이스 지연 로드
        self.after(100, self.load_database)
        
    def setup_minimal_ui(self):
        """최소한의 UI만 설정"""
        print("[LoginViewSafe] UI 설정 시작")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # 중앙 프레임
        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=0, column=0)
        
        # 제목
        title_label = ctk.CTkLabel(
            center_frame, 
            text="치과 연차관리 시스템", 
            font=("맑은 고딕", 24)
        )
        title_label.grid(row=0, column=0, pady=30)
        
        # 로딩 메시지
        self.status_label = ctk.CTkLabel(
            center_frame,
            text="로그인 화면 준비 중...",
            font=("맑은 고딕", 12)
        )
        self.status_label.grid(row=1, column=0, pady=20)
        
        print("[LoginViewSafe] 최소 UI 설정 완료")
    
    def load_database(self):
        """데이터베이스 로드"""
        print("[LoginViewSafe] 데이터베이스 로드 시작")
        try:
            from models.database import Database
            from utils.session import Session
            
            self.db = Database()
            self.session = Session()
            
            print("[LoginViewSafe] 데이터베이스 로드 완료")
            self.setup_full_ui()
            
        except Exception as e:
            print(f"[LoginViewSafe] 데이터베이스 로드 실패: {e}")
            self.status_label.configure(
                text=f"데이터베이스 로드 실패: {str(e)}",
                text_color="red"
            )
            
            # 재시도 버튼
            retry_btn = ctk.CTkButton(
                self.status_label.master,
                text="재시도",
                command=self.load_database
            )
            retry_btn.grid(row=2, column=0, pady=10)
    
    def setup_full_ui(self):
        """전체 UI 설정"""
        print("[LoginViewSafe] 전체 UI 설정 시작")
        
        # 기존 위젯 제거
        for widget in self.winfo_children():
            widget.destroy()
        
        # 새로운 UI 구성
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # 로그인 프레임
        login_frame = ctk.CTkFrame(self)
        login_frame.grid(row=0, column=0, padx=20, pady=20)
        
        # 제목
        title_label = ctk.CTkLabel(
            login_frame, 
            text="치과 연차관리 시스템", 
            font=("맑은 고딕", 24)
        )
        title_label.grid(row=0, column=0, columnspan=2, padx=40, pady=(40, 30))
        
        # 직원 선택
        username_label = ctk.CTkLabel(
            login_frame, 
            text="직원 선택", 
            font=("맑은 고딕", 12)
        )
        username_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=40, pady=(0, 5))
        
        # 직원 목록
        try:
            employees = self.db.get_all_employees()
            employee_names = [emp['name'] for emp in employees]
            if not employee_names:
                employee_names = ["관리자"]
        except:
            employee_names = ["관리자"]
        
        self.username_combo = ctk.CTkComboBox(
            login_frame,
            values=employee_names,
            width=280,
            height=40
        )
        self.username_combo.grid(row=2, column=0, columnspan=2, padx=40, pady=(0, 15))
        self.username_combo.set("직원을 선택하세요")
        
        # 비밀번호
        password_label = ctk.CTkLabel(
            login_frame, 
            text="비밀번호", 
            font=("맑은 고딕", 12)
        )
        password_label.grid(row=3, column=0, columnspan=2, sticky="w", padx=40, pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(
            login_frame, 
            width=280, 
            height=40,
            show="*"
        )
        self.password_entry.grid(row=4, column=0, columnspan=2, padx=40, pady=(0, 20))
        
        # 로그인 버튼
        login_button = ctk.CTkButton(
            login_frame,
            text="로그인",
            command=self.login,
            width=280,
            height=45
        )
        login_button.grid(row=5, column=0, columnspan=2, padx=40, pady=(0, 20))
        
        # 도움말
        help_label = ctk.CTkLabel(
            login_frame,
            text="관리자 계정: 관리자 / admin123",
            font=("맑은 고딕", 10)
        )
        help_label.grid(row=6, column=0, columnspan=2, pady=(0, 30))
        
        print("[LoginViewSafe] 전체 UI 설정 완료")
    
    def login(self):
        """로그인 처리"""
        username = self.username_combo.get().strip()
        password = self.password_entry.get()
        
        if not username or username == "직원을 선택하세요" or not password:
            messagebox.showwarning("입력 오류", "직원을 선택하고 비밀번호를 입력해주세요.")
            return
        
        try:
            user = self.db.authenticate_user(username, password)
            
            if user:
                self.session.login(user)
                print(f"[LoginViewSafe] 로그인 성공: {username}")
                self.on_login_success()
            else:
                messagebox.showerror("로그인 실패", "비밀번호가 올바르지 않습니다.")
                self.password_entry.delete(0, 'end')
                
        except Exception as e:
            print(f"[LoginViewSafe] 로그인 처리 오류: {e}")
            messagebox.showerror("오류", f"로그인 처리 중 오류가 발생했습니다:\n{str(e)}")