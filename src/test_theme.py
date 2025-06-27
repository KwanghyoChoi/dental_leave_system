#!/usr/bin/env python3
"""
Theme 모듈 테스트
"""
import sys
import os

def test_theme_import():
    try:
        print("Theme 모듈 import 테스트...")
        from utils.theme import Theme
        print("✓ Theme import 성공")
        
        print("색상 테스트...")
        print(f"✓ Primary 색상: {Theme.COLORS['primary']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Theme import 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_font_after_tkinter():
    try:
        print("\ntkinter 초기화 후 폰트 테스트...")
        import customtkinter as ctk
        
        # tkinter 루트 생성
        root = ctk.CTk()
        root.withdraw()  # 화면에 표시하지 않음
        
        from utils.theme import Theme
        
        print("폰트 생성 테스트...")
        title_font = Theme.get_font('title')
        print(f"✓ 제목 폰트 생성 성공: {title_font}")
        
        body_font = Theme.get_font('body')
        print(f"✓ 본문 폰트 생성 성공: {body_font}")
        
        root.destroy()
        print("✓ 모든 폰트 테스트 성공")
        return True
        
    except Exception as e:
        print(f"❌ 폰트 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=== Theme 모듈 테스트 ===")
    
    if not test_theme_import():
        return False
        
    if not test_font_after_tkinter():
        return False
    
    print("\n🎉 모든 Theme 테스트 통과!")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        input("Enter를 눌러 종료...")
        sys.exit(1)