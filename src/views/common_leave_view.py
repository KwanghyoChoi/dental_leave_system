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
        
        # 테이블 프레임
        table_frame = ctk.CTkFrame(self)
        table_frame.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # 스크롤 가능한 프레임
        self.scrollable_frame = ctk.CTkScrollableFrame(table_frame, height=400)
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # 테이블 헤더
        headers = ["연차명", "기간", "실제휴무", "차감일수", "등록자", "적용직원", "메모", "작업"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(
                self.scrollable_frame,
                text=header,
                font=ctk.CTkFont(weight="bold")
            )
            label.grid(row=0, column=i, padx=5, pady=5, sticky="w")
        
        refresh_button = ctk.CTkButton(
            self,
            text="새로고침",
            command=self.load_common_leaves,
            width=100
        )
        refresh_button.grid(row=3, column=0, pady=10)
    
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
        # 기존 내용 삭제 (헤더 제외)
        for widget in self.scrollable_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()
        
        try:
            common_leaves = self.db.get_common_leaves()
            
            if not common_leaves:
                no_data_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text="등록된 공통 연차가 없습니다.",
                    text_color="gray"
                )
                no_data_label.grid(row=1, column=0, columnspan=8, pady=20)
                return
            
            for idx, leave in enumerate(common_leaves, start=1):
                # 연차명
                name_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=leave['leave_name']
                )
                name_label.grid(row=idx, column=0, padx=5, pady=2, sticky="w")
                
                # 기간
                period = f"{leave['start_date']} ~ {leave['end_date']}"
                period_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=period
                )
                period_label.grid(row=idx, column=1, padx=5, pady=2, sticky="w")
                
                # 실제휴무
                actual_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=str(leave['actual_days'])
                )
                actual_label.grid(row=idx, column=2, padx=5, pady=2, sticky="w")
                
                # 차감일수
                deduct_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=str(leave['deduct_days'])
                )
                deduct_label.grid(row=idx, column=3, padx=5, pady=2, sticky="w")
                
                # 등록자
                created_by_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=leave['created_by_name'] or '-'
                )
                created_by_label.grid(row=idx, column=4, padx=5, pady=2, sticky="w")
                
                # 적용직원
                employees = self.db.get_common_leave_employees(leave['id'])
                emp_names = [emp['name'] for emp in employees]
                emp_text = ', '.join(emp_names) if emp_names else '-'
                emp_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=emp_text,
                    wraplength=150
                )
                emp_label.grid(row=idx, column=5, padx=5, pady=2, sticky="w")
                
                # 메모
                memo_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=leave['memo'] or '-',
                    wraplength=150
                )
                memo_label.grid(row=idx, column=6, padx=5, pady=2, sticky="w")
                
                # 수정 버튼
                edit_btn = ctk.CTkButton(
                    self.scrollable_frame,
                    text="수정",
                    command=lambda lid=leave['id']: self.edit_common_leave(lid),
                    width=50,
                    height=25,
                    fg_color="green",
                    hover_color="darkgreen"
                )
                edit_btn.grid(row=idx, column=7, padx=5, pady=2, sticky="w")
                
        except Exception as e:
            print(f"공통 연차 목록 로드 오류: {e}")
            error_label = ctk.CTkLabel(
                self.scrollable_frame,
                text=f"데이터 로드 중 오류 발생: {str(e)}",
                text_color="red"
            )
            error_label.grid(row=1, column=0, columnspan=8, pady=20)
    
    def clear_form(self):
        self.name_entry.delete(0, 'end')
        self.actual_days_entry.delete(0, 'end')
        self.deduct_days_entry.delete(0, 'end')
        self.memo_entry.delete(0, 'end')
        
        for var in self.employee_vars.values():
            var.set(True)
    
    def refresh(self):
        self.load_common_leaves()
    
    def edit_common_leave(self, common_leave_id):
        """공통 연차 수정 다이얼로그"""
        # 기존 데이터 조회
        leave_data = self.db.get_common_leave_by_id(common_leave_id)
        existing_employees = self.db.get_common_leave_employees(common_leave_id)
        existing_emp_ids = [emp['id'] for emp in existing_employees]
        
        # 수정 다이얼로그 창
        edit_window = ctk.CTkToplevel(self)
        edit_window.title("공통 연차 수정")
        edit_window.geometry("600x500")
        edit_window.transient(self.winfo_toplevel())
        edit_window.grab_set()
        
        # 중앙 배치
        edit_window.update_idletasks()
        x = (edit_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (edit_window.winfo_screenheight() // 2) - (500 // 2)
        edit_window.geometry(f"600x500+{x}+{y}")
        
        # 제목
        title_label = ctk.CTkLabel(
            edit_window,
            text="공통 연차 수정",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # 입력 필드
        fields_frame = ctk.CTkFrame(edit_window)
        fields_frame.pack(padx=20, pady=10, fill="x")
        
        # 연차명
        name_label = ctk.CTkLabel(fields_frame, text="연차명:")
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        name_entry = ctk.CTkEntry(fields_frame, width=200)
        name_entry.insert(0, leave_data['leave_name'])
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # 시작일
        start_label = ctk.CTkLabel(fields_frame, text="시작일:")
        start_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        start_date_entry = DateEntry(
            fields_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd'
        )
        start_date_entry.set_date(datetime.strptime(leave_data['start_date'], '%Y-%m-%d').date())
        start_date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # 종료일
        end_label = ctk.CTkLabel(fields_frame, text="종료일:")
        end_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        end_date_entry = DateEntry(
            fields_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd'
        )
        end_date_entry.set_date(datetime.strptime(leave_data['end_date'], '%Y-%m-%d').date())
        end_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        # 실제 휴무일
        actual_label = ctk.CTkLabel(fields_frame, text="실제 휴무일:")
        actual_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        actual_days_entry = ctk.CTkEntry(fields_frame, width=100)
        actual_days_entry.insert(0, str(leave_data['actual_days']))
        actual_days_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        # 차감 일수
        deduct_label = ctk.CTkLabel(fields_frame, text="차감 일수:")
        deduct_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        deduct_days_entry = ctk.CTkEntry(fields_frame, width=100)
        deduct_days_entry.insert(0, str(leave_data['deduct_days']))
        deduct_days_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        # 메모
        memo_label = ctk.CTkLabel(fields_frame, text="메모:")
        memo_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        memo_entry = ctk.CTkEntry(fields_frame, width=300)
        if leave_data['memo']:
            memo_entry.insert(0, leave_data['memo'])
        memo_entry.grid(row=5, column=1, padx=5, pady=5)
        
        # 직원 선택
        emp_label = ctk.CTkLabel(edit_window, text="적용 직원:")
        emp_label.pack(pady=(10, 5))
        
        # 스크롤 가능한 직원 목록
        emp_scroll_frame = ctk.CTkScrollableFrame(edit_window, height=150)
        emp_scroll_frame.pack(padx=20, pady=5, fill="x")
        
        employee_vars = {}
        employees = self.db.get_all_employees()
        
        for i, emp in enumerate(employees):
            var = ctk.BooleanVar(value=emp['id'] in existing_emp_ids)
            check = ctk.CTkCheckBox(
                emp_scroll_frame,
                text=emp['name'],
                variable=var
            )
            check.grid(row=i // 3, column=i % 3, padx=10, pady=5, sticky="w")
            employee_vars[emp['id']] = var
        
        # 버튼 프레임
        button_frame = ctk.CTkFrame(edit_window, fg_color="transparent")
        button_frame.pack(pady=20)
        
        def save_changes():
            try:
                name = name_entry.get().strip()
                start_date = start_date_entry.get_date()
                end_date = end_date_entry.get_date()
                actual_days = int(actual_days_entry.get())
                deduct_days = float(deduct_days_entry.get())
                memo = memo_entry.get().strip() or None
                
                if not name:
                    messagebox.showwarning("입력 오류", "연차명을 입력해주세요.")
                    return
                
                if start_date > end_date:
                    messagebox.showwarning("입력 오류", "종료일이 시작일보다 빠를 수 없습니다.")
                    return
                
                selected_employees = [
                    emp_id for emp_id, var in employee_vars.items() if var.get()
                ]
                
                if not selected_employees:
                    messagebox.showwarning("선택 오류", "최소 한 명 이상의 직원을 선택해주세요.")
                    return
                
                self.db.update_common_leave(
                    common_leave_id, name, start_date, end_date, 
                    actual_days, deduct_days, selected_employees, memo
                )
                
                messagebox.showinfo("성공", "공통 연차가 수정되었습니다.")
                edit_window.destroy()
                self.load_common_leaves()
                
            except ValueError:
                messagebox.showerror("입력 오류", "실제 휴무일과 차감 일수는 숫자로 입력해주세요.")
            except Exception as e:
                messagebox.showerror("오류", f"공통 연차 수정 중 오류가 발생했습니다: {str(e)}")
        
        save_button = ctk.CTkButton(
            button_frame,
            text="저장",
            command=save_changes,
            width=100
        )
        save_button.pack(side="left", padx=5)
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="취소",
            command=edit_window.destroy,
            width=100,
            fg_color="gray",
            hover_color="darkgray"
        )
        cancel_button.pack(side="left", padx=5)