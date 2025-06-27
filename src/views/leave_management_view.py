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
        
        # 테이블 프레임
        table_frame = ctk.CTkFrame(self)
        table_frame.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # 스크롤 가능한 프레임
        self.scrollable_frame = ctk.CTkScrollableFrame(table_frame, height=350)
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # 테이블 헤더
        headers = ["날짜", "종류", "사유", "ID"]
        header_widths = [120, 120, 300, 60]
        for i, (header, width) in enumerate(zip(headers, header_widths)):
            label = ctk.CTkLabel(
                self.scrollable_frame,
                text=header,
                font=ctk.CTkFont(weight="bold"),
                width=width
            )
            label.grid(row=0, column=i, padx=5, pady=5, sticky="w")
        
        # 버튼 프레임
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=3, column=0, pady=10)
        
        refresh_button = ctk.CTkButton(
            button_frame,
            text="새로고침",
            command=self.load_leaves,
            width=100
        )
        refresh_button.pack(side="left", padx=5)
        
        delete_button = ctk.CTkButton(
            button_frame,
            text="전체 삭제",
            command=self.delete_all,
            width=100,
            fg_color="red",
            hover_color="darkred"
        )
        delete_button.pack(side="left", padx=5)
        
        stats_frame = ctk.CTkFrame(self)
        stats_frame.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")
        
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
        # 기존 내용 삭제 (헤더 제외)
        for widget in self.scrollable_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()
        
        try:
            current_year = datetime.now().year
            leaves = self.db.get_employee_leaves(self.session.get_user_id(), current_year)
            
            if not leaves:
                no_data_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text="등록된 연차가 없습니다.",
                    text_color="gray"
                )
                no_data_label.grid(row=1, column=0, columnspan=4, pady=20)
            
            total_days = 0
            leave_counts = {"연차": 0, "반차(오전)": 0, "반차(오후)": 0, "병가": 0, "경조사": 0}
            
            for idx, leave in enumerate(leaves, start=1):
                # 날짜
                date_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=leave['leave_date'],
                    width=120
                )
                date_label.grid(row=idx, column=0, padx=5, pady=2, sticky="w")
                
                # 종류
                type_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=leave['leave_type'],
                    width=120
                )
                type_label.grid(row=idx, column=1, padx=5, pady=2, sticky="w")
                
                # 사유
                reason_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=leave['reason'] or "-",
                    width=300,
                    anchor="w"
                )
                reason_label.grid(row=idx, column=2, padx=5, pady=2, sticky="w")
                
                # ID와 삭제 버튼
                id_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
                id_frame.grid(row=idx, column=3, padx=5, pady=2, sticky="w")
                
                id_label = ctk.CTkLabel(
                    id_frame,
                    text=str(leave['id']),
                    width=40
                )
                id_label.pack(side="left")
                
                delete_btn = ctk.CTkButton(
                    id_frame,
                    text="삭제",
                    command=lambda lid=leave['id']: self.delete_leave(lid),
                    width=50,
                    height=25,
                    fg_color="red",
                    hover_color="darkred"
                )
                delete_btn.pack(side="left", padx=(10, 0))
                
                # 통계 계산
                leave_type = leave['leave_type']
                if leave_type in leave_counts:
                    leave_counts[leave_type] += 1
                    if leave_type == "연차":
                        total_days += 1
                    elif "반차" in leave_type:
                        total_days += 0.5
            
            # 공통 연차 정보 추가
            common_leaves = self.db.get_employee_common_leaves(self.session.get_user_id(), current_year)
            common_leave_days = 0
            for cl in common_leaves:
                common_leave_days += cl['deduct_days']
            
            # 통계 업데이트
            employee = self.db.get_employee_by_id(self.session.get_user_id())
            annual_leave_days = employee['annual_leave_days']
            total_used_days = total_days + common_leave_days  # 개인 + 공통 연차
            remaining_days = annual_leave_days - total_used_days
            
            stats_text = f"{current_year}년 연차 현황: "
            stats_text += f"총 {annual_leave_days}일 중 {total_used_days:.1f}일 사용, {remaining_days:.1f}일 남음\n"
            stats_text += f"(개인연차: {total_days}일 [연차 {leave_counts['연차']}일, 반차 {leave_counts['반차(오전)']+leave_counts['반차(오후)']}회], "
            stats_text += f"공통연차: {common_leave_days:.1f}일)"
            
            self.stats_label.configure(text=stats_text)
            
        except Exception as e:
            print(f"연차 목록 로드 오류: {e}")
            error_label = ctk.CTkLabel(
                self.scrollable_frame,
                text=f"데이터 로드 중 오류 발생: {str(e)}",
                text_color="red"
            )
            error_label.grid(row=1, column=0, columnspan=4, pady=20)
    
    def delete_leave(self, leave_id):
        if messagebox.askyesno("삭제 확인", "선택한 연차를 삭제하시겠습니까?"):
            try:
                self.db.delete_leave(leave_id)
                messagebox.showinfo("성공", "연차가 삭제되었습니다.")
                self.load_leaves()
            except Exception as e:
                messagebox.showerror("오류", f"연차 삭제 중 오류가 발생했습니다: {str(e)}")
    
    def delete_all(self):
        if messagebox.askyesno("전체 삭제", "정말로 모든 연차를 삭제하시겠습니까?\n이 작업은 되돌릴 수 없습니다."):
            try:
                current_year = datetime.now().year
                leaves = self.db.get_employee_leaves(self.session.get_user_id(), current_year)
                for leave in leaves:
                    self.db.delete_leave(leave['id'])
                messagebox.showinfo("성공", "모든 연차가 삭제되었습니다.")
                self.load_leaves()
            except Exception as e:
                messagebox.showerror("오류", f"연차 삭제 중 오류가 발생했습니다: {str(e)}")
    
    def refresh(self):
        self.load_leaves()