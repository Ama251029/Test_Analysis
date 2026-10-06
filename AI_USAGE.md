# AI Usage

## Tools

- ChatGPT

## Usage

### 1. 분석 방향 검토
- Q3의 Multi-turn Conversation 분석 방향을 검토하였다.

### 2. 데이터 구조 이해
- `messages`, `llm_label`과 같은 object 컬럼의 Python 내부 구조와 활용 방법을 검토하였다.

### 3. 전처리 및 지표 코드 작성 보조
- `llm_label`을 intent, category, subcategory 형태로 분리하는 전처리 로직을 설계하였다.
- Interaction / Conversation / User 단위 DataFrame 생성 함수를 설계하였다.
- 평균, 중앙값, 분위수 등 기술통계 계산 함수를 작성하는 데 활용하였다.

---

## Verification

AI가 제안한 코드와 분석 기준은 그대로 사용하지 않고 실제 데이터 결과를 통해 확인하였다.

- 전체 데이터 규모를 직접 확인하였다.
  - Interaction: 16,851
  - Conversation: 2,214
  - User: 203
- 결측치와 `(chatId, interactionCount)` 중복 여부를 직접 확인하였다.
- 하나의 `chatId`가 하나의 `userId`에만 연결되는지 확인하였다.
- `messages`와 `llm_label`의 실제 값을 출력하여 내부 구조를 확인하였다.
- 전처리 함수 실행 후 Interaction / Conversation / User DataFrame의 행 수가 원본 분석 단위와 일치하는지 확인하였다.
- 평균, 중앙값, 최소·최대값, P25/P75 등을 직접 계산하여 지표 분포를 확인하였다.
- Multi-turn / Multi-day 교차 결과를 확인하면서 정의와 원본 컬럼의 의미가 실제 데이터와 일치하는지 재검토하였다.

---

## Corrections

### 1. `chatTotalInteractionCount` 사용 방식 수정
초기에는 `chatTotalInteractionCount`를 Conversation의 전체 interaction 수로 그대로 사용할 수 있다고 판단하였다.

그러나 실제 분석 과정에서 원본 값과 관측된 interaction 수 사이의 차이가 확인되어,
실제 관측된 interaction 수는 `chatId`별 행 수를 기준으로 다시 계산하여 사용하는 방향으로 수정하였다.

### 2. Topic 활용 범위 축소
초기에는 Q2와 Q3에서 첫 질문의 `topic`도 비교 변수로 고려하였다.

하지만 `topic`이 `a1~a7` 형태의 식별자이며 각 값의 제품 관점 의미를 설명할 배경 정보가 부족하다고 판단하여,
Q2와 Q3의 핵심 변수에서는 제외하고 Q1의 전체 분포 확인에만 활용하기로 하였다.

### 3. Semester 활용 제외
`semester`는 원본 데이터에는 유지하지만 주요 사용자 행동 분석에서는 제외하기로 하였다.

학기별 제품 환경, 사용자 구성 등의 배경 정보가 없으므로
학기별 차이를 제품 사용 행동의 차이로 해석하기 어렵다고 판단하였다.

### 4. Session 정의 보류
일정 시간의 비활동을 기준으로 Session을 정의하는 방법을 검토하였다.

그러나 30분 또는 60분 등의 기준을 임의로 설정하지 않고,
실제 interaction 간 시간 간격 분포를 확인한 뒤 필요할 경우 정의하기로 하였다.