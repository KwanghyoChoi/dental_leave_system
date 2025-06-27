import customtkinter as ctk
import calendar
from datetime import datetime, date, timedelta
from models.database import Database
from utils.session import Session

class CalendarView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = Database()
        self.session = Session()
        
        self.current_date = datetime.now()
        self.setup_ui()
        self.update_calendar()
    
    def setup_ui(self):
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(
            self,
            text="연차 달력",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        nav_frame = ctk.CTkFrame(self)
        nav_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        prev_button = ctk.CTkButton(
            nav_frame,
            text="◀",
            command=self.prev_month,
            width=40
        )
        prev_button.pack(side="left", padx=5)
        
        self.month_label = ctk.CTkLabel(
            nav_frame,
            text="",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.month_label.pack(side="left", expand=True)
        
        next_button = ctk.CTkButton(
            nav_frame,
            text="▶",
            command=self.next_month,
            width=40
        )
        next_button.pack(side="right", padx=5)
        
        today_button = ctk.CTkButton(
            nav_frame,
            text="오늘",
            command=self.go_to_today,
            width=60
        )
        today_button.pack(side="right", padx=5)
        
        self.calendar_frame = ctk.CTkScrollableFrame(self, width=900, height=500)
        self.calendar_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        legend_frame = ctk.CTkFrame(self)
        legend_frame.grid(row=3, column=0, padx=20, pady=(0, 20))
        
        legend_items = [
            ("나의 연차", "#FF6B6B"),
            ("다른 직원 연차", "#4ECDC4"),
            ("공통 연차", "#FFE66D")
        ]
        
        for text, color in legend_items:
            item_frame = ctk.CTkFrame(legend_frame)
            item_frame.pack(side="left", padx=10)
            
            color_box = ctk.CTkLabel(
                item_frame,
                text="",
                width=20,
                height=20,
                fg_color=color
            )
            color_box.pack(side="left", padx=(0, 5))
            
            label = ctk.CTkLabel(item_frame, text=text)
            label.pack(side="left")
    
    def prev_month(self):
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(
                year=self.current_date.year - 1, month=12
            )
        else:
            self.current_date = self.current_date.replace(
                month=self.current_date.month - 1
            )
        self.update_calendar()
    
    def next_month(self):
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(
                year=self.current_date.year + 1, month=1
            )
        else:
            self.current_date = self.current_date.replace(
                month=self.current_date.month + 1
            )
        self.update_calendar()
    
    def go_to_today(self):
        self.current_date = datetime.now()
        self.update_calendar()
    
    def update_calendar(self):
        try:
            for widget in self.calendar_frame.winfo_children():
                widget.destroy()
            
            self.month_label.configure(
                text=f"{self.current_date.year}년 {self.current_date.month}월"
            )
            
            days = ['월', '화', '수', '목', '금', '토', '일']
            for i, day in enumerate(days):
                label = ctk.CTkLabel(
                    self.calendar_frame,
                    text=day,
                    font=ctk.CTkFont(weight="bold")
                )
                label.grid(row=0, column=i, padx=2, pady=2)
            
            cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
            
            my_leaves = self.get_my_leaves_for_month()
            other_leaves = self.get_other_leaves_for_month()
            common_leaves = self.get_common_leaves_for_month()
            
            today = date.today()
            
            for week_num, week in enumerate(cal):
                for day_num, day in enumerate(week):
                    if day == 0:
                        continue
                    
                    current_date = date(self.current_date.year, self.current_date.month, day)
                    
                    day_frame = ctk.CTkFrame(
                        self.calendar_frame,
                        width=100,
                        height=80
                    )
                    day_frame.grid(row=week_num+1, column=day_num, padx=2, pady=2, sticky="nsew")
                    day_frame.grid_propagate(False)
                    
                    if current_date == today:
                        day_frame.configure(fg_color=("gray85", "gray25"))
                    
                    day_label = ctk.CTkLabel(
                        day_frame,
                        text=str(day),
                        font=ctk.CTkFont(size=14, weight="bold")
                    )
                    day_label.pack(pady=(5, 2))
                    
                    if current_date in my_leaves:
                        leave_label = ctk.CTkLabel(
                            day_frame,
                            text=my_leaves[current_date],
                            font=ctk.CTkFont(size=10),
                            text_color="#FF6B6B"
                        )
                        leave_label.pack()
                    
                    if current_date in other_leaves:
                        count_label = ctk.CTkLabel(
                            day_frame,
                            text=f"{other_leaves[current_date]}명",
                            font=ctk.CTkFont(size=10),
                            text_color="#4ECDC4"
                        )
                        count_label.pack()
                    
                    if current_date in common_leaves:
                        common_label = ctk.CTkLabel(
                            day_frame,
                            text=common_leaves[current_date],
                            font=ctk.CTkFont(size=10),
                            text_color="#FFE66D"
                        )
                        common_label.pack()
            
            for i in range(7):
                self.calendar_frame.grid_columnconfigure(i, weight=1)
            for i in range(len(cal) + 1):
                self.calendar_frame.grid_rowconfigure(i, weight=1)
        except Exception as e:
            print(f"캘린더 업데이트 오류: {e}")
            # 오류 시 기본 메시지 표시
            error_label = ctk.CTkLabel(
                self.calendar_frame,
                text=f"캘린더를 불러오는 중 오류가 발생했습니다.\n{str(e)}",
                text_color="red"
            )
            error_label.grid(row=0, column=0, columnspan=7, pady=50)
    
    def get_my_leaves_for_month(self):
        try:
            leaves = self.db.get_employee_leaves(
                self.session.get_user_id(),
                self.current_date.year
            )
            
            result = {}
            for leave in leaves:
                leave_date = datetime.strptime(leave['leave_date'], '%Y-%m-%d').date()
                if leave_date.year == self.current_date.year and leave_date.month == self.current_date.month:
                    leave_type = leave['leave_type']
                    if "반차" in leave_type:
                        result[leave_date] = "반차"
                    else:
                        result[leave_date] = leave_type[:2]
            
            return result
        except Exception as e:
            print(f"개인연차 조회 오류: {e}")
            return {}
    
    def get_other_leaves_for_month(self):
        try:
            all_employees = self.db.get_all_employees()
            my_id = self.session.get_user_id()
            
            result = {}
            for emp in all_employees:
                if emp['id'] == my_id:
                    continue
                
                leaves = self.db.get_employee_leaves(emp['id'], self.current_date.year)
                for leave in leaves:
                    leave_date = datetime.strptime(leave['leave_date'], '%Y-%m-%d').date()
                    if leave_date.year == self.current_date.year and leave_date.month == self.current_date.month:
                        result[leave_date] = result.get(leave_date, 0) + 1
            
            return result
        except Exception as e:
            print(f"다른 직원 연차 조회 오류: {e}")
            return {}
    
    def get_common_leaves_for_month(self):
        try:
            # 관리자는 모든 공통연차를 볼 수 있도록 함
            if self.session.is_admin():
                # 관리자: 모든 공통연차 표시
                all_common_leaves = self.db.get_common_leaves()
                common_leaves = []
                for leave in all_common_leaves:
                    start_year = datetime.strptime(leave['start_date'], '%Y-%m-%d').year
                    if start_year == self.current_date.year:
                        common_leaves.append(leave)
            else:
                # 일반 직원: 해당 직원에게 적용된 공통연차만 가져오기
                if hasattr(self.db, 'get_employee_common_leaves'):
                    common_leaves = self.db.get_employee_common_leaves(
                        self.session.get_user_id(), 
                        self.current_date.year
                    )
                else:
                    # 기존 방식: 모든 공통연차 가져온 후 필터링
                    all_common_leaves = self.db.get_common_leaves()
                    common_leaves = []
                    for leave in all_common_leaves:
                        # 이 직원에게 적용되는지 확인
                        employees = self.db.get_common_leave_employees(leave['id'])
                        if any(emp['id'] == self.session.get_user_id() for emp in employees):
                            start_year = datetime.strptime(leave['start_date'], '%Y-%m-%d').year
                            if start_year == self.current_date.year:
                                common_leaves.append(leave)
            
            result = {}
            for leave in common_leaves:
                start_date = datetime.strptime(leave['start_date'], '%Y-%m-%d').date()
                end_date = datetime.strptime(leave['end_date'], '%Y-%m-%d').date()
                
                current = start_date
                while current <= end_date:
                    if current.year == self.current_date.year and current.month == self.current_date.month:
                        result[current] = "공통"
                    current = current + timedelta(days=1)
            
            return result
        except Exception as e:
            print(f"공통연차 조회 오류: {e}")
            return {}
    
    def refresh(self):
        self.update_calendar()