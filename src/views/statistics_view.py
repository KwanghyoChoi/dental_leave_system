import customtkinter as ctk
from datetime import datetime
from models.database import Database
from utils.session import Session

class StatisticsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = Database()
        self.session = Session()
        
        self.setup_ui()
        self.load_statistics()
    
    def setup_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(
            self,
            text="연차 사용 통계",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        self.stats_frame = ctk.CTkScrollableFrame(self, width=900, height=600)
        self.stats_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
    
    def load_statistics(self):
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        current_year = datetime.now().year
        
        year_label = ctk.CTkLabel(
            self.stats_frame,
            text=f"{current_year}년 연차 사용 현황",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        year_label.pack(pady=(0, 20))
        
        if self.session.is_admin():
            self.show_all_employees_stats(current_year)
        else:
            self.show_personal_stats(current_year)
    
    def show_personal_stats(self, year):
        employee = self.db.get_employee_by_id(self.session.get_user_id())
        leaves = self.db.get_employee_leaves(self.session.get_user_id(), year)
        common_leaves = self.db.get_employee_common_leaves(self.session.get_user_id(), year)
        
        # 연차 통계 계산
        total_days = 0
        leave_counts = {"연차": 0, "반차(오전)": 0, "반차(오후)": 0, "병가": 0, "경조사": 0}
        
        for leave in leaves:
            leave_type = leave['leave_type']
            if leave_type in leave_counts:
                leave_counts[leave_type] += 1
                if leave_type == "연차":
                    total_days += 1
                elif "반차" in leave_type:
                    total_days += 0.5
        
        # 공통 연차 일수 계산
        common_leave_days = sum(cl['deduct_days'] for cl in common_leaves)
        total_used_days = total_days + common_leave_days
        remaining_days = employee['annual_leave_days'] - total_used_days
        usage_rate = (total_used_days / employee['annual_leave_days'] * 100) if employee['annual_leave_days'] > 0 else 0
        
        # 요약 정보
        info_frame = ctk.CTkFrame(self.stats_frame)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_text = f"총 연차: {employee['annual_leave_days']}일\n"
        info_text += f"사용 연차: {total_used_days:.1f}일 (개인: {total_days}일, 공통: {common_leave_days:.1f}일)\n"
        info_text += f"잔여 연차: {remaining_days:.1f}일\n"
        info_text += f"사용률: {usage_rate:.1f}%"
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=14),
            justify="left"
        )
        info_label.pack(pady=10)
        
        # 개인 연차 상세 내역
        personal_frame = ctk.CTkFrame(self.stats_frame)
        personal_frame.pack(fill="x", padx=20, pady=10)
        
        personal_label = ctk.CTkLabel(
            personal_frame,
            text="개인 연차 사용 내역",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        personal_label.pack(pady=(10, 5))
        
        if leaves:
            # 테이블 헤더
            header_frame = ctk.CTkFrame(personal_frame)
            header_frame.pack(fill="x", padx=10, pady=5)
            
            headers = ["날짜", "종류", "사유"]
            for i, header in enumerate(headers):
                label = ctk.CTkLabel(
                    header_frame,
                    text=header,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    width=150 if i < 2 else 300
                )
                label.grid(row=0, column=i, padx=5, sticky="w")
            
            # 개인 연차 목록
            for idx, leave in enumerate(leaves):
                row_frame = ctk.CTkFrame(personal_frame)
                row_frame.pack(fill="x", padx=10, pady=2)
                
                date_label = ctk.CTkLabel(row_frame, text=leave['leave_date'], width=150)
                date_label.grid(row=0, column=0, padx=5, sticky="w")
                
                type_label = ctk.CTkLabel(row_frame, text=leave['leave_type'], width=150)
                type_label.grid(row=0, column=1, padx=5, sticky="w")
                
                reason_label = ctk.CTkLabel(row_frame, text=leave['reason'] or "-", width=300)
                reason_label.grid(row=0, column=2, padx=5, sticky="w")
        else:
            no_data_label = ctk.CTkLabel(
                personal_frame,
                text="사용한 개인 연차가 없습니다.",
                text_color="gray"
            )
            no_data_label.pack(pady=10)
        
        # 공통 연차 상세 내역
        common_frame = ctk.CTkFrame(self.stats_frame)
        common_frame.pack(fill="x", padx=20, pady=10)
        
        common_label = ctk.CTkLabel(
            common_frame,
            text="공통 연차 적용 내역",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        common_label.pack(pady=(10, 5))
        
        if common_leaves:
            # 테이블 헤더
            header_frame = ctk.CTkFrame(common_frame)
            header_frame.pack(fill="x", padx=10, pady=5)
            
            headers = ["연차명", "기간", "실제휴무", "차감일수", "메모"]
            widths = [150, 200, 80, 80, 200]
            for i, (header, width) in enumerate(zip(headers, widths)):
                label = ctk.CTkLabel(
                    header_frame,
                    text=header,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    width=width
                )
                label.grid(row=0, column=i, padx=5, sticky="w")
            
            # 공통 연차 목록
            for idx, cl in enumerate(common_leaves):
                row_frame = ctk.CTkFrame(common_frame)
                row_frame.pack(fill="x", padx=10, pady=2)
                
                name_label = ctk.CTkLabel(row_frame, text=cl['leave_name'], width=150)
                name_label.grid(row=0, column=0, padx=5, sticky="w")
                
                period_label = ctk.CTkLabel(
                    row_frame, 
                    text=f"{cl['start_date']} ~ {cl['end_date']}", 
                    width=200
                )
                period_label.grid(row=0, column=1, padx=5, sticky="w")
                
                actual_label = ctk.CTkLabel(row_frame, text=str(cl['actual_days']), width=80)
                actual_label.grid(row=0, column=2, padx=5, sticky="w")
                
                deduct_label = ctk.CTkLabel(row_frame, text=str(cl['deduct_days']), width=80)
                deduct_label.grid(row=0, column=3, padx=5, sticky="w")
                
                memo_label = ctk.CTkLabel(row_frame, text=cl['memo'] or "-", width=200)
                memo_label.grid(row=0, column=4, padx=5, sticky="w")
        else:
            no_data_label = ctk.CTkLabel(
                common_frame,
                text="적용된 공통 연차가 없습니다.",
                text_color="gray"
            )
            no_data_label.pack(pady=10)
        
        # 월별 사용 현황
        monthly_frame = ctk.CTkFrame(self.stats_frame)
        monthly_frame.pack(fill="x", padx=20, pady=10)
        
        monthly_label = ctk.CTkLabel(
            monthly_frame,
            text="월별 사용 현황",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        monthly_label.pack(pady=(10, 5))
        
        monthly_usage = {i: 0 for i in range(1, 13)}
        for leave in leaves:
            leave_date = datetime.strptime(leave['leave_date'], '%Y-%m-%d')
            if leave['leave_type'] == '연차':
                monthly_usage[leave_date.month] += 1
            elif '반차' in leave['leave_type']:
                monthly_usage[leave_date.month] += 0.5
        
        for month, days in monthly_usage.items():
            if days > 0:
                month_label = ctk.CTkLabel(
                    monthly_frame,
                    text=f"{month}월: {days}일",
                    font=ctk.CTkFont(size=12)
                )
                month_label.pack(pady=2)
    
    def show_all_employees_stats(self, year):
        employees = self.db.get_all_employees()
        
        summary_frame = ctk.CTkFrame(self.stats_frame)
        summary_frame.pack(fill="x", padx=20, pady=10)
        
        summary_label = ctk.CTkLabel(
            summary_frame,
            text="전체 직원 연차 현황",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        summary_label.pack(pady=(10, 5))
        
        total_allocated = 0
        total_used_sum = 0
        
        for emp in employees:
            emp_frame = ctk.CTkFrame(self.stats_frame)
            emp_frame.pack(fill="x", padx=20, pady=5)
            
            leaves = self.db.get_employee_leaves(emp['id'], year)
            common_leaves = self.db.get_employee_common_leaves(emp['id'], year)
            
            # 개인 연차 계산
            personal_days = 0
            for leave in leaves:
                if leave['leave_type'] == '연차':
                    personal_days += 1
                elif '반차' in leave['leave_type']:
                    personal_days += 0.5
            
            # 공통 연차 계산
            common_days = sum(cl['deduct_days'] for cl in common_leaves)
            total_used = personal_days + common_days
            remaining = emp['annual_leave_days'] - total_used
            usage_rate = (total_used / emp['annual_leave_days'] * 100) if emp['annual_leave_days'] > 0 else 0
            
            total_allocated += emp['annual_leave_days']
            total_used_sum += total_used
            
            emp_info = f"{emp['name']} ({emp['position'] or '직원'})\n"
            emp_info += f"할당: {emp['annual_leave_days']}일 | "
            emp_info += f"사용: {total_used:.1f}일 (개인: {personal_days}, 공통: {common_days:.1f}) | "
            emp_info += f"잔여: {remaining:.1f}일 | "
            emp_info += f"사용률: {usage_rate:.1f}%"
            
            emp_label = ctk.CTkLabel(
                emp_frame,
                text=emp_info,
                font=ctk.CTkFont(size=12),
                justify="left"
            )
            emp_label.pack(pady=5, padx=10, anchor="w")
            
            progress_frame = ctk.CTkFrame(emp_frame, height=10)
            progress_frame.pack(fill="x", padx=10, pady=(0, 5))
            
            if emp['annual_leave_days'] > 0:
                progress_width = int(300 * usage_rate / 100)
                progress_bar = ctk.CTkFrame(
                    progress_frame,
                    height=10,
                    width=progress_width,
                    fg_color="#4ECDC4"
                )
                progress_bar.pack(side="left")
        
        total_frame = ctk.CTkFrame(self.stats_frame)
        total_frame.pack(fill="x", padx=20, pady=20)
        
        total_usage_rate = (total_used_sum / total_allocated * 100) if total_allocated > 0 else 0
        
        total_text = f"전체 통계\n"
        total_text += f"총 할당 연차: {total_allocated}일\n"
        total_text += f"총 사용 연차: {total_used_sum:.1f}일\n"
        total_text += f"전체 사용률: {total_usage_rate:.1f}%"
        
        total_label = ctk.CTkLabel(
            total_frame,
            text=total_text,
            font=ctk.CTkFont(size=14, weight="bold"),
            justify="left"
        )
        total_label.pack(pady=10)
    
    
    def refresh(self):
        self.load_statistics()