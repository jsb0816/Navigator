# 🚀 지능형 SDLC 다중 에이전트 파이프라인 (Intelligent SDLC Pipeline)

이 프로젝트는 대규모 언어 모델(LLM)과 LangGraph를 활용하여 소프트웨어 개발 생명주기(SDLC)의 초기 기획 및 아키텍처 설계 단계를 자동화하는 다중 에이전트(Multi-Agent) 시스템입니다.

현재 사용자의 자연어 아이디어를 기반으로 요구사항 명세서를 작성하는 **PM 에이전트**와, 이를 바탕으로 시스템 설계 및 개발 순서를 최적화하는 **SA 에이전트**가 구현되어 있습니다.

## ✨ 주요 기능 (구현된 에이전트)

### 1. 🧑‍💼 PM (Product Manager) 에이전트
사용자의 둥구름 잡는 줄글 기획 아이디어를 입력받아 개발 가능한 최소 단위로 분해합니다.
* **요구사항 원자화 (Atomizer):** 자연어에서 핵심 기능을 추출하여 고유 ID(`REQ_XXX`)를 부여합니다.
* **우선순위 산정 (Prioritizer):** 자원 한계를 고려하여 MoSCoW(Must/Should/Could/Won't) 기반 우선순위를 할당합니다.
* **상태 명세서 발행:** 최종 도출된 요구사항 추적 매트릭스(RTM)를 `PROJECT_STATE.md` 파일로 마크다운 형식으로 자동 저장합니다.

### 2. 🏛️ SA (Software Architect) 에이전트
PM이 작성한 `PROJECT_STATE.md`를 분석하여 기술적 청사진을 그립니다.
* **아키텍처 매핑:** 요구사항에 적합한 프레임워크, 데이터베이스, 디자인 패턴을 결정합니다.
* **의존성 그래프(DAG) 생성:** 요구사항 간의 선행/후행 의존 관계를 파악합니다.
* **위상 정렬 (Topological Sort):** 하부 의존성이 없는 기능부터 순차적으로 개발할 수 있도록 최적의 개발 순서(Queue)를 산출하여 `PROJECT_STATE.md` 하단에 추가(Append)합니다.

---

## 🛠️ 기술 스택

* **Backend:** Python, FastAPI, LangGraph, Pydantic, LangChain
* **LLM:** Google Gemini API (`gemini-1.5-flash` / `gemini-2.5-flash`)
* **Frontend:** React (Vite), TypeScript, Tailwind CSS

---

## 🚀 프로젝트 실행 방법

이 프로젝트는 Backend(FastAPI)와 Frontend(React) 서버를 각각 실행해야 합니다.

### 사전 준비 (Prerequisites)
* Python 3.9 이상
* Node.js 및 npm
* [Google AI Studio](https://aistudio.google.com/)에서 발급받은 Gemini API Key

### 1. 백엔드 (Backend) 설정 및 실행

```bash
# 1. backend 폴더로 이동
cd backend

# 2. 가상환경 생성 및 활성화 (권장)
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. 의존성 패키지 설치
pip install -r requirements.txt

# 4. 환경 변수 설정
# backend 폴더 최상단에 .env 파일을 생성하고 아래와 같이 API 키를 입력합니다.
# 🚨 주의: .env 파일은 절대 GitHub에 커밋하지 마세요! (.gitignore 확인 필수)
echo "GOOGLE_API_KEY=당신의_제미나이_API_키" > .env

# 5. FastAPI 서버 실행
uvicorn main:app --reload --port 8000


### 2.프론트엔드 (Frontend) 설정 및 실행
새로운 터미널 창을 열고 아래 명령어를 순서대로 실행합니다.

Bash
# 1. frontend 폴더로 이동
cd frontend

# 2. 의존성 패키지 설치
npm install

# 3. Vite 개발 서버 실행
npm run dev




### 디렉터리 구조
project_root/
├── backend/
│   ├── main.py                 # FastAPI 엔트리포인트
│   ├── requirements.txt        # 파이썬 라이브러리 목록
│   ├── .env                    # (Git에서 제외됨) API 키 보관
│   ├── agent/
│   │   ├── schemas.py          # Pydantic 데이터 모델 (RTM, SA_Result 등)
│   │   ├── state.py            # LangGraph State 구조
│   │   ├── pm_graph.py         # PM 에이전트 파이프라인
│   │   └── sa_graph.py         # SA 에이전트 파이프라인
│   └── utils/
│       └── file_io.py          # 마크다운 저장 유틸리티
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   └── src/
│       ├── App.tsx             # 메인 대시보드 UI
│       ├── api.ts              # 백엔드 통신(Axios/Fetch) 로직
│       └── components/         # 테이블, 아키텍처 뷰 등 UI 컴포넌트
└── README.md                   # 본 설명서