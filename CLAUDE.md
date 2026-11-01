# 주소록 웹 애플리케이션

## 프로젝트 목적
Python Flask와 SQLite로 만든 주소록 관리 웹앱이다. 별도 DB 서버 없이 파일 하나(`instance/addressbook.db`)에 저장한다.
대학 4학년 학생이 따라 할 수 있도록 파일 수는 적게, 구조는 실무형으로 유지한다.
설치·실행 안내는 README.md에 있다. 명령이나 구조를 바꾸면 README.md도 함께 고친다.

- 항목: 이름(필수), 전화번호(필수), 이메일, 주소, 메모, created_at(등록 시각, 자동)
- 기능: 목록 보기, 등록, 수정, 삭제, 이름·전화번호 검색, 서버 입력 검증
- 외부 패키지는 Flask, pytest만 사용한다. ORM, Flask-WTF, CSS 라이브러리 등은 추가하지 않는다.

## 폴더 구조
```
address_book/
├── app.py              # 앱 팩토리 create_app(), 라우트, read_form()·validate() 입력 검증
├── db.py               # DB 연결(get_db), 테이블 정의(SCHEMA), init-db 명령, CRUD·검색 함수
├── templates/          # base.html(공통 틀), index.html(목록+검색), form.html(등록·수정 공용), 404.html
├── static/             # style.css (색은 맨 위 :root 변수에 모아 둠, 600px 이하 반응형)
├── tests/              # conftest.py(임시 DB fixture: app, client, count_contacts), test_app.py
├── instance/           # 실행 시 생성되는 DB 파일 (git 제외)
├── pytest.ini          # pytest 설정 (pythonpath = . , testpaths = tests)
├── requirements.txt    # pip freeze 결과 (버전 고정)
├── README.md           # 설치·실행·테스트 안내 (Windows, Mac)
└── .gitignore
```

## 라우트
| 주소 | 메서드 | 함수 | 템플릿 |
|---|---|---|---|
| `/` (`?q=`) | GET | `index` | index.html |
| `/add` | GET, POST | `add` | form.html |
| `/edit/<int:contact_id>` | GET, POST | `edit` | form.html |
| `/delete/<int:contact_id>` | POST | `delete` | (목록으로 리다이렉트) |
| 404 | - | `not_found` | 404.html |

## 실행 명령
Windows (PowerShell)
```powershell
.\.venv\Scripts\Activate.ps1           # 가상환경 활성화
pip install -r requirements.txt        # 패키지 설치
flask --app app init-db                # DB 초기화 (최초 1회, 다시 실행해도 데이터 유지)
python app.py                          # 개발 서버 실행 (debug) → http://127.0.0.1:5000
```

Mac (터미널)
```bash
source .venv/bin/activate
pip install -r requirements.txt
flask --app app init-db
flask --app app run --debug --port 5001   # 5000번은 macOS AirPlay 수신 모드와 충돌
```

## 테스트 명령
```bash
pytest -v
```
- 테스트는 `tmp_path`의 임시 DB를 쓴다. 실제 `instance/addressbook.db`를 쓰는 테스트는 만들지 않는다.
- 기능을 추가하거나 바꾸면 tests/test_app.py에 테스트를 추가하고 `pytest -v`가 모두 통과해야 한다.

## 코딩 규칙
- 주석은 한글로 작성한다.
- SQL은 반드시 파라미터 바인딩(`?` 플레이스홀더)을 사용한다. f-string, `+`, `%`, `.format()`으로 SQL 문자열에 값을 넣지 않는다. LIKE 검색도 `%`를 파이썬에서 붙인 값을 `?`로 넘기고, 사용자 입력은 `escape_like()`를 거친다.
  ```python
  # 올바른 예
  db.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
  # 금지
  db.execute(f"SELECT * FROM contacts WHERE id = {contact_id}")
  ```
- SQL은 `db.py`에만 둔다. 라우트(`app.py`)에서는 `db.py`의 함수를 호출한다.
- 입력 검증은 서버(`validate()`)에서 한다. 오류는 `{칸 이름: 한글 메시지}` 사전으로 돌려주고, 폼을 다시 보여 줄 때 입력값을 유지한다.
- 상태를 바꾸는 요청(등록·수정·삭제)은 POST로 받고, 처리 후 리다이렉트한다(PRG 패턴).
- 템플릿 출력은 Jinja2 자동 이스케이프에 맡기고 `|safe`는 쓰지 않는다. 템플릿 확장자는 `.html`을 유지한다.
- 없는 id는 `abort(404)`로 처리한다.
