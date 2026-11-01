# 주소록 웹 애플리케이션

## 프로젝트 목적
Python Flask와 SQLite로 만드는 주소록 관리 웹앱이다. 별도 DB 서버 없이 파일 하나(`instance/address_book.db`)에 저장한다.
대학 4학년 학생이 따라 할 수 있도록 파일 수는 적게, 구조는 실무형으로 유지한다.

- 항목: 이름(필수), 전화번호(필수), 이메일, 주소, 메모
- 기능: 목록 보기, 등록, 수정, 삭제, 이름·전화번호 검색
- 외부 패키지는 Flask, pytest만 사용한다. ORM, Flask-WTF 등은 추가하지 않는다.

## 폴더 구조
```
address_book/
├── app.py              # 앱 팩토리 create_app(), 라우트, 입력 검증
├── db.py               # DB 연결, init-db 명령, CRUD·검색 함수
├── schema.sql          # contacts 테이블 정의
├── templates/          # base.html, index.html(목록+검색), form.html(등록·수정 공용)
├── static/             # style.css
├── tests/              # test_app.py (pytest)
├── instance/           # 실행 시 생성되는 DB 파일 (git 제외)
├── requirements.txt
└── .gitignore
```

## 실행 명령 (Windows PowerShell)
```powershell
.\.venv\Scripts\Activate.ps1           # 가상환경 활성화
pip install -r requirements.txt        # 패키지 설치
flask --app app init-db                # DB 초기화 (최초 1회)
flask --app app run --debug            # 개발 서버 실행 → http://127.0.0.1:5000
```

## 테스트 명령
```powershell
pytest -v
```

## 코딩 규칙
- 주석은 한글로 작성한다.
- SQL은 반드시 파라미터 바인딩(`?` 플레이스홀더)을 사용한다. f-string, `+`, `%`, `.format()`으로 SQL 문자열에 값을 넣지 않는다.
  ```python
  # 올바른 예
  db.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
  # 금지
  db.execute(f"SELECT * FROM contacts WHERE id = {contact_id}")
  ```
- SQL은 `db.py`에만 둔다. 라우트(`app.py`)에서는 `db.py`의 함수를 호출한다.
- 입력 검증은 서버에서 한다. 상태를 바꾸는 요청(등록·수정·삭제)은 POST로 받고, 처리 후 리다이렉트한다(PRG 패턴).
- 템플릿 출력은 Jinja2 자동 이스케이프에 맡기고 `|safe`는 쓰지 않는다.
