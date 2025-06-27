#!/usr/bin/env python3
"""
데이터베이스만 테스트
"""
import sys
import os

# 경로 설정
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_database():
    try:
        print("=== 데이터베이스 테스트 ===")
        from models.database import Database
        
        print("1. 데이터베이스 모듈 import 성공")
        
        db = Database()
        print("2. 데이터베이스 초기화 성공")
        
        employees = db.get_all_employees()
        print(f"3. 직원 {len(employees)}명 조회 성공")
        
        for emp in employees:
            print(f"   - {emp['name']} ({emp['position']}) {'[관리자]' if emp['is_admin'] else '[직원]'}")
        
        print("\n✅ 데이터베이스 테스트 통과!")
        return True
        
    except Exception as e:
        print(f"❌ 데이터베이스 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_database()