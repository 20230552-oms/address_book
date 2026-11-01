# 주소록 (Address Book)

Python **Flask**와 **SQLite**로 만든 주소록 관리 웹 애플리케이션입니다.
별도의 DB 서버 없이 파일 하나(`instance/addressbook.db`)에 데이터를 저장하므로 설치가 간단합니다.

파일 수는 적게 유지하면서도 실무에서 쓰는 구조(앱 팩토리, DB 모듈 분리, 템플릿 상속, 자동 테스트)를 따랐습니다.

## 주요 기능

| 기능 | 설명 |
|---|---|
| 목록 보기 | 모든 연락처를 이름 가나다순으로 표에 보여 줍니다. |
| 등록 | 이름(필수), 전화번호(필수), 이메일, 주소, 메모를 입력합니다. |
| 수정 | 기존 값이 채워진 폼에서 고칩니다. |
| 삭제 | 확인 창("정말 삭제하시겠습니까?")을 거쳐 삭제합니다. POST 요청으로만 처리합니다. |
| 검색 | 이름 또는 전화번호의 일부로 찾습니다. 전화번호는 하이픈이 있어도 없어도 검색됩니다. |
| 입력 검증 | 서버에서 검사하고, 틀린 칸과 이유를 한글로 알려 줍니다. |
| 반응형 화면 | 휴대폰에서는 표가 카드 형태로 바뀝니다. |

**입력 규칙**
- 이름: 필수, 30자 이하
- 전화번호: 필수, 숫자와 하이픈만 사용 (예: `010-1234-5678`, `01012345678`, `02-123-4567`)
- 이메일: 입력했다면 이메일 형식 (예: `hong@example.com`)

## 기술 스택

- Python 3.10 이상 (3.13에서 개발·테스트)
- Flask 3.1
- SQLite (파이썬 기본 내장 `sqlite3` 모듈, 추가 설치 없음)
- pytest 9 (테스트)

## 폴더 구조

```
address_book/
├── app.py              # 앱 생성(create_app), 화면별 라우트, 입력 검증
├── db.py               # DB 연결, 테이블 정의, init-db 명령, 등록·조회·수정·삭제·검색 함수
├── templates/
│   ├── base.html       # 모든 화면의 공통 틀 (상단 바, 안내 메시지)
│   ├── index.html      # 목록 + 검색
│   ├── form.html       # 등록·수정 공용 입력 폼
│   └── 404.html        # 없는 페이지·연락처 안내
├── static/
│   └── style.css       # 화면 디자인 (외부 CSS 라이브러리 없음)
├── tests/
│   ├── conftest.py     # 테스트 공통 준비물 (테스트 전용 임시 DB)
│   └── test_app.py     # 기능·검증·보안 테스트
├── instance/           # 실행하면 자동 생성. DB 파일이 저장됨 (git에 올리지 않음)
├── pytest.ini          # pytest 설정
├── requirements.txt    # 설치할 패키지 목록
├── CLAUDE.md           # Claude Code용 프로젝트 안내
└── README.md
```

## 화면과 주소

| 주소 | 화면 |
|---|---|
| `/` | 목록 (`/?q=검색어` 로 검색) |
| `/add` | 새 연락처 등록 |
| `/edit/<id>` | 연락처 수정 |
| `/delete/<id>` | 삭제 (POST 전용, 화면 없음) |

---

## 설치 방법

아래 명령은 모두 **프로젝트 폴더(`address_book`) 안에서** 실행합니다.

### 0. Python 설치 확인

| Windows (PowerShell) | Mac (터미널) |
|---|---|
| `python --version` | `python3 --version` |

`Python 3.10` 이상이 나오면 됩니다. 없으면 https://www.python.org/downloads/ 에서 설치하세요.
Windows에서 설치할 때는 첫 화면의 **"Add python.exe to PATH"를 꼭 체크**하세요.

### 1. 가상환경 만들기 (최초 1회)

가상환경은 이 프로젝트 전용 패키지 설치 공간입니다. 다른 프로젝트와 패키지 버전이 섞이지 않게 해 줍니다.

**Windows (PowerShell)**
```powershell
cd 경로\address_book
python -m venv .venv
```

**Mac (터미널)**
```bash
cd 경로/address_book
python3 -m venv .venv
```

### 2. 가상환경 켜기 (터미널을 새로 열 때마다)

**Windows (PowerShell)**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Mac (터미널)**
```bash
source .venv/bin/activate
```

켜지면 프롬프트 앞에 `(.venv)`가 붙습니다.

> **Windows에서 "이 시스템에서 스크립트를 실행할 수 없으므로…" 오류가 나면**
> 아래 명령을 한 번 실행한 뒤 다시 켜 보세요.
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```

### 3. 패키지 설치 (최초 1회)

가상환경이 켜진 상태에서 실행합니다. Windows와 Mac 모두 같습니다.

```bash
pip install -r requirements.txt
```

---

## DB 초기화 (최초 1회)

`instance/addressbook.db` 파일과 `contacts` 테이블을 만듭니다. Windows와 Mac 모두 같습니다.

```bash
flask --app app init-db
```

`데이터베이스를 초기화했습니다.`가 나오면 성공입니다.
여러 번 실행해도 기존 데이터는 지워지지 않습니다.

## 실행 방법

**Windows (PowerShell)**
```powershell
python app.py
```

**Mac (터미널)** - 아래 "Mac 5000번 포트 주의"를 먼저 읽어 보세요.
```bash
flask --app app run --debug --port 5001
```

`Running on http://127.0.0.1:5000`(Mac은 `5001`)이 나오면 브라우저에서 그 주소로 접속합니다.

- 서버가 켜져 있는 동안 **터미널 창을 닫지 마세요.** 닫거나 `Ctrl+C`를 누르면 서버가 꺼지고, 브라우저에 "사이트에 연결할 수 없음"이 뜹니다.
- debug 모드라서 코드를 고치고 저장하면 서버가 자동으로 다시 시작됩니다. 브라우저만 새로고침하면 됩니다.
- CSS를 고쳤는데 화면이 그대로면 강력 새로고침(Windows `Ctrl+F5`, Mac `Cmd+Shift+R`)을 하세요.

> **Mac 5000번 포트 주의**
> macOS 12(Monterey) 이후에는 **AirPlay 수신 모드**가 5000번 포트를 사용합니다.
> 그래서 `python app.py`(5000번)로 실행하면 "Address already in use" 오류가 나거나 브라우저에 403 오류가 뜰 수 있습니다.
> 위처럼 `--port 5001`로 실행하거나, `시스템 설정 → 일반 → AirDrop 및 Handoff → AirPlay 수신 모드`를 끄세요.

Windows에서도 `flask --app app run --debug` 명령으로 실행할 수 있습니다. `python app.py`와 결과가 같습니다.

## 테스트 방법

가상환경이 켜진 상태에서 실행합니다. Windows와 Mac 모두 같습니다.

```bash
pytest -v
```

마지막 줄에 `15 passed`가 나오면 모두 통과한 것입니다.

테스트는 매번 **임시 DB**를 새로 만들어 사용합니다. 실제 `instance/addressbook.db`의 데이터는 바뀌지 않습니다.

| 테스트 | 확인 내용 |
|---|---|
| 목록 | 목록 화면이 정상(200) 응답 |
| 등록 | 등록하면 목록에 나타남 |
| 수정 | 수정하면 화면과 DB 값이 바뀜 |
| 삭제 | 삭제하면 목록에서 사라짐, GET 요청으로는 삭제되지 않음 |
| 검색 | 이름 검색, 결과 없음 안내 |
| 입력 검증 | 이름이 비었거나 전화번호 형식이 틀리면 저장되지 않음 (등록·수정 모두) |
| 보안 | 검색어 `' OR '1'='1`(SQL 인젝션 시도)로 모든 데이터가 나오지 않음 |

## 처음부터 순서대로 (요약)

**Windows (PowerShell)**
```powershell
cd 경로\address_book
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
flask --app app init-db
pytest -v
python app.py
```

**Mac (터미널)**
```bash
cd 경로/address_book
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app init-db
pytest -v
flask --app app run --debug --port 5001
```

## 자주 겪는 문제

| 증상 | 원인과 해결 |
|---|---|
| `python`(또는 `pip`, `flask`)을 찾을 수 없음 | Python이 설치되지 않았거나 PATH에 없습니다. Mac은 `python3`을 쓰세요. `flask`, `pytest`가 없다고 나오면 가상환경이 켜져 있는지 확인하세요. |
| `ModuleNotFoundError: No module named 'flask'` | 가상환경을 켜지 않았거나 패키지를 설치하지 않았습니다. 2·3단계를 다시 하세요. |
| `no such table: contacts` | DB 초기화를 하지 않았습니다. `flask --app app init-db`를 실행하세요. |
| 브라우저에 "사이트에 연결할 수 없음" | 서버가 꺼져 있습니다. 터미널에서 실행 명령을 다시 입력하세요. |
| `Address already in use` | 이미 같은 포트에서 서버가 실행 중입니다. 기존 터미널에서 `Ctrl+C`로 끄거나, `--port 5001`처럼 다른 포트를 쓰세요. |

## 참고: 배포할 때 주의

이 프로젝트는 학습용 개발 서버 설정입니다. 다른 사람이 접속하는 서버에 올릴 때는 다음을 지켜야 합니다.
- debug 모드를 끕니다. debug 모드에서는 오류 화면을 통해 서버 코드를 실행할 수 있습니다.
- `SECRET_KEY` 환경변수에 추측하기 어려운 값을 넣습니다. 기본값 `"dev"`를 쓰지 않습니다.
- CSRF 보호를 추가합니다. 지금은 다른 사이트에서 삭제 요청을 보낼 수 있습니다.
