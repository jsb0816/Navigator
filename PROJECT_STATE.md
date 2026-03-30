# 📋 PROJECT STATE — Requirements Traceability Matrix

| REQ ID | Title | Description | Priority |
|--------|-------|-------------|----------|
| REQ_001 | 구독 서비스 정보 수동 등록 | 사용자가 구독 중인 서비스의 이름, 결제일, 결제 금액을 직접 입력하여 등록할 수 있어야 한다. | Priority.MUST |
| REQ_002 | 등록된 구독 서비스 목록 조회 | 사용자가 등록한 모든 구독 서비스의 목록과 상세 정보를 확인할 수 있어야 한다. | Priority.MUST |
| REQ_003 | 구독 서비스 정보 수정 | 사용자가 등록한 구독 서비스의 이름, 결제일, 결제 금액 등의 정보를 수정할 수 있어야 한다. | Priority.MUST |
| REQ_004 | 구독 서비스 삭제 | 사용자가 더 이상 구독하지 않는 서비스를 목록에서 삭제할 수 있어야 한다. | Priority.MUST |
| REQ_005 | 월별 총 구독료 대시보드 표시 | 현재 월에 지출될 총 구독료 합계를 대시보드 화면에서 한눈에 확인할 수 있도록 제공해야 한다. | Priority.MUST |
| REQ_006 | 결제 예정일 푸시 알림 | 각 구독 서비스의 결제일 하루 전날, 해당 서비스의 결제 예정임을 사용자에게 푸시 알림으로 전송해야 한다. | Priority.SHOULD |
| REQ_007 | 구독 서비스 카테고리 태그 기능 | 사용자가 등록한 구독 서비스를 '엔터테인먼트', '쇼핑', '건강' 등과 같은 카테고리 태그로 분류할 수 있는 기능을 제공해야 한다. | Priority.COULD |
| REQ_008 | 다크 모드 UI 지원 | 앱의 사용자 인터페이스(UI)가 다크 모드를 지원하여 사용자가 선택할 수 있도록 제공해야 한다. | Priority.COULD |

---

# 🏗️ SA Analysis — Architecture & Execution Order

## 기술 스택 & 디자인 패턴

| 항목 | 선택 |
|------|------|
| Frontend | React |
| Backend | Spring Boot |
| Database | PostgreSQL |
| Design Pattern | Layered Architecture |

> **선택 근거:** React는 동적인 UI와 다크 모드 지원에 적합하며, Spring Boot는 안정적인 백엔드 API, 스케줄링 및 푸시 알림 통합에 강점을 가집니다. PostgreSQL은 구조화된 구독 데이터를 안정적으로 관리하고 집계하는 데 효율적이며, 계층형 아키텍처는 명확한 책임 분리와 유지보수성을 제공합니다.


## 요구사항 의존성 (DAG)

| REQ ID | Depends On |
|--------|-----------|
| REQ_001 | (없음) |
| REQ_002 | REQ_001 |
| REQ_003 | REQ_001, REQ_002 |
| REQ_004 | REQ_001, REQ_002 |
| REQ_005 | REQ_001 |
| REQ_006 | REQ_001 |
| REQ_007 | REQ_001, REQ_002 |
| REQ_008 | (없음) |

## 개발 순서 (위상 정렬)

1. **REQ_001**
2. **REQ_008**
3. **REQ_002**
4. **REQ_005**
5. **REQ_006**
6. **REQ_003**
7. **REQ_004**
8. **REQ_007**
