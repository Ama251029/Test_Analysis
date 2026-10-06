# StudyChat User Behavior Analysis

## 프로젝트 목적

StudyChat 대화 데이터를 활용하여 사용자가 AI Assistant를 어떤 방식으로 이용하는지 파악하고,
지속적인 사용과 함께 나타나는 행동 특성을 분석한다.

분석에서는 사용자 수나 전체 대화량만 확인하는 것이 아니라,
사용자가 서비스를 얼마나 자주 이용하는지, 하나의 대화를 어떤 방식으로 이어가는지,
어떤 유형의 질문을 하는지 등을 User, Conversation, Interaction 단위로 구분하여 확인한다.

최종적으로는 분석 결과를 바탕으로 사용자 경험을 개선하기 위한
데이터 기반 Product Recommendation을 제안하는 것을 목표로 한다.

## 분석 개요

### 데이터 분석 단위

원본 데이터의 한 행을 하나의 관측 Interaction으로 보고,
분석 목적에 따라 다음 세 가지 단위의 데이터를 구성한다.

- **Interaction**
  - 사용자의 prompt와 AI response 한 쌍
  - 사용 시간, 질문 Intent, Prompt/Response 특성 분석에 활용

- **Conversation**
  - 동일한 `chatId`에 속하는 Interaction 집합
  - 대화 길이, 활동일 수, Multi-turn 여부, 첫 질문 특성 분석에 활용

- **User**
  - 동일한 `userId`에 속하는 전체 사용 기록
  - 대화 수, 상호작용 수, 활동일 수, 지속 사용 여부 분석에 활용

### Q1. 사용자는 AI Assistant를 어떻게 사용하고 있는가?

전체적인 이용 패턴을 User, Conversation, Interaction 단위로 확인한다.

주요 분석 항목은 다음과 같다.

- 사용자당 대화 수
- 사용자당 상호작용 수
- 사용자당 활동일 수
- 대화당 관측 상호작용 수
- 대화 활동일 수 및 사용 기간
- Multi-turn / Multi-day Conversation 비율
- 시간대별 사용량
- 질문 Intent 분포

수치형 지표는 평균과 중앙값을 기본으로 확인하고,
P25, P75, 최소·최대값과 분포를 함께 사용하여
일반적인 사용 수준과 사용량 편향을 확인한다.

원본 `interactionCount`와 `chatTotalInteractionCount`의 일부 불일치가 확인되어,
Conversation의 길이와 Multi-turn 여부는 현재 데이터에서 실제로 관측된 Interaction을 기준으로 재계산하였다.


### Q2. 지속 사용자와 일회성 사용자는 어떤 차이가 있는가?

지속 사용은 사용 기간의 개념을 반영하여
서로 다른 날짜에 서비스를 이용했는지를 기준으로 정의한다.

- **One-day User**
  - 관측 기간 내 한 날짜에서만 활동한 사용자

- **Returning User**
  - 서로 다른 날짜에 2일 이상 활동한 사용자

두 사용자 그룹의 전체 사용량과 초기 사용 행동을 비교한다.

주요 비교 항목은 다음과 같다.

- 총 대화 수
- 총 상호작용 수
- 활동일 수
- 첫 사용일의 대화 수
- 첫 사용일의 상호작용 수
- 첫 대화의 관측 상호작용 수
- 첫 대화의 Multi-turn 여부
- 첫 질문 길이
- 첫 질문 Intent
- 두 번째 활동일까지의 기간

전체 누적 사용량은 그룹 특성을 파악하는 참고 지표로 사용하고,
주요 행동 차이는 첫 사용일과 첫 대화의 특성을 중심으로 확인한다.