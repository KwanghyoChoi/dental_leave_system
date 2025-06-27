# 치과 연차관리 시스템 - 초기 설정 가이드

## 시스템 요구사항
- Windows 10/11 또는 Linux/macOS
- Python 3.8 이상
- 네트워크 공유 폴더 접근 권한 (다중 사용자 환경의 경우)

## 설치 방법

### 1. Python 설치 확인
터미널/명령 프롬프트에서 다음 명령어 실행:
```bash
python --version
# 또는
python3 --version
```

### 2. 필요한 패키지 설치

#### Windows PowerShell:
```powershell
cd dental_leave_system
pip install -r requirements.txt
```

#### Linux/macOS:
```bash
cd dental_leave_system
pip3 install -r requirements.txt
```

#### 가상환경 사용 (권장):
```bash
# 가상환경 생성
python -m venv venv

# Windows에서 활성화
venv\Scripts\activate

# Linux/macOS에서 활성화
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

### 3. 프로그램 실행

#### Windows:
```powershell
cd src
python main.py
```

#### Linux/macOS:
```bash
cd src
python3 main.py
```

## 초기 설정

### 1. 관리자 계정
- 최초 실행 시 자동으로 관리자 계정이 생성됩니다
- ID: `admin`
- Password: `admin123`
- **중요**: 첫 로그인 후 반드시 비밀번호를 변경하세요

### 2. 데이터베이스 위치
- 기본 위치: `data/dental_leave.db`
- 네트워크 공유 설정 시: `database.py`의 경로를 수정하세요
  ```python
  # 예시: 네트워크 드라이브
  db_path = "Z:/shared/dental_leave.db"
  
  # 예시: UNC 경로
  db_path = "//server/share/dental_leave.db"
  ```

### 3. 직원 계정 생성
1. 관리자로 로그인
2. 좌측 메뉴에서 "직원 관리" 클릭
3. 다음 정보 입력:
   - 아이디 (중복 불가)
   - 비밀번호
   - 이름
   - 입사일
   - 연차 할당일수 (기본: 15일)
   - 직책 (선택사항)
   - 관리자 권한 체크박스

### 4. 공통 연차 설정
관리자로 로그인 후 "공통 연차 관리"에서:
- 연차명 (예: 여름휴가, 연말연시)
- 시작일/종료일
- 실제 휴무일수
- 차감될 연차 일수
- 적용할 직원 선택

## 문제 해결

### 1. ModuleNotFoundError 발생 시
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### 2. tkinter 관련 오류 (Linux)
```bash
sudo apt-get install python3-tk
```

### 3. 데이터베이스 권한 오류
- 데이터베이스 파일과 폴더에 읽기/쓰기 권한 확인
- Windows: 폴더 속성 → 보안 → 모든 권한 부여
- Linux: `chmod 777 data/`

### 4. 네트워크 드라이브 접근 오류
- 네트워크 드라이브가 연결되어 있는지 확인
- 공유 폴더 접근 권한 확인
- 방화벽 설정 확인

## 백업 방법
정기적으로 `data/dental_leave.db` 파일을 백업하세요:
```bash
# Windows
copy data\dental_leave.db backup\dental_leave_backup_%date%.db

# Linux/macOS
cp data/dental_leave.db backup/dental_leave_backup_$(date +%Y%m%d).db
```