#!/usr/bin/env python3
"""
간단한 GUI 테스트 - 창이 제대로 표시되는지 확인
"""
import sys
import os

print("간단한 GUI 테스트를 시작합니다...")

try:
    import customtkinter as ctk
    print("✓ customtkinter import 성공")
    
    # 간단한 창 생성
    app = ctk.CTk()
    app.title("GUI 테스트")
    app.geometry("400x300")
    
    # 화면 중앙에 배치
    app.update_idletasks()
    x = (app.winfo_screenwidth() // 2) - 200
    y = (app.winfo_screenheight() // 2) - 150
    app.geometry(f'400x300+{x}+{y}')
    
    # 창을 최상위로
    app.lift()
    app.attributes('-topmost', True)
    app.after(100, lambda: app.attributes('-topmost', False))
    
    # 간단한 위젯
    label = ctk.CTkLabel(app, text="GUI 테스트 성공!", font=("Arial", 24))
    label.pack(pady=50)
    
    button = ctk.CTkButton(app, text="창 닫기", command=app.quit)
    button.pack(pady=20)
    
    # 상태 메시지
    status = ctk.CTkLabel(app, text="이 창이 보이면 GUI가 정상 작동합니다", 
                         font=("Arial", 12), text_color="gray")
    status.pack(pady=10)
    
    print("GUI 창이 열렸습니다.")
    print("창이 보이지 않으면:")
    print("1. 작업 표시줄 확인")
    print("2. Alt+Tab으로 창 전환")
    print("3. Windows Defender나 백신이 차단하는지 확인")
    
    app.mainloop()
    print("GUI 테스트 완료")
    
except Exception as e:
    print(f"❌ 오류 발생: {e}")
    import traceback
    traceback.print_exc()
    
input("\nEnter를 눌러 종료...")