#!/usr/bin/env python3
import sqlite3
import os
from datetime import datetime
import hashlib

class ConsoleLeaveSystem:
    def __init__(self):
        self.init_db()
        self.current_user = None
    
    def init_db(self):
        os.makedirs("data", exist_ok=True)
        self.conn = sqlite3.connect("data/console_dental.db")
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        
        # 테이블 생성
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                annual_days INTEGER DEFAULT 15,
                is_admin BOOLEAN DEFAULT 0
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
        
        # 관리자 계정 생성
        admin_exists = cursor.execute("SELECT COUNT(*) FROM employees WHERE username='admin'").fetchone()[0]
        if admin_exists == 0:
            admin_pass = hashlib.md5("admin123".encode()).hexdigest()
            cursor.execute(
                "INSERT INTO employees (username, password, name, is_admin) VALUES (?, ?, ?, ?)",
                ("admin", admin_pass, "관리자", 1)
            )
        
        self.conn.commit()
    
    def login(self):
        print("\n=== 로그인 ===")
        username = input("아이디: ")
        password = input("비밀번호: ")
        
        hashed_pass = hashlib.md5(password.encode()).hexdigest()
        cursor = self.conn.cursor()
        user = cursor.execute(
            "SELECT * FROM employees WHERE username=? AND password=?",
            (username, hashed_pass)
        ).fetchone()
        
        if user:
            self.current_user = dict(user)
            print(f"\n{user['name']}님 환영합니다!")
            return True
        else:
            print("\n로그인 실패!")
            return False
    
    def show_menu(self):
        while True:
            print("\n=== 메인 메뉴 ===")
            print("1. 내 연차 조회")
            print("2. 연차 신청")
            print("3. 연차 삭제")
            
            if self.current_user['is_admin']:
                print("4. 직원 관리")
                print("5. 전체 연차 현황")
            
            print("0. 로그아웃")
            
            choice = input("\n선택: ")
            
            if choice == "1":
                self.show_my_leaves()
            elif choice == "2":
                self.add_leave()
            elif choice == "3":
                self.delete_leave()
            elif choice == "4" and self.current_user['is_admin']:
                self.manage_employees()
            elif choice == "5" and self.current_user['is_admin']:
                self.show_all_leaves()
            elif choice == "0":
                self.current_user = None
                break
            else:
                print("\n잘못된 선택입니다.")
    
    def show_my_leaves(self):
        print(f"\n=== {self.current_user['name']}님의 연차 현황 ===")
        cursor = self.conn.cursor()
        
        year = datetime.now().year
        leaves = cursor.execute(
            "SELECT * FROM leaves WHERE employee_id=? AND strftime('%Y', leave_date)=? ORDER BY leave_date",
            (self.current_user['id'], str(year))
        ).fetchall()
        
        if leaves:
            print(f"\n{year}년 사용 내역:")
            for leave in leaves:
                print(f"- {leave['leave_date']}: {leave['leave_type']}")
            
            total = len(leaves)
            remaining = self.current_user['annual_days'] - total
            print(f"\n총 {total}일 사용, {remaining}일 남음")
        else:
            print(f"\n{year}년 사용한 연차가 없습니다.")
            print(f"잔여 연차: {self.current_user['annual_days']}일")
    
    def add_leave(self):
        print("\n=== 연차 신청 ===")
        date_str = input("날짜 (YYYY-MM-DD): ")
        
        try:
            # 날짜 형식 검증
            datetime.strptime(date_str, '%Y-%m-%d')
            
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO leaves (employee_id, leave_date, leave_type) VALUES (?, ?, ?)",
                (self.current_user['id'], date_str, "연차")
            )
            self.conn.commit()
            print("\n연차가 신청되었습니다.")
        except ValueError:
            print("\n올바른 날짜 형식이 아닙니다.")
        except sqlite3.IntegrityError:
            print("\n이미 해당 날짜에 연차가 등록되어 있습니다.")
    
    def delete_leave(self):
        cursor = self.conn.cursor()
        leaves = cursor.execute(
            "SELECT * FROM leaves WHERE employee_id=? ORDER BY leave_date DESC LIMIT 10",
            (self.current_user['id'],)
        ).fetchall()
        
        if not leaves:
            print("\n삭제할 연차가 없습니다.")
            return
        
        print("\n=== 최근 연차 목록 ===")
        for i, leave in enumerate(leaves, 1):
            print(f"{i}. {leave['leave_date']}: {leave['leave_type']}")
        
        try:
            choice = int(input("\n삭제할 번호 (0=취소): "))
            if 1 <= choice <= len(leaves):
                cursor.execute("DELETE FROM leaves WHERE id=?", (leaves[choice-1]['id'],))
                self.conn.commit()
                print("\n연차가 삭제되었습니다.")
        except ValueError:
            print("\n잘못된 입력입니다.")
    
    def manage_employees(self):
        print("\n=== 직원 관리 ===")
        print("1. 직원 목록")
        print("2. 직원 추가")
        
        choice = input("\n선택: ")
        
        if choice == "1":
            cursor = self.conn.cursor()
            employees = cursor.execute("SELECT * FROM employees").fetchall()
            print("\n직원 목록:")
            for emp in employees:
                admin_str = " (관리자)" if emp['is_admin'] else ""
                print(f"- {emp['name']} ({emp['username']}){admin_str} - 연차: {emp['annual_days']}일")
        
        elif choice == "2":
            print("\n=== 직원 추가 ===")
            username = input("아이디: ")
            password = input("비밀번호: ")
            name = input("이름: ")
            annual_days = input("연차일수 (기본=15): ") or "15"
            
            try:
                hashed_pass = hashlib.md5(password.encode()).hexdigest()
                cursor = self.conn.cursor()
                cursor.execute(
                    "INSERT INTO employees (username, password, name, annual_days) VALUES (?, ?, ?, ?)",
                    (username, hashed_pass, name, int(annual_days))
                )
                self.conn.commit()
                print("\n직원이 추가되었습니다.")
            except sqlite3.IntegrityError:
                print("\n이미 존재하는 아이디입니다.")
            except ValueError:
                print("\n연차일수는 숫자여야 합니다.")
    
    def show_all_leaves(self):
        print("\n=== 전체 연차 현황 ===")
        cursor = self.conn.cursor()
        
        year = datetime.now().year
        employees = cursor.execute("SELECT * FROM employees").fetchall()
        
        for emp in employees:
            leaves_count = cursor.execute(
                "SELECT COUNT(*) FROM leaves WHERE employee_id=? AND strftime('%Y', leave_date)=?",
                (emp['id'], str(year))
            ).fetchone()[0]
            
            remaining = emp['annual_days'] - leaves_count
            print(f"\n{emp['name']}: 사용 {leaves_count}일 / 잔여 {remaining}일")
    
    def run(self):
        print("=" * 50)
        print("치과 연차관리 시스템 (콘솔 버전)")
        print("=" * 50)
        print("\n기본 관리자 계정: admin / admin123")
        
        while True:
            if not self.current_user:
                if not self.login():
                    continue
            
            self.show_menu()
            
            if not self.current_user:
                again = input("\n다시 로그인하시겠습니까? (y/n): ")
                if again.lower() != 'y':
                    break
        
        print("\n프로그램을 종료합니다.")
        self.conn.close()

if __name__ == "__main__":
    app = ConsoleLeaveSystem()
    app.run()