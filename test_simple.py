#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

# 간단한 테스트 프로그램
class SimpleLeaveApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("치과 연차관리 시스템 - 테스트")
        self.root.geometry("400x300")
        
        # 데이터베이스 초기화
        self.init_db()
        
        # UI 구성
        self.setup_ui()
    
    def init_db(self):
        os.makedirs("data", exist_ok=True)
        self.conn = sqlite3.connect("data/test_dental.db")
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                annual_days INTEGER DEFAULT 15
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leaves (
                id INTEGER PRIMARY KEY,
                employee_id INTEGER,
                leave_date DATE,
                leave_type TEXT,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
        ''')
        
        # 테스트 데이터
        cursor.execute("INSERT OR IGNORE INTO employees (id, name) VALUES (1, '테스트 직원')")
        self.conn.commit()
    
    def setup_ui(self):
        # 제목
        title = tk.Label(self.root, text="치과 연차관리 시스템", font=("Arial", 16, "bold"))
        title.pack(pady=20)
        
        # 현재 상태
        self.status_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.status_label.pack(pady=10)
        
        # 버튼들
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="연차 현황 조회", command=self.show_status, width=20).pack(pady=5)
        tk.Button(btn_frame, text="연차 추가", command=self.add_leave, width=20).pack(pady=5)
        tk.Button(btn_frame, text="종료", command=self.root.quit, width=20).pack(pady=5)
        
        # 초기 상태 표시
        self.show_status()
    
    def show_status(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM leaves WHERE employee_id = 1 AND strftime('%Y', leave_date) = strftime('%Y', 'now')
        ''')
        used_days = cursor.fetchone()[0]
        remaining = 15 - used_days
        
        self.status_label.config(text=f"2025년 연차 현황\n사용: {used_days}일 / 잔여: {remaining}일")
    
    def add_leave(self):
        # 간단한 입력 창
        dialog = tk.Toplevel(self.root)
        dialog.title("연차 추가")
        dialog.geometry("300x150")
        
        tk.Label(dialog, text="날짜 (YYYY-MM-DD):").pack(pady=5)
        date_entry = tk.Entry(dialog)
        date_entry.pack(pady=5)
        date_entry.insert(0, "2025-01-15")
        
        def save():
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "INSERT INTO leaves (employee_id, leave_date, leave_type) VALUES (?, ?, ?)",
                    (1, date_entry.get(), "연차")
                )
                self.conn.commit()
                messagebox.showinfo("성공", "연차가 추가되었습니다.")
                dialog.destroy()
                self.show_status()
            except Exception as e:
                messagebox.showerror("오류", str(e))
        
        tk.Button(dialog, text="저장", command=save).pack(pady=20)
    
    def run(self):
        self.root.mainloop()
        self.conn.close()

if __name__ == "__main__":
    print("치과 연차관리 시스템 테스트 버전을 실행합니다...")
    print("customtkinter가 설치되지 않아 기본 tkinter를 사용합니다.")
    app = SimpleLeaveApp()
    app.run()