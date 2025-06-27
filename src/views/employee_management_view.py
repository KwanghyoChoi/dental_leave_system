import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from models.database import Database

class EmployeeManagementView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = Database()
        
        self.setup_ui()
        self.load_employees()
    
    def setup_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(
            self,
            text="직원 관리",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        list_frame = ctk.CTkFrame(main_frame)
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        list_frame.grid_rowconfigure(0, weight=1)
        
        self.employee_listbox = ctk.CTkTextbox(list_frame, width=400, height=500)
        self.employee_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.employee_listbox.bind("<Button-1>", self.on_employee_select)
        
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.grid(row=0, column=1, sticky="nsew")
        
        fields = [
            ("이름:", "name"),
            ("비밀번호:", "password"),
            ("입사일:", "hire_date"),
            ("연차일수:", "annual_leave_days"),
            ("직책:", "position"),
            ("전화번호:", "phone"),
            ("입사구분:", "employment_type"),
            ("메모:", "memo")
        ]
        
        self.entries = {}
        for i, (label_text, field_name) in enumerate(fields):
            label = ctk.CTkLabel(form_frame, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            
            if field_name == "password":
                entry = ctk.CTkEntry(form_frame, width=200, show="*")
            elif field_name == "memo":
                entry = ctk.CTkTextbox(form_frame, width=200, height=60)
            else:
                entry = ctk.CTkEntry(form_frame, width=200)
            
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            self.entries[field_name] = entry
        
        self.entries["hire_date"].insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entries["annual_leave_days"].insert(0, "15")
        
        admin_frame = ctk.CTkFrame(form_frame)
        admin_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        self.is_admin_var = ctk.BooleanVar()
        admin_check = ctk.CTkCheckBox(
            admin_frame,
            text="관리자 권한",
            variable=self.is_admin_var
        )
        admin_check.pack()
        
        button_frame = ctk.CTkFrame(form_frame)
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
        
        add_button = ctk.CTkButton(
            button_frame,
            text="직원 추가",
            command=self.add_employee,
            width=100
        )
        add_button.grid(row=0, column=0, padx=5)
        
        update_button = ctk.CTkButton(
            button_frame,
            text="정보 수정",
            command=self.update_employee,
            width=100
        )
        update_button.grid(row=0, column=1, padx=5)
        
        delete_button = ctk.CTkButton(
            button_frame,
            text="직원 삭제",
            command=self.delete_employee,
            width=100,
            fg_color="red",
            hover_color="darkred"
        )
        delete_button.grid(row=0, column=2, padx=5)
        
        refresh_button = ctk.CTkButton(
            button_frame,
            text="새로고침",
            command=self.load_employees,
            width=100
        )
        refresh_button.grid(row=0, column=3, padx=5)
        
        self.selected_employee_id = None
    
    def load_employees(self):
        self.employee_listbox.configure(state="normal")
        self.employee_listbox.delete("1.0", "end")
        
        employees = self.db.get_all_employees()
        
        header = f"{'ID':<5} {'이름':<20} {'직책':<15} {'권한':<10} {'입사일':<12}\n"
        header += "-" * 70 + "\n"
        self.employee_listbox.insert("1.0", header)
        
        for emp in employees:
            line = f"{emp['id']:<5} {emp['name']:<20} "
            line += f"{emp['position'] or '-':<15} {'관리자' if emp['is_admin'] else '일반':<10} "
            line += f"{emp['hire_date']:<12}\n"
            self.employee_listbox.insert("end", line)
        
        self.employee_listbox.configure(state="disabled")
    
    def add_employee(self):
        try:
            name = self.entries["name"].get().strip()
            password = self.entries["password"].get()
            hire_date = self.entries["hire_date"].get().strip()
            annual_leave_days = int(self.entries["annual_leave_days"].get())
            position = self.entries["position"].get().strip() or None
            phone = self.entries["phone"].get().strip() or None
            employment_type = self.entries["employment_type"].get().strip() or None
            memo = self.entries["memo"].get("1.0", "end").strip() or None
            is_admin = self.is_admin_var.get()
            
            if not all([name, password, hire_date]):
                messagebox.showwarning("입력 오류", "필수 항목(이름, 비밀번호, 입사일)을 모두 입력해주세요.")
                return
            
            # 이름 중복 체크
            employees = self.db.get_all_employees()
            if any(emp['name'] == name for emp in employees):
                messagebox.showerror("입력 오류", "이미 존재하는 이름입니다. 다른 이름을 사용해주세요.")
                return
            
            self.db.create_employee(
                name, password, hire_date, annual_leave_days,
                position, is_admin, None, phone, employment_type, memo
            )
            
            messagebox.showinfo("성공", "직원이 추가되었습니다.")
            self.clear_form()
            self.load_employees()
            
        except Exception as e:
            messagebox.showerror("오류", f"직원 추가 중 오류가 발생했습니다: {str(e)}")
    
    def update_employee(self):
        if not self.selected_employee_id:
            messagebox.showwarning("선택 오류", "수정할 직원을 먼저 선택해주세요.")
            return
        
        try:
            update_data = {
                'name': self.entries["name"].get().strip(),
                'hire_date': self.entries["hire_date"].get().strip(),
                'annual_leave_days': int(self.entries["annual_leave_days"].get()),
                'position': self.entries["position"].get().strip() or None,
                'phone': self.entries["phone"].get().strip() or None,
                'employment_type': self.entries["employment_type"].get().strip() or None,
                'memo': self.entries["memo"].get("1.0", "end").strip() or None,
                'is_admin': self.is_admin_var.get()
            }
            
            self.db.update_employee(self.selected_employee_id, **update_data)
            
            new_password = self.entries["password"].get()
            if new_password:
                self.db.update_password(self.selected_employee_id, new_password)
            
            messagebox.showinfo("성공", "직원 정보가 수정되었습니다.")
            self.clear_form()
            self.load_employees()
            
        except Exception as e:
            messagebox.showerror("오류", f"직원 정보 수정 중 오류가 발생했습니다: {str(e)}")
    
    def delete_employee(self):
        """선택된 직원 삭제"""
        if not self.selected_employee_id:
            messagebox.showwarning("선택 오류", "삭제할 직원을 먼저 선택해주세요.")
            return
        
        # 선택된 직원 정보 조회
        employees = self.db.get_all_employees()
        selected_employee = None
        for emp in employees:
            if emp['id'] == self.selected_employee_id:
                selected_employee = emp
                break
        
        if not selected_employee:
            messagebox.showerror("오류", "선택된 직원 정보를 찾을 수 없습니다.")
            return
        
        # 관리자 본인은 삭제할 수 없도록 보호
        if selected_employee['is_admin']:
            # 관리자 계정이 몇 개인지 확인
            admin_count = sum(1 for emp in employees if emp['is_admin'])
            if admin_count <= 1:
                messagebox.showerror("삭제 불가", "마지막 관리자 계정은 삭제할 수 없습니다.")
                return
        
        # 확인 대화상자
        confirm_msg = f"'{selected_employee['name']}' 직원을 정말 삭제하시겠습니까?\n\n"
        confirm_msg += "⚠️ 주의: 다음 데이터가 모두 삭제됩니다:\n"
        confirm_msg += "• 직원의 모든 연차 기록\n"
        confirm_msg += "• 공통연차 적용 기록\n"
        confirm_msg += "• 기타 관련 데이터\n\n"
        confirm_msg += "이 작업은 되돌릴 수 없습니다."
        
        if not messagebox.askyesno("직원 삭제 확인", confirm_msg):
            return
        
        try:
            # 직원 삭제 실행
            success = self.db.delete_employee(self.selected_employee_id)
            
            if success:
                messagebox.showinfo("성공", f"'{selected_employee['name']}' 직원이 성공적으로 삭제되었습니다.")
                self.clear_form()
                self.load_employees()
            else:
                messagebox.showerror("오류", "직원 삭제에 실패했습니다.")
                
        except Exception as e:
            messagebox.showerror("오류", f"직원 삭제 중 오류가 발생했습니다: {str(e)}")
            print(f"직원 삭제 오류: {e}")
            import traceback
            traceback.print_exc()
    
    def clear_form(self):
        for field_name, entry in self.entries.items():
            if isinstance(entry, ctk.CTkTextbox):
                entry.delete("1.0", "end")
            else:
                entry.delete(0, "end")
        
        self.entries["hire_date"].insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entries["annual_leave_days"].insert(0, "15")
        self.is_admin_var.set(False)
        self.selected_employee_id = None
    
    def on_employee_select(self, event):
        try:
            index = self.employee_listbox.index("@%s,%s" % (event.x, event.y))
            line_start = f"{index.split('.')[0]}.0"
            line_end = f"{index.split('.')[0]}.end"
            line_text = self.employee_listbox.get(line_start, line_end)
            
            if line_text and not line_text.startswith("ID") and not line_text.startswith("-"):
                parts = line_text.split()
                if len(parts) >= 3:
                    emp_id = int(parts[0])
                    
                    # 직원 정보 조회
                    employees = self.db.get_all_employees()
                    for emp in employees:
                        if emp['id'] == emp_id:
                            self.selected_employee_id = emp_id
                            # 폼에 정보 채우기
                            self.entries["name"].delete(0, "end")
                            self.entries["name"].insert(0, emp['name'])
                            self.entries["hire_date"].delete(0, "end")
                            self.entries["hire_date"].insert(0, emp['hire_date'])
                            self.entries["annual_leave_days"].delete(0, "end")
                            self.entries["annual_leave_days"].insert(0, str(emp['annual_leave_days']))
                            if emp['position']:
                                self.entries["position"].delete(0, "end")
                                self.entries["position"].insert(0, emp['position'])
                            if emp['phone']:
                                self.entries["phone"].delete(0, "end")
                                self.entries["phone"].insert(0, emp['phone'])
                            if emp['employment_type']:
                                self.entries["employment_type"].delete(0, "end")
                                self.entries["employment_type"].insert(0, emp['employment_type'])
                            if emp['memo']:
                                self.entries["memo"].delete("1.0", "end")
                                self.entries["memo"].insert("1.0", emp['memo'])
                            self.is_admin_var.set(bool(emp['is_admin']))
                            break
        except Exception as e:
            pass
    
    def refresh(self):
        self.load_employees()