import customtkinter as ctk
from datetime import datetime
from models.database import Database
from utils.session import Session

class AdminLeaveOverview(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = Database()
        self.session = Session()
        
        self.current_year = datetime.now().year
        self.selected_employee_id = None
        
        self.setup_ui()
        self.load_overview()
    
    def setup_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # 제목과 연도 선택
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="전체 직원 연차 현황",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left", padx=(0, 20))
        
        year_label = ctk.CTkLabel(header_frame, text="연도:")
        year_label.pack(side="left", padx=5)
        
        self.year_var = ctk.StringVar(value=str(self.current_year))
        year_combo = ctk.CTkComboBox(
            header_frame,
            values=[str(y) for y in range(2020, 2030)],
            variable=self.year_var,
            width=100,
            command=self.on_year_change
        )
        year_combo.pack(side="left", padx=5)
        
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="새로고침",
            command=self.load_overview,
            width=100
        )
        refresh_btn.pack(side="left", padx=20)
        
        # 메인 컨텐츠
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=2)
        main_frame.grid_columnconfigure(1, weight=3)
        
        # 좌측: 직원 목록
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_frame.grid_rowconfigure(1, weight=1)
        
        list_title = ctk.CTkLabel(
            left_frame,
            text="직원별 연차 요약",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        list_title.grid(row=0, column=0, padx=10, pady=10)
        
        self.employee_listbox = ctk.CTkTextbox(left_frame, width=500, height=600)
        self.employee_listbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.employee_listbox.bind("<Button-1>", self.on_employee_select)
        
        # 우측: 선택된 직원의 상세 정보
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.grid_rowconfigure(2, weight=1)
        
        detail_title = ctk.CTkLabel(
            right_frame,
            text="상세 연차 내역",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        detail_title.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.detail_info_label = ctk.CTkLabel(
            right_frame,
            text="직원을 선택하세요",
            font=ctk.CTkFont(size=14)
        )
        self.detail_info_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.detail_listbox = ctk.CTkTextbox(right_frame, width=600, height=500)
        self.detail_listbox.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")
        
        # 하단: 전체 통계
        stats_frame = ctk.CTkFrame(self)
        stats_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.stats_label.pack(pady=10)
    
    def load_overview(self):
        self.employee_listbox.configure(state="normal")
        self.employee_listbox.delete("1.0", "end")
        
        year = int(self.year_var.get())
        employees = self.db.get_all_employees()
        
        header = f"{'이름':<15} {'직책':<15} {'총연차':<8} {'사용':<8} {'잔여':<8} {'사용률':<10}\n"
        header += "-" * 80 + "\n"
        self.employee_listbox.insert("1.0", header)
        
        total_allocated = 0
        total_used = 0
        employee_stats = []
        
        for emp in employees:
            leaves = self.db.get_employee_leaves(emp['id'], year)
            
            # 개인 연차 계산
            used_days = 0
            for leave in leaves:
                if leave['leave_type'] == '연차':
                    used_days += 1
                elif '반차' in leave['leave_type']:
                    used_days += 0.5
            
            # 공통 연차 계산
            common_leaves = self.db.get_common_leaves()
            for common_leave in common_leaves:
                leave_employees = self.db.get_common_leave_employees(common_leave['id'])
                if any(le['id'] == emp['id'] for le in leave_employees):
                    # 연도 확인
                    start_date = datetime.strptime(common_leave['start_date'], '%Y-%m-%d')
                    if start_date.year == year:
                        used_days += common_leave['deduct_days']
            
            remaining = emp['annual_leave_days'] - used_days
            usage_rate = (used_days / emp['annual_leave_days'] * 100) if emp['annual_leave_days'] > 0 else 0
            
            line = f"{emp['name']:<15} {emp['position'] or '-':<15} "
            line += f"{emp['annual_leave_days']:<8} {used_days:<8.1f} {remaining:<8.1f} "
            line += f"{usage_rate:<10.1f}%\n"
            
            self.employee_listbox.insert("end", line)
            
            total_allocated += emp['annual_leave_days']
            total_used += used_days
            
            employee_stats.append({
                'id': emp['id'],
                'name': emp['name'],
                'used': used_days,
                'remaining': remaining,
                'rate': usage_rate
            })
        
        self.employee_listbox.configure(state="disabled")
        
        # 전체 통계 업데이트
        total_remaining = total_allocated - total_used
        total_rate = (total_used / total_allocated * 100) if total_allocated > 0 else 0
        
        stats_text = f"{year}년 전체 통계: "
        stats_text += f"총 할당 {total_allocated}일 | "
        stats_text += f"총 사용 {total_used:.1f}일 | "
        stats_text += f"총 잔여 {total_remaining:.1f}일 | "
        stats_text += f"평균 사용률 {total_rate:.1f}%"
        
        self.stats_label.configure(text=stats_text)
    
    def on_employee_select(self, event):
        try:
            index = self.employee_listbox.index("@%s,%s" % (event.x, event.y))
            line_start = f"{index.split('.')[0]}.0"
            line_end = f"{index.split('.')[0]}.end"
            line_text = self.employee_listbox.get(line_start, line_end)
            
            if line_text and not line_text.startswith("이름") and not line_text.startswith("-"):
                # 이름으로 직원 찾기
                name = line_text.split()[0]
                employees = self.db.get_all_employees()
                
                for emp in employees:
                    if emp['name'] == name:
                        self.show_employee_detail(emp)
                        break
        except Exception as e:
            pass
    
    def show_employee_detail(self, employee):
        self.selected_employee_id = employee['id']
        year = int(self.year_var.get())
        
        # 정보 라벨 업데이트
        info_text = f"{employee['name']} ({employee['position'] or '직원'}) - "
        info_text += f"입사일: {employee['hire_date']} | "
        info_text += f"연차: {employee['annual_leave_days']}일"
        self.detail_info_label.configure(text=info_text)
        
        # 상세 내역 표시
        self.detail_listbox.configure(state="normal")
        self.detail_listbox.delete("1.0", "end")
        
        # 개인 연차 내역
        self.detail_listbox.insert("end", f"=== {year}년 개인 연차 사용 내역 ===\n\n")
        
        leaves = self.db.get_employee_leaves(employee['id'], year)
        
        if leaves:
            header = f"{'날짜':<15} {'종류':<15} {'사유':<30}\n"
            header += "-" * 60 + "\n"
            self.detail_listbox.insert("end", header)
            
            for leave in leaves:
                line = f"{leave['leave_date']:<15} {leave['leave_type']:<15} "
                line += f"{leave['reason'] or '-':<30}\n"
                self.detail_listbox.insert("end", line)
        else:
            self.detail_listbox.insert("end", "사용 내역이 없습니다.\n")
        
        # 공통 연차 내역
        self.detail_listbox.insert("end", f"\n\n=== {year}년 공통 연차 내역 ===\n\n")
        
        common_leaves = self.db.get_common_leaves()
        has_common = False
        
        for common_leave in common_leaves:
            leave_employees = self.db.get_common_leave_employees(common_leave['id'])
            if any(le['id'] == employee['id'] for le in leave_employees):
                start_date = datetime.strptime(common_leave['start_date'], '%Y-%m-%d')
                if start_date.year == year:
                    has_common = True
                    line = f"{common_leave['leave_name']}: "
                    line += f"{common_leave['start_date']} ~ {common_leave['end_date']} "
                    line += f"(차감: {common_leave['deduct_days']}일)\n"
                    self.detail_listbox.insert("end", line)
        
        if not has_common:
            self.detail_listbox.insert("end", "적용된 공통 연차가 없습니다.\n")
        
        # 월별 분석
        self.detail_listbox.insert("end", "\n\n=== 월별 사용 현황 ===\n\n")
        monthly_count = {}
        
        for leave in leaves:
            month = datetime.strptime(leave['leave_date'], '%Y-%m-%d').month
            if month not in monthly_count:
                monthly_count[month] = 0
            
            if leave['leave_type'] == '연차':
                monthly_count[month] += 1
            elif '반차' in leave['leave_type']:
                monthly_count[month] += 0.5
        
        for month in range(1, 13):
            if month in monthly_count and monthly_count[month] > 0:
                self.detail_listbox.insert("end", f"{month}월: {monthly_count[month]}일\n")
        
        self.detail_listbox.configure(state="disabled")
    
    def on_year_change(self, value):
        self.current_year = int(value)
        self.load_overview()
        if self.selected_employee_id:
            employees = self.db.get_all_employees()
            for emp in employees:
                if emp['id'] == self.selected_employee_id:
                    self.show_employee_detail(emp)
                    break
    
    def refresh(self):
        self.load_overview()