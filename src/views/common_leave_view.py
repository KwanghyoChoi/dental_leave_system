import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
from models.database import Database
from utils.session import Session

class CommonLeaveView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = Database()
        self.session = Session()
        
        self.setup_ui()
        self.load_common_leaves()
    
    def setup_ui(self):
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(
            self,
            text="공통 연차 관리",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        name_label = ctk.CTkLabel(input_frame, text="연차명:")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.name_entry = ctk.CTkEntry(input_frame, width=150)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        start_label = ctk.CTkLabel(input_frame, text="시작일:")
        start_label.grid(row=0, column=2, padx=5, pady=5)
        
        self.start_date_entry = DateEntry(
            input_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd'
        )
        self.start_date_entry.grid(row=0, column=3, padx=5, pady=5)
        
        end_label = ctk.CTkLabel(input_frame, text="종료일:")
        end_label.grid(row=0, column=4, padx=5, pady=5)
        
        self.end_date_entry = DateEntry(
            input_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd'
        )
        self.end_date_entry.grid(row=0, column=5, padx=5, pady=5)
        
        actual_days_label = ctk.CTkLabel(input_frame, text="실제 휴무일:")
        actual_days_label.grid(row=1, column=0, padx=5, pady=5)
        
        self.actual_days_entry = ctk.CTkEntry(input_frame, width=100)
        self.actual_days_entry.grid(row=1, column=1, padx=5, pady=5)
        
        deduct_days_label = ctk.CTkLabel(input_frame, text="차감 일수:")
        deduct_days_label.grid(row=1, column=2, padx=5, pady=5)
        
        self.deduct_days_entry = ctk.CTkEntry(input_frame, width=100)
        self.deduct_days_entry.grid(row=1, column=3, padx=5, pady=5)
        
        memo_label = ctk.CTkLabel(input_frame, text="메모:")
        memo_label.grid(row=1, column=4, padx=5, pady=5)
        
        self.memo_entry = ctk.CTkEntry(input_frame, width=200)
        self.memo_entry.grid(row=1, column=5, padx=5, pady=5)
        
        employee_frame = ctk.CTkFrame(input_frame)
        employee_frame.grid(row=2, column=0, columnspan=6, pady=10)
        
        emp_label = ctk.CTkLabel(employee_frame, text="적용 직원:")
        emp_label.pack(side="left", padx=5)
        
        self.employee_vars = {}
        employees = self.db.get_all_employees()
        
        for emp in employees:
            var = ctk.BooleanVar(value=True)
            check = ctk.CTkCheckBox(
                employee_frame,
                text=emp['name'],
                variable=var
            )
            check.pack(side="left", padx=5)
            self.employee_vars[emp['id']] = var
        
        add_button = ctk.CTkButton(
            input_frame,
            text="공통 연차 추가",
            command=self.add_common_leave,
            width=150
        )
        add_button.grid(row=3, column=0, columnspan=6, pady=10)
        
        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        self.leave_listbox = ctk.CTkTextbox(list_frame, width=800, height=400)
        self.leave_listbox.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        refresh_button = ctk.CTkButton(
            list_frame,
            text="새로고침",
            command=self.load_common_leaves,
            width=100
        )
        refresh_button.grid(row=1, column=0, pady=10)
    
    def add_common_leave(self):
        try:
            name = self.name_entry.get().strip()
            start_date = self.start_date_entry.get_date()
            end_date = self.end_date_entry.get_date()
            actual_days = int(self.actual_days_entry.get())
            deduct_days = float(self.deduct_days_entry.get())
            memo = self.memo_entry.get().strip() or None
            
            if not name:
                messagebox.showwarning("입력 오류", "연차명을 입력해주세요.")
                return
            
            if start_date > end_date:
                messagebox.showwarning("입력 오류", "종료일이 시작일보다 빠를 수 없습니다.")
                return
            
            selected_employees = [
                emp_id for emp_id, var in self.employee_vars.items() if var.get()
            ]
            
            if not selected_employees:
                messagebox.showwarning("선택 오류", "최소 한 명 이상의 직원을 선택해주세요.")
                return
            
            self.db.create_common_leave(
                name, start_date, end_date, actual_days, deduct_days,
                selected_employees, self.session.get_user_id(), memo
            )
            
            messagebox.showinfo("성공", "공통 연차가 추가되었습니다.")
            self.clear_form()
            self.load_common_leaves()
            
        except ValueError:
            messagebox.showerror("입력 오류", "실제 휴무일과 차감 일수는 숫자로 입력해주세요.")
        except Exception as e:
            messagebox.showerror("오류", f"공통 연차 추가 중 오류가 발생했습니다: {str(e)}")
    
    def load_common_leaves(self):
        self.leave_listbox.delete("1.0", "end")
        
        common_leaves = self.db.get_common_leaves()
        
        header = f"{'연차명':<20} {'기간':<25} {'실제휴무':<10} {'차감일수':<10} {'등록자':<15}\n"
        header += "-" * 80 + "\n"
        self.leave_listbox.insert("1.0", header)
        
        for leave in common_leaves:
            period = f"{leave['start_date']} ~ {leave['end_date']}"
            line = f"{leave['leave_name']:<20} {period:<25} "
            line += f"{leave['actual_days']:<10} {leave['deduct_days']:<10} "
            line += f"{leave['created_by_name'] or '-':<15}\n"
            
            self.leave_listbox.insert("end", line)
            
            if leave['memo']:
                self.leave_listbox.insert("end", f"  메모: {leave['memo']}\n")
            
            employees = self.db.get_common_leave_employees(leave['id'])
            emp_names = [emp['name'] for emp in employees]
            self.leave_listbox.insert("end", f"  적용 직원: {', '.join(emp_names)}\n\n")
        
        self.leave_listbox.configure(state="disabled")
    
    def clear_form(self):
        self.name_entry.delete(0, 'end')
        self.actual_days_entry.delete(0, 'end')
        self.deduct_days_entry.delete(0, 'end')
        self.memo_entry.delete(0, 'end')
        
        for var in self.employee_vars.values():
            var.set(True)
    
    def refresh(self):
        self.load_common_leaves()