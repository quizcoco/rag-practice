# 1. 프로젝트의 주요 기능과 목적 
RAG(Retrieval-Augmented Generation) 구조를 직접 구현하는 개인 학습 프로젝트입니다.

### 목적
이 프로젝트는 LLM 단독 응답의 한계를 보완하기 위해  
**외부 문서를 검색한 뒤, 해당 내용을 근거로 답변을 생성하는 RAG 구조**를  
직접 구현하고 이해하는 것을 목표로 합니다.

### 주요 기능
- 문서 및 사용자 질문 임베딩 생성
- Vector DB 저장 및 유사도 기반 문서 검색
- Parent / Child 구조를 통한 문맥 보완
- 검색된 문서를 컨텍스트로 LLM 응답 생성
- OpenAI 호환 API 기반 LLM 교체 가능 구조


---

# 2. 사전 요구사항
- Python 3.12
- LLM API Key (Groq 또는 OpenAI 호환)

---

# 3. 설치 방법 

### 저장소 클론
```bash
git clone https://github.com/mission-ground/yuna-rag-practice.git
cd yuna-rag-practice
```
### config.py 파일 생성
1. config.example.py를 복사하여 config.py로 이름을 변경합니다.
2. Groq 또는 OpenAI 호환 LLM API Key를 설정합니다.


### 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 라이브러리 설치
```bash
pip install groq
```
(필요한 추가 라이브러리는 추후 requirements.txt로 정리 예정)

---

# 4. 사용 예시 
```bash
python main.py

나 > OSI 7계층에 대해 설명해 주세요

AI >
OSI 7계층은 네트워크 통신을 계층별로 나눈 모델로,
물리 계층부터 응용 계층까지 총 7단계로 구성됩니다.
(문서 기반 응답)
```


---
# 5. 변경 로그 

#### v0.1.0

- 기본 RAG 파이프라인 구현
- 문서 임베딩 및 검색 기능 추가
 
#### v0.2.0

- LLM 응답 생성 단계 추가

#### v0.3.0
- Parent / Child 문서 구조 적용
- 검색 정확도 개선


---

# 6. 라이선스 정보 

이 프로젝트는 MIT License를 따릅니다.

- 개인 및 상업적 사용 가능
- 저작권 표시 필수
- 책임 제한
---

# 7. 지원창구 
GitHub Issues를 통해 버그 및 개선 사항을 제보해주세요.

### 개발자
GitHub: https://github.com/mission-ground
