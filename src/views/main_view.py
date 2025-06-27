import customtkinter as ctk
from tkinter import messagebox
from utils.session import Session
from utils.theme import Theme

class MainView(ctk.CTkFrame):
    def __init__(self, parent, on_logout):
        super().__init__(parent, fg_color=Theme.COLORS['bg_secondary'])
        self.session = Session()
        self.on_logout = on_logout
        
        self.setup_ui()
    
    def setup_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # 헤더 - 그라데이션 효과를 위한 색상 설정
        header_frame = ctk.CTkFrame(self, fg_color=Theme.COLORS['primary'], corner_radius=0)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=0)
        
        # 좌측 로고 영역
        logo_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        logo_frame.pack(side="left", padx=20, pady=10)
        
        logo_icon = ctk.CTkLabel(
            logo_frame,
            text="🦷",
            font=ctk.CTkFont(size=24)
        )
        logo_icon.pack(side="left", padx=(0, 10))
        
        welcome_label = ctk.CTkLabel(
            logo_frame,
            text=f"{self.session.get_user_name()}님 환영합니다!",
            font=Theme.get_font('subtitle'),
            text_color="white"
        )
        welcome_label.pack(side="left")
        
        # 우측 사용자 정보 영역
        user_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        user_frame.pack(side="right", padx=20, pady=10)
        
        role_label = ctk.CTkLabel(
            user_frame,
            text="관리자" if self.session.is_admin() else "직원",
            font=Theme.get_font('caption'),
            text_color=Theme.COLORS['accent']
        )
        role_label.pack(side="right", padx=(10, 0))
        
        logout_button = ctk.CTkButton(
            user_frame,
            text="로그아웃",
            command=self.logout,
            width=80,
            height=32,
            font=Theme.get_font('body'),
            fg_color=Theme.COLORS['secondary'],
            hover_color=Theme.COLORS['primary_hover'],
            corner_radius=6
        )
        logout_button.pack(side="right")
        
        # 사이드바 - 새로운 디자인
        sidebar_frame = ctk.CTkFrame(
            self, 
            width=220, 
            fg_color=Theme.COLORS['bg_card'],
            corner_radius=12,
            border_width=1,
            border_color=Theme.COLORS['medium_gray']
        )
        sidebar_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=10)
        sidebar_frame.grid_propagate(False)
        
        # 사이드바 제목
        sidebar_title = ctk.CTkLabel(
            sidebar_frame,
            text="메뉴",
            font=Theme.get_font('header'),
            text_color=Theme.COLORS['primary']
        )
        sidebar_title.pack(pady=(20, 10))
        
        # 구분선
        separator = ctk.CTkFrame(sidebar_frame, height=2, fg_color=Theme.COLORS['medium_gray'])
        separator.pack(fill="x", padx=20, pady=(0, 20))
        
        self.nav_buttons = []
        
        # 메뉴 아이콘과 함께
        leave_btn = ctk.CTkButton(
            sidebar_frame,
            text="📋 연차 관리",
            command=lambda: self.show_view("leave_management"),
            width=180,
            height=40,
            font=Theme.get_font('body_bold'),
            fg_color="transparent",
            text_color=Theme.COLORS['text_primary'],
            hover_color=Theme.COLORS['accent'],
            corner_radius=8,
            anchor="w"
        )
        leave_btn.pack(padx=20, pady=(0, 8))
        self.nav_buttons.append(("leave_management", leave_btn))
        
        calendar_btn = ctk.CTkButton(
            sidebar_frame,
            text="📅 달력 보기",
            command=lambda: self.show_view("calendar"),
            width=180,
            height=40,
            font=Theme.get_font('body_bold'),
            fg_color="transparent",
            text_color=Theme.COLORS['text_primary'],
            hover_color=Theme.COLORS['accent'],
            corner_radius=8,
            anchor="w"
        )
        calendar_btn.pack(padx=20, pady=(0, 8))
        self.nav_buttons.append(("calendar", calendar_btn))
        
        if self.session.is_admin():
            # 관리자 섹션 구분
            admin_separator = ctk.CTkFrame(sidebar_frame, height=1, fg_color=Theme.COLORS['light_gray'])
            admin_separator.pack(fill="x", padx=20, pady=(10, 15))
            
            admin_label = ctk.CTkLabel(
                sidebar_frame,
                text="관리자 메뉴",
                font=Theme.get_font('caption'),
                text_color=Theme.COLORS['text_secondary']
            )
            admin_label.pack(pady=(0, 10))
            
            admin_overview_btn = ctk.CTkButton(
                sidebar_frame,
                text="👥 전체 연차 현황",
                command=lambda: self.show_view("admin_overview"),
                width=180,
                height=40,
                font=Theme.get_font('body_bold'),
                fg_color="transparent",
                text_color=Theme.COLORS['text_primary'],
                hover_color=Theme.COLORS['accent'],
                corner_radius=8,
                anchor="w"
            )
            admin_overview_btn.pack(padx=20, pady=(0, 8))
            self.nav_buttons.append(("admin_overview", admin_overview_btn))
            
            employee_btn = ctk.CTkButton(
                sidebar_frame,
                text="👤 직원 관리",
                command=lambda: self.show_view("employee_management"),
                width=180,
                height=40,
                font=Theme.get_font('body_bold'),
                fg_color="transparent",
                text_color=Theme.COLORS['text_primary'],
                hover_color=Theme.COLORS['accent'],
                corner_radius=8,
                anchor="w"
            )
            employee_btn.pack(padx=20, pady=(0, 8))
            self.nav_buttons.append(("employee_management", employee_btn))
            
            common_leave_btn = ctk.CTkButton(
                sidebar_frame,
                text="🗓️ 공통 연차 관리",
                command=lambda: self.show_view("common_leave"),
                width=180,
                height=40,
                font=Theme.get_font('body_bold'),
                fg_color="transparent",
                text_color=Theme.COLORS['text_primary'],
                hover_color=Theme.COLORS['accent'],
                corner_radius=8,
                anchor="w"
            )
            common_leave_btn.pack(padx=20, pady=(0, 8))
            self.nav_buttons.append(("common_leave", common_leave_btn))
        
        # 통계 섹션
        stats_separator = ctk.CTkFrame(sidebar_frame, height=1, fg_color=Theme.COLORS['light_gray'])
        stats_separator.pack(fill="x", padx=20, pady=(10, 15))
        
        stats_btn = ctk.CTkButton(
            sidebar_frame,
            text="📊 통계",
            command=lambda: self.show_view("statistics"),
            width=180,
            height=40,
            font=Theme.get_font('body_bold'),
            fg_color="transparent",
            text_color=Theme.COLORS['text_primary'],
            hover_color=Theme.COLORS['accent'],
            corner_radius=8,
            anchor="w"
        )
        stats_btn.pack(padx=20, pady=(0, 8))
        self.nav_buttons.append(("statistics", stats_btn))
        
        # 컨텐츠 영역 - 카드 스타일
        self.content_frame = ctk.CTkFrame(
            self,
            fg_color=Theme.COLORS['bg_card'],
            corner_radius=12,
            border_width=1,
            border_color=Theme.COLORS['medium_gray']
        )
        self.content_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=10)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        self.views = {}
        self.current_view = None
        
        self.show_view("leave_management")
    
    def show_view(self, view_name):
        # 활성 메뉴 스타일 적용
        for name, button in self.nav_buttons:
            if name == view_name:
                button.configure(
                    fg_color=Theme.COLORS['primary'],
                    text_color="white",
                    hover_color=Theme.COLORS['primary_hover']
                )
            else:
                button.configure(
                    fg_color="transparent",
                    text_color=Theme.COLORS['text_primary'],
                    hover_color=Theme.COLORS['accent']
                )
        
        if self.current_view:
            self.current_view.grid_forget()
        
        if view_name not in self.views:
            try:
                if view_name == "leave_management":
                    from views.leave_management_view import LeaveManagementView
                    self.views[view_name] = LeaveManagementView(self.content_frame)
                elif view_name == "admin_overview":
                    from views.admin_leave_overview import AdminLeaveOverview
                    self.views[view_name] = AdminLeaveOverview(self.content_frame)
                elif view_name == "employee_management":
                    from views.employee_management_view import EmployeeManagementView
                    self.views[view_name] = EmployeeManagementView(self.content_frame)
                elif view_name == "calendar":
                    from views.calendar_view import CalendarView
                    self.views[view_name] = CalendarView(self.content_frame)
                elif view_name == "statistics":
                    from views.statistics_view import StatisticsView
                    self.views[view_name] = StatisticsView(self.content_frame)
                elif view_name == "common_leave":
                    from views.common_leave_view import CommonLeaveView
                    self.views[view_name] = CommonLeaveView(self.content_frame)
            except Exception as e:
                print(f"뷰 로드 오류 ({view_name}): {e}")
                messagebox.showerror("오류", f"화면을 불러올 수 없습니다: {view_name}")
                return
        
        self.current_view = self.views[view_name]
        self.current_view.grid(row=0, column=0, sticky="nsew")
        
        if hasattr(self.current_view, 'refresh'):
            self.current_view.refresh()
    
    def logout(self):
        if messagebox.askyesno("로그아웃", "정말 로그아웃하시겠습니까?"):
            self.session.logout()
            self.on_logout()