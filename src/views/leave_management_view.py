import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime, date
from models.database import Database
from utils.session import Session

class LeaveManagementView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = Database()
        self.session = Session()
        
        self.setup_ui()
        self.load_leaves()
    
    def setup_ui(self):
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(
            self,
            text="개인 연차 관리",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        date_label = ctk.CTkLabel(input_frame, text="날짜:")
        date_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.date_entry = DateEntry(
            input_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd'
        )
        self.date_entry.grid(row=0, column=1, padx=10, pady=10)
        
        type_label = ctk.CTkLabel(input_frame, text="연차 종류:")
        type_label.grid(row=0, column=2, padx=10, pady=10)
        
        self.type_combo = ctk.CTkComboBox(
            input_frame,
            values=["연차", "반차(오전)", "반차(오후)", "병가", "경조사"],
            width=150
        )
        self.type_combo.set("연차")
        self.type_combo.grid(row=0, column=3, padx=10, pady=10)
        
        reason_label = ctk.CTkLabel(input_frame, text="사유:")
        reason_label.grid(row=0, column=4, padx=10, pady=10)
        
        self.reason_entry = ctk.CTkEntry(input_frame, width=200)
        self.reason_entry.grid(row=0, column=5, padx=10, pady=10)
        
        add_button = ctk.CTkButton(
            input_frame,
            text="추가",
            command=self.add_leave,
            width=100
        )
        add_button.grid(row=0, column=6, padx=10, pady=10)
        
        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        self.leave_listbox = ctk.CTkTextbox(list_frame, wrap="none", width=800, height=400)
        self.leave_listbox.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        button_frame = ctk.CTkFrame(list_frame)
        button_frame.grid(row=1, column=0, pady=10)
        
        refresh_button = ctk.CTkButton(
            button_frame,
            text="새로고침",
            command=self.load_leaves,
            width=100
        )
        refresh_button.pack(side="left", padx=5)
        
        delete_button = ctk.CTkButton(
            button_frame,
            text="선택 삭제",
            command=self.delete_selected,
            width=100
        )
        delete_button.pack(side="left", padx=5)
        
        stats_frame = ctk.CTkFrame(self)
        stats_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.stats_label = ctk.CTkLabel(stats_frame, text="")
        self.stats_label.pack(pady=10)
    
    def add_leave(self):
        leave_date = self.date_entry.get_date()
        leave_type = self.type_combo.get()
        reason = self.reason_entry.get().strip()
        
        try:
            self.db.create_leave(
                self.session.get_user_id(),
                leave_date,
                leave_type,
                reason if reason else None
            )
            messagebox.showinfo("성공", "연차가 등록되었습니다.")
            self.reason_entry.delete(0, 'end')
            self.load_leaves()
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                messagebox.showerror("오류", "해당 날짜에 이미 연차가 등록되어 있습니다.")
            else:
                messagebox.showerror("오류", f"연차 등록 중 오류가 발생했습니다: {str(e)}")
    
    def load_leaves(self):
        self.leave_listbox.delete("1.0", "end")
        
        current_year = datetime.now().year
        leaves = self.db.get_employee_leaves(self.session.get_user_id(), current_year)
        
        header = f"{'날짜':<15} {'종류':<15} {'사유':<30} {'ID':<10}\n"
        header += "-" * 70 + "\n"
        self.leave_listbox.insert("1.0", header)
        
        total_days = 0
        leave_counts = {"연차": 0, "반차(오전)": 0, "반차(오후)": 0, "병가": 0, "경조사": 0}
        
        for leave in leaves:
            date_str = leave['leave_date']
            leave_type = leave['leave_type']
            reason = leave['reason'] or "-"
            leave_id = leave['id']
            
            line = f"{date_str:<15} {leave_type:<15} {reason:<30} {leave_id:<10}\n"
            self.leave_listbox.insert("end", line)
            
            if leave_type in leave_counts:
                leave_counts[leave_type] += 1
                if leave_type == "연차":
                    total_days += 1
                elif "반차" in leave_type:
                    total_days += 0.5
        
        employee = self.db.get_employee_by_id(self.session.get_user_id())
        annual_leave_days = employee['annual_leave_days']
        remaining_days = annual_leave_days - total_days
        
        stats_text = f"{current_year}년 연차 현황: "
        stats_text += f"총 {annual_leave_days}일 중 {total_days}일 사용, {remaining_days}일 남음\n"
        stats_text += f"(연차: {leave_counts['연차']}일, 반차: {leave_counts['반차(오전)']+leave_counts['반차(오후)']}회)"
        
        self.stats_label.configure(text=stats_text)
        
        self.leave_listbox.configure(state="disabled")
    
    def delete_selected(self):
        try:
            cursor_pos = self.leave_listbox.index("insert")
            line_start = f"{cursor_pos.split('.')[0]}.0"
            line_end = f"{cursor_pos.split('.')[0]}.end"
            
            line_text = self.leave_listbox.get(line_start, line_end)
            
            if line_text and not line_text.startswith("날짜") and not line_text.startswith("-"):
                parts = line_text.split()
                if len(parts) >= 4:
                    leave_id = parts[-1]
                    
                    if messagebox.askyesno("삭제 확인", "선택한 연차를 삭제하시겠습니까?"):
                        self.db.delete_leave(int(leave_id))
                        messagebox.showinfo("성공", "연차가 삭제되었습니다.")
                        self.load_leaves()
        except Exception as e:
            messagebox.showerror("오류", "연차를 선택해주세요.")
    
    def refresh(self):
        self.load_leaves()