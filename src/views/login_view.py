import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, date
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
        login_button.grid(row=4, column=0, columnspan=2, pady=(0, 10))
        
        # 신규 직원 등록 버튼
        register_button = ctk.CTkButton(
            input_frame,
            text="신규 직원 등록",
            command=self.open_register_dialog,
            width=330,
            height=40,
            font=Theme.get_font('body'),
            fg_color=Theme.COLORS['secondary'],
            hover_color=Theme.COLORS['primary'],
            corner_radius=8
        )
        register_button.grid(row=5, column=0, columnspan=2, pady=(0, 20))
        
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
    
    def open_register_dialog(self):
        """신규 직원 등록 다이얼로그 열기"""
        dialog = EmployeeRegisterDialog(self, self.db, self.on_employee_registered)
    
    def on_employee_registered(self, employee_name, password):
        """신규 직원 등록 완료 후 콜백"""
        # 직원 목록 새로고침
        self.refresh_employee_list()
        
        # 새로 등록된 직원으로 자동 선택
        self.username_combo.set(employee_name)
        self.password_entry.delete(0, 'end')
        self.password_entry.insert(0, password)
        self.password_entry.focus()
        
        messagebox.showinfo("등록 완료", f"{employee_name}님이 성공적으로 등록되었습니다.\n로그인을 진행해주세요.")


class EmployeeRegisterDialog:
    def __init__(self, parent, db, callback):
        self.db = db
        self.callback = callback
        
        # 다이얼로그 창 생성
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("신규 직원 등록")
        self.dialog.geometry("400x600")
        self.dialog.resizable(False, False)
        
        # 부모 창 중앙에 배치
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
        
        # 창 중앙 배치
        self.dialog.update_idletasks()
        x = (parent.winfo_screenwidth() // 2) - (400 // 2)
        y = (parent.winfo_screenheight() // 2) - (600 // 2)
        self.dialog.geometry(f"400x600+{x}+{y}")
    
    def setup_ui(self):
        # 메인 프레임
        main_frame = ctk.CTkScrollableFrame(self.dialog, width=380, height=580)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # 제목
        title_label = ctk.CTkLabel(
            main_frame,
            text="신규 직원 등록",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # 필수 정보
        required_frame = ctk.CTkFrame(main_frame)
        required_frame.pack(fill="x", padx=10, pady=5)
        
        required_title = ctk.CTkLabel(
            required_frame,
            text="필수 정보",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        required_title.pack(pady=(10, 5))
        
        # 이름
        ctk.CTkLabel(required_frame, text="이름 *").pack(anchor="w", padx=10, pady=(10, 5))
        self.name_entry = ctk.CTkEntry(required_frame, width=300, placeholder_text="이름을 입력하세요")
        self.name_entry.pack(padx=10, pady=(0, 10))
        
        # 비밀번호
        ctk.CTkLabel(required_frame, text="비밀번호 * (4자 이상)", text_color=Theme.COLORS['text_primary']).pack(anchor="w", padx=10, pady=(5, 5))
        self.password_entry = ctk.CTkEntry(required_frame, width=300, show="*", placeholder_text="4자 이상의 비밀번호를 입력하세요")
        self.password_entry.pack(padx=10, pady=(0, 5))
        
        # 비밀번호 안내 문구
        password_info = ctk.CTkLabel(
            required_frame,
            text="* 비밀번호는 최소 4자 이상이어야 합니다.",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        password_info.pack(anchor="w", padx=10, pady=(0, 10))
        
        # 비밀번호 확인
        ctk.CTkLabel(required_frame, text="비밀번호 확인 *").pack(anchor="w", padx=10, pady=(5, 5))
        self.password_confirm_entry = ctk.CTkEntry(required_frame, width=300, show="*", placeholder_text="비밀번호를 다시 입력하세요")
        self.password_confirm_entry.pack(padx=10, pady=(0, 10))
        
        # 입사일
        ctk.CTkLabel(required_frame, text="입사일 *").pack(anchor="w", padx=10, pady=(5, 5))
        date_frame = ctk.CTkFrame(required_frame, fg_color="transparent")
        date_frame.pack(padx=10, pady=(0, 10))
        
        self.hire_date_entry = DateEntry(
            date_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd',
            maxdate=date.today()
        )
        self.hire_date_entry.pack(side="left")
        
        # 연차 일수
        ctk.CTkLabel(required_frame, text="연간 연차 일수 *").pack(anchor="w", padx=10, pady=(5, 5))
        self.annual_leave_entry = ctk.CTkEntry(required_frame, width=300, placeholder_text="15")
        self.annual_leave_entry.pack(padx=10, pady=(0, 15))
        self.annual_leave_entry.insert(0, "15")  # 기본값
        
        # 선택 정보
        optional_frame = ctk.CTkFrame(main_frame)
        optional_frame.pack(fill="x", padx=10, pady=5)
        
        optional_title = ctk.CTkLabel(
            optional_frame,
            text="선택 정보",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        optional_title.pack(pady=(10, 5))
        
        # 직책
        ctk.CTkLabel(optional_frame, text="직책").pack(anchor="w", padx=10, pady=(5, 5))
        self.position_entry = ctk.CTkEntry(optional_frame, width=300, placeholder_text="예: 치과의사, 간호사, 접수")
        self.position_entry.pack(padx=10, pady=(0, 10))
        
        # 전화번호
        ctk.CTkLabel(optional_frame, text="전화번호").pack(anchor="w", padx=10, pady=(5, 5))
        self.phone_entry = ctk.CTkEntry(optional_frame, width=300, placeholder_text="010-1234-5678")
        self.phone_entry.pack(padx=10, pady=(0, 10))
        
        # 고용 형태
        ctk.CTkLabel(optional_frame, text="고용 형태").pack(anchor="w", padx=10, pady=(5, 5))
        self.employment_type_combo = ctk.CTkComboBox(
            optional_frame,
            values=["정규직", "계약직", "파트타임", "인턴"],
            width=300
        )
        self.employment_type_combo.pack(padx=10, pady=(0, 10))
        self.employment_type_combo.set("정규직")
        
        # 메모
        ctk.CTkLabel(optional_frame, text="메모").pack(anchor="w", padx=10, pady=(5, 5))
        self.memo_entry = ctk.CTkTextbox(optional_frame, width=300, height=80)
        self.memo_entry.pack(padx=10, pady=(0, 15))
        
        # 버튼 프레임
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        # 취소 버튼
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="취소",
            command=self.dialog.destroy,
            width=120,
            fg_color="gray",
            hover_color="darkgray"
        )
        cancel_btn.pack(side="left", padx=5)
        
        # 등록 버튼
        register_btn = ctk.CTkButton(
            button_frame,
            text="등록",
            command=self.register_employee,
            width=120,
            fg_color=Theme.COLORS['primary'],
            hover_color=Theme.COLORS['primary_hover']
        )
        register_btn.pack(side="left", padx=5)
        
        # 첫 번째 입력 필드에 포커스
        self.name_entry.focus()
    
    def register_employee(self):
        """직원 등록 처리"""
        try:
            # 필수 필드 검증
            name = self.name_entry.get().strip()
            password = self.password_entry.get()
            password_confirm = self.password_confirm_entry.get()
            hire_date = self.hire_date_entry.get_date()
            annual_leave_days = self.annual_leave_entry.get().strip()
            
            if not name:
                messagebox.showerror("입력 오류", "이름을 입력해주세요.")
                self.name_entry.focus()
                return
            
            if not password:
                messagebox.showerror("입력 오류", "비밀번호를 입력해주세요.")
                self.password_entry.focus()
                return
            
            if password != password_confirm:
                messagebox.showerror("입력 오류", "비밀번호가 일치하지 않습니다.")
                self.password_confirm_entry.focus()
                return
            
            if len(password) < 4:
                messagebox.showerror("입력 오류", "비밀번호는 4자 이상이어야 합니다.")
                self.password_entry.focus()
                return
            
            try:
                annual_leave_days = int(annual_leave_days)
                if annual_leave_days < 0 or annual_leave_days > 365:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("입력 오류", "연간 연차 일수는 0~365 사이의 숫자를 입력해주세요.")
                self.annual_leave_entry.focus()
                return
            
            # 선택 필드
            position = self.position_entry.get().strip() or None
            phone = self.phone_entry.get().strip() or None
            employment_type = self.employment_type_combo.get() if self.employment_type_combo.get() != "정규직" else None
            memo = self.memo_entry.get("1.0", "end-1c").strip() or None
            
            # 이름 중복 확인
            try:
                existing_user = self.db.authenticate_user(name, "dummy")
                if existing_user is None:
                    # 인증 실패는 정상 (사용자가 없음)
                    pass
                else:
                    # 인증 성공은 이미 존재하는 사용자
                    messagebox.showerror("등록 오류", f"'{name}' 이름의 직원이 이미 존재합니다.")
                    self.name_entry.focus()
                    return
            except:
                # 인증 과정에서 오류가 나면 사용자가 없다고 가정
                pass
            
            # 직원 생성
            employee_id = self.db.create_employee(
                name=name,
                password=password,
                hire_date=hire_date,
                annual_leave_days=annual_leave_days,
                position=position,
                phone=phone,
                employment_type=employment_type,
                memo=memo,
                is_admin=False
            )
            
            # 성공 시 콜백 호출 및 다이얼로그 닫기
            self.callback(name, password)
            self.dialog.destroy()
            
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                messagebox.showerror("등록 오류", f"'{name}' 이름의 직원이 이미 존재합니다.")
            else:
                messagebox.showerror("등록 오류", f"직원 등록 중 오류가 발생했습니다: {str(e)}")
            print(f"직원 등록 오류: {e}")
            import traceback
            traceback.print_exc()