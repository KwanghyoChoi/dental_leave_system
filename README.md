# 치과 직원 연차관리 프로그램

## 개요
Python과 customtkinter를 사용한 치과 직원 연차관리 데스크톱 애플리케이션

## 🌟 주요 기능
- 한글 이름 기반 로그인 시스템 (드롭다운 선택)
- 개인 연차 입력/조회 (즉시 확정)
- 직원 계정 관리 (관리자 전용)
- 공통 연차 관리 (관리자 전용)
- 전체 직원 연차 현황 관리 (관리자 전용)
- 달력 뷰로 전체 연차 현황 확인
- 연차 사용 통계

## 🚀 실행 방법

### 🏥 추천 방법 (Windows):
1. **`run_safe.bat` 더블클릭** - 모든 것을 자동으로 처리합니다!
   - Python 환경 체크
   - 데이터베이스 테스트
   - 필요한 패키지 자동 설치
   - 프로그램 안전 실행

### 🔧 수동 실행 (Windows):
1. **패키지 설치:**
   ```bash
   pip install customtkinter Pillow tkcalendar bcrypt python-dateutil
   ```

2. **프로그램 실행:**
   ```bash
   cd src
   python main.py
   ```

3. **문제 해결:**
   - 오류 발생 시: `python debug.py` 실행
   - 데이터베이스 테스트: `python test_db.py` 실행
   - 안전 시작: `python start.py` 실행

### Linux/macOS:
```bash
pip3 install customtkinter Pillow tkcalendar bcrypt python-dateutil
cd src
python3 main.py
```

## 🔐 로그인 방법
- **기본 관리자**: 드롭다운에서 "관리자" 선택 → 비밀번호: admin123
- **일반 직원**: 드롭다운에서 이름 선택 → 개인 비밀번호 입력

## 📁 데이터베이스
- SQLite 파일: `data/dental_leave.db`
- 네트워크 공유폴더 저장 가능
- 자동 백업 권장

## 🎨 새로운 기능
- 🦷 치과 전문 디자인 테마
- 📋 아이콘 기반 메뉴
- 👥 전체 직원 연차 현황 관리
- 🔄 실시간 직원 목록 새로고침
- 📊 향상된 통계 화면