# PyQt 카메라 앱 & MySQL 데이터베이스 연동 프로젝트

이 프로젝트는 두 가지 주요 구성 요소로 이루어져 있습니다:
1. PyQt6 기반의 카메라 앱 (main.py)
2. MariaDB 연동 테스트 프로그램 (addBookMySQL.py)

## 주요 기능

### 카메라 앱 (main.py)
- Qt Designer를 활용한 GUI 구현
- 실시간 카메라 화면 표시
- 이미지 캡처 및 저장
- 연락처 정보 저장
- InstallFactory를 통한 실행 파일(.exe) 배포

### 데이터베이스 연동 (addBookMySQL.py)
- MariaDB와 연동
- HeidiSQL을 통한 데이터베이스 관리
- 기본적인 CRUD 작업 구현:
  - 연락처 추가 (Create)
  - 연락처 검색 (Read)
  - 연락처 수정 (Update)
  - 연락처 삭제 (Delete)

## 기술 스택
- Python
- PyQt6 / PyQt5
- MariaDB
- HeidiSQL
- Qt Designer
- InstallFactory

## 설치 요구사항

### 파이썬 패키지
```
PySide6==6.9.0
PySide6-Addons==6.9.0
PySide6-Essentials==6.9.0
PyQt5==5.15.9
PyQt5-Qt5>=5.15.2
PyQt5-sip>=12.11.0
pymysql==1.1.0
```

### 패키지 설치 방법
```bash
pip install -r requirements.txt
```

### 외부 프로그램
1. MariaDB
   - [MariaDB 공식 사이트](https://mariadb.org/download/)에서 다운로드
   - 설치 시 root 비밀번호 설정 필요

2. HeidiSQL
   - [HeidiSQL 공식 사이트](https://www.heidisql.com/download.php)에서 다운로드
   - MariaDB 관리를 위한 GUI 도구

3. Qt Designer
   - PyQt6 설치 시 함께 설치됨
   - GUI 디자인 도구

## 데이터베이스 설정
1. MariaDB 설치 및 실행
2. HeidiSQL을 통해 데이터베이스 생성:
   ```sql
   CREATE DATABASE kim;
   USE kim;
   ```
3. 테이블 생성:
   ```sql
   CREATE TABLE IF NOT EXISTS addbook (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(50) NOT NULL,
       phone VARCHAR(20) NOT NULL
   );
   ```
4. 데이터베이스 접속 정보 설정:
   - 호스트: localhost
   - 포트: 3336
   - 사용자: kim
   - 비밀번호: 6262
   - 데이터베이스: kim

## 실행 방법

### 카메라 앱 실행
1. 배포된 실행 파일(.exe)을 다운로드
2. 설치 프로그램 실행
3. 애플리케이션 실행

### 개발 모드로 실행
```bash
# 카메라 앱 실행
python main.py

# 데이터베이스 테스트
python addBookMySQL.py
```

## 프로젝트 구조
```
├── main.py              # 메인 카메라 앱
├── addBookMySQL.py      # 데이터베이스 연동 테스트
├── requirements.txt     # 필요한 파이썬 패키지
└── res/                 # 리소스 파일
    └── mainWin.ui      # Qt Designer UI 파일
```

## 라이선스
이 프로젝트는 MIT 라이선스 하에 있습니다. 