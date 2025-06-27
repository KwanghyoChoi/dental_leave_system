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
        
        stats = self.calculate_leave_stats(leaves, employee['annual_leave_days'])
        
        info_frame = ctk.CTkFrame(self.stats_frame)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_text = f"총 연차: {employee['annual_leave_days']}일\n"
        info_text += f"사용 연차: {stats['used_days']}일\n"
        info_text += f"잔여 연차: {stats['remaining_days']}일\n"
        info_text += f"사용률: {stats['usage_rate']:.1f}%"
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=14),
            justify="left"
        )
        info_label.pack(pady=10)
        
        detail_frame = ctk.CTkFrame(self.stats_frame)
        detail_frame.pack(fill="x", padx=20, pady=10)
        
        detail_label = ctk.CTkLabel(
            detail_frame,
            text="상세 내역",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        detail_label.pack(pady=(10, 5))
        
        for leave_type, count in stats['type_counts'].items():
            if count > 0:
                type_label = ctk.CTkLabel(
                    detail_frame,
                    text=f"{leave_type}: {count}회",
                    font=ctk.CTkFont(size=12)
                )
                type_label.pack(pady=2)
        
        monthly_frame = ctk.CTkFrame(self.stats_frame)
        monthly_frame.pack(fill="x", padx=20, pady=10)
        
        monthly_label = ctk.CTkLabel(
            monthly_frame,
            text="월별 사용 현황",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        monthly_label.pack(pady=(10, 5))
        
        for month, days in stats['monthly_usage'].items():
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
        total_used = 0
        
        for emp in employees:
            emp_frame = ctk.CTkFrame(self.stats_frame)
            emp_frame.pack(fill="x", padx=20, pady=5)
            
            leaves = self.db.get_employee_leaves(emp['id'], year)
            stats = self.calculate_leave_stats(leaves, emp['annual_leave_days'])
            
            total_allocated += emp['annual_leave_days']
            total_used += stats['used_days']
            
            emp_info = f"{emp['name']} ({emp['position'] or '직원'})\n"
            emp_info += f"할당: {emp['annual_leave_days']}일 | "
            emp_info += f"사용: {stats['used_days']}일 | "
            emp_info += f"잔여: {stats['remaining_days']}일 | "
            emp_info += f"사용률: {stats['usage_rate']:.1f}%"
            
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
                progress_width = int(300 * stats['usage_rate'] / 100)
                progress_bar = ctk.CTkFrame(
                    progress_frame,
                    height=10,
                    width=progress_width,
                    fg_color="#4ECDC4"
                )
                progress_bar.pack(side="left")
        
        total_frame = ctk.CTkFrame(self.stats_frame)
        total_frame.pack(fill="x", padx=20, pady=20)
        
        total_usage_rate = (total_used / total_allocated * 100) if total_allocated > 0 else 0
        
        total_text = f"전체 통계\n"
        total_text += f"총 할당 연차: {total_allocated}일\n"
        total_text += f"총 사용 연차: {total_used}일\n"
        total_text += f"전체 사용률: {total_usage_rate:.1f}%"
        
        total_label = ctk.CTkLabel(
            total_frame,
            text=total_text,
            font=ctk.CTkFont(size=14, weight="bold"),
            justify="left"
        )
        total_label.pack(pady=10)
    
    def calculate_leave_stats(self, leaves, annual_days):
        stats = {
            'used_days': 0,
            'remaining_days': annual_days,
            'usage_rate': 0,
            'type_counts': {
                '연차': 0,
                '반차(오전)': 0,
                '반차(오후)': 0,
                '병가': 0,
                '경조사': 0
            },
            'monthly_usage': {i: 0 for i in range(1, 13)}
        }
        
        for leave in leaves:
            leave_type = leave['leave_type']
            leave_date = datetime.strptime(leave['leave_date'], '%Y-%m-%d')
            
            if leave_type in stats['type_counts']:
                stats['type_counts'][leave_type] += 1
            
            if leave_type == '연차':
                stats['used_days'] += 1
                stats['monthly_usage'][leave_date.month] += 1
            elif '반차' in leave_type:
                stats['used_days'] += 0.5
                stats['monthly_usage'][leave_date.month] += 0.5
        
        common_leaves = self.db.get_common_leaves()
        for common_leave in common_leaves:
            employees = self.db.get_common_leave_employees(common_leave['id'])
            if any(emp['id'] == self.session.get_user_id() for emp in employees):
                stats['used_days'] += common_leave['deduct_days']
        
        stats['remaining_days'] = annual_days - stats['used_days']
        stats['usage_rate'] = (stats['used_days'] / annual_days * 100) if annual_days > 0 else 0
        
        return stats
    
    def refresh(self):
        self.load_statistics()