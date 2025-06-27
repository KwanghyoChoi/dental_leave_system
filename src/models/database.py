import sqlite3
import os
from datetime import datetime
import bcrypt
from contextlib import contextmanager

class Database:
    def __init__(self, db_path="data/dental_leave.db"):
        try:
            self.db_path = db_path
            # 상대 경로를 절대 경로로 변환
            if not os.path.isabs(db_path):
                script_dir = os.path.dirname(os.path.abspath(__file__))
                project_root = os.path.dirname(script_dir)
                self.db_path = os.path.join(project_root, db_path)
            
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            print(f"데이터베이스 경로: {self.db_path}")
            self.init_database()
        except Exception as e:
            print(f"데이터베이스 초기화 오류: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def init_database(self):
        try:
            print("데이터베이스 테이블 생성 중...")
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS employees (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        name TEXT NOT NULL,
                        hire_date DATE NOT NULL,
                        annual_leave_days INTEGER NOT NULL,
                        position TEXT,
                        is_admin BOOLEAN DEFAULT 0,
                        ssn_encrypted TEXT,
                        phone TEXT,
                        employment_type TEXT,
                        memo TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS leaves (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        employee_id INTEGER NOT NULL,
                        leave_date DATE NOT NULL,
                        leave_type TEXT NOT NULL,
                        reason TEXT,
                        status TEXT DEFAULT 'confirmed',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (employee_id) REFERENCES employees (id),
                        UNIQUE(employee_id, leave_date)
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS common_leaves (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        leave_name TEXT NOT NULL,
                        start_date DATE NOT NULL,
                        end_date DATE NOT NULL,
                        actual_days INTEGER NOT NULL,
                        deduct_days REAL NOT NULL,
                        memo TEXT,
                        created_by INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (created_by) REFERENCES employees (id)
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS common_leave_employees (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        common_leave_id INTEGER NOT NULL,
                        employee_id INTEGER NOT NULL,
                        FOREIGN KEY (common_leave_id) REFERENCES common_leaves (id),
                        FOREIGN KEY (employee_id) REFERENCES employees (id),
                        UNIQUE(common_leave_id, employee_id)
                    )
                ''')
                
                admin_exists = cursor.execute(
                    "SELECT COUNT(*) FROM employees WHERE username = '관리자'"
                ).fetchone()[0]
                
                if admin_exists == 0:
                    admin_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
                    cursor.execute('''
                        INSERT INTO employees (username, password_hash, name, hire_date, 
                                             annual_leave_days, position, is_admin)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', ('관리자', admin_password, '관리자', datetime.now().date(), 15, '관리자', 1))
                    print("관리자 계정 생성 완료")
                
                print("데이터베이스 초기화 완료")
        except Exception as e:
            print(f"데이터베이스 초기화 중 오류: {e}")
            raise
    
    def create_employee(self, name, password, hire_date, annual_leave_days, 
                       position=None, is_admin=False, ssn_encrypted=None, 
                       phone=None, employment_type=None, memo=None):
        # 이름을 username으로 사용
        username = name
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO employees (username, password_hash, name, hire_date, 
                                     annual_leave_days, position, is_admin, ssn_encrypted,
                                     phone, employment_type, memo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username, password_hash, name, hire_date, annual_leave_days, 
                  position, is_admin, ssn_encrypted, phone, employment_type, memo))
            return cursor.lastrowid
    
    def authenticate_user(self, username, password):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            user = cursor.execute(
                "SELECT * FROM employees WHERE username = ?", (username,)
            ).fetchone()
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
                return dict(user)
            return None
    
    def get_employee_by_id(self, employee_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            return dict(cursor.execute(
                "SELECT * FROM employees WHERE id = ?", (employee_id,)
            ).fetchone())
    
    def get_all_employees(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            return [dict(row) for row in cursor.execute(
                "SELECT * FROM employees ORDER BY name"
            ).fetchall()]
    
    def create_leave(self, employee_id, leave_date, leave_type, reason=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO leaves (employee_id, leave_date, leave_type, reason)
                VALUES (?, ?, ?, ?)
            ''', (employee_id, leave_date, leave_type, reason))
            return cursor.lastrowid
    
    def get_employee_leaves(self, employee_id, year=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if year:
                return [dict(row) for row in cursor.execute('''
                    SELECT * FROM leaves 
                    WHERE employee_id = ? AND strftime('%Y', leave_date) = ?
                    ORDER BY leave_date
                ''', (employee_id, str(year))).fetchall()]
            else:
                return [dict(row) for row in cursor.execute('''
                    SELECT * FROM leaves 
                    WHERE employee_id = ?
                    ORDER BY leave_date DESC
                ''', (employee_id,)).fetchall()]
    
    def delete_leave(self, leave_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM leaves WHERE id = ?", (leave_id,))
    
    def update_employee(self, employee_id, **kwargs):
        allowed_fields = ['name', 'hire_date', 'annual_leave_days', 'position', 
                         'is_admin', 'ssn_encrypted', 'phone', 'employment_type', 'memo']
        
        fields_to_update = []
        values = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                fields_to_update.append(f"{field} = ?")
                values.append(value)
        
        if not fields_to_update:
            return
        
        values.append(employee_id)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = f"UPDATE employees SET {', '.join(fields_to_update)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
            cursor.execute(query, values)
    
    def update_password(self, employee_id, new_password):
        password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE employees SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (password_hash, employee_id)
            )
    
    def create_common_leave(self, leave_name, start_date, end_date, actual_days, 
                           deduct_days, employee_ids, created_by, memo=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO common_leaves (leave_name, start_date, end_date, 
                                         actual_days, deduct_days, memo, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (leave_name, start_date, end_date, actual_days, deduct_days, memo, created_by))
            
            common_leave_id = cursor.lastrowid
            
            for emp_id in employee_ids:
                cursor.execute('''
                    INSERT INTO common_leave_employees (common_leave_id, employee_id)
                    VALUES (?, ?)
                ''', (common_leave_id, emp_id))
            
            return common_leave_id
    
    def get_common_leaves(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            return [dict(row) for row in cursor.execute('''
                SELECT cl.*, e.name as created_by_name
                FROM common_leaves cl
                LEFT JOIN employees e ON cl.created_by = e.id
                ORDER BY cl.start_date DESC
            ''').fetchall()]
    
    def get_common_leave_employees(self, common_leave_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            return [dict(row) for row in cursor.execute('''
                SELECT e.*
                FROM employees e
                JOIN common_leave_employees cle ON e.id = cle.employee_id
                WHERE cle.common_leave_id = ?
            ''', (common_leave_id,)).fetchall()]
    
    def update_common_leave(self, common_leave_id, leave_name, start_date, end_date, 
                          actual_days, deduct_days, employee_ids, memo=None):
        """공통 연차 정보 업데이트"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 공통 연차 정보 업데이트
            cursor.execute('''
                UPDATE common_leaves
                SET leave_name = ?, start_date = ?, end_date = ?, 
                    actual_days = ?, deduct_days = ?, memo = ?
                WHERE id = ?
            ''', (leave_name, start_date, end_date, actual_days, 
                  deduct_days, memo, common_leave_id))
            
            # 기존 직원 연결 삭제
            cursor.execute('''
                DELETE FROM common_leave_employees
                WHERE common_leave_id = ?
            ''', (common_leave_id,))
            
            # 새로운 직원 연결 추가
            for emp_id in employee_ids:
                cursor.execute('''
                    INSERT INTO common_leave_employees (common_leave_id, employee_id)
                    VALUES (?, ?)
                ''', (common_leave_id, emp_id))
            
            return common_leave_id
    
    def get_common_leave_by_id(self, common_leave_id):
        """특정 공통 연차 정보 조회"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            return dict(cursor.execute('''
                SELECT * FROM common_leaves
                WHERE id = ?
            ''', (common_leave_id,)).fetchone())
    
    def get_employee_common_leaves(self, employee_id, year):
        """특정 직원에게 적용된 공통 연차 조회"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            return [dict(row) for row in cursor.execute('''
                SELECT cl.*
                FROM common_leaves cl
                JOIN common_leave_employees cle ON cl.id = cle.common_leave_id
                WHERE cle.employee_id = ?
                AND strftime('%Y', cl.start_date) = ?
                ORDER BY cl.start_date
            ''', (employee_id, str(year))).fetchall()]
    
    def delete_employee(self, employee_id):
        """직원 삭제 (관련된 모든 데이터도 함께 삭제)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 해당 직원의 연차 기록 삭제
            cursor.execute("DELETE FROM leaves WHERE employee_id = ?", (employee_id,))
            
            # 해당 직원의 공통연차 연결 삭제
            cursor.execute("DELETE FROM common_leave_employees WHERE employee_id = ?", (employee_id,))
            
            # 직원 정보 삭제
            cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
            
            return cursor.rowcount > 0
    
    def delete_common_leave(self, common_leave_id):
        """공통 연차 삭제 (관련된 모든 데이터도 함께 삭제)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 해당 공통연차의 직원 연결 삭제
            cursor.execute("DELETE FROM common_leave_employees WHERE common_leave_id = ?", (common_leave_id,))
            
            # 공통연차 삭제
            cursor.execute("DELETE FROM common_leaves WHERE id = ?", (common_leave_id,))
            
            return cursor.rowcount > 0