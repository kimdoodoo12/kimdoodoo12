<div align="center">
  <img src="assets/header.svg" width="100%" alt="어둠의 개발자가 되고 싶어서!" />
  <br/><br/>
  <img src="assets/character.svg" width="100%" alt="두두의 상태창" />
  <br/><br/>
  <a href="mailto:kimdoodoo12@gmail.com"><img src="https://img.shields.io/badge/Email-kimdoodoo12%40gmail.com-7c3aed?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>
</div>

## 🛠 Tech Stack

<p>
  <img src="https://skillicons.dev/icons?i=java,spring,py,django,react,js,flutter,dart,mysql,redis,aws,docker,nginx,git,githubactions&theme=dark" alt="tech stack" />
</p>

<a name="projects"></a>

## 📂 Projects

| 프로젝트 | 한 줄 소개 | 형태 |
|---|---|---|
| [**SongRush**](#songrush) | 같은 순간에 같은 곡을 듣고 애니 제목을 맞히는 멀티플레이 게임 | 개인 · 운영 중 |
| [**English INSSA**](#english-inssa) | 사전 슬랭 3만 개에서 실제로 쓰이는 384개를 골라낸 데이터 파이프라인 | 졸업 작품 · 파이프라인 담당 |
| [**이음 옥션**](#ieum-auction) | 취약계층이 만든 상품을 경매로 파는 사회적 가치 플랫폼 | 팀 4명 · 팀장 |
| [**시간표 최적화**](#schedule) | 담금질 기법으로 공강 적은 시간표 자동 생성 | 개인 |

<a name="songrush"></a>

### SongRush

<a href="https://github.com/kimdoodoo12/SongRushApp"><img src="https://img.shields.io/badge/GitHub-SongRushApp-181717?style=for-the-badge&logo=github" alt="저장소" /></a> <a href="https://animeopguessr.com"><img src="https://img.shields.io/badge/Live-animeopguessr.com-ff8a4c?style=for-the-badge" alt="서비스" /></a>

<img src="https://raw.githubusercontent.com/kimdoodoo12/SongRushApp/dev/docs/images/demo.gif" width="100%" alt="PC와 휴대폰이 같은 방에서 한 곡을 진행하는 실제 화면" />

친구들과 노래 맞히기를 하면 누가 먼저 들었는지 늘 애매했습니다. 그래서 모두가 같은 순간에 같은 곡을 듣고, 서버가 먼저 맞힌 사람을 가리는 애니 OP/ED 게임을 만들었습니다. 기획부터 AWS 배포·운영까지 혼자 했고, 코드는 제가 설계한 AI 에이전트 팀이 쓰고 저는 결정과 검증 구조를 맡았습니다.

주로 고민한 것: 지연이 다른 기기들을 같은 순간에 재생시키기, 거의 동시에 들어온 정답 판정, 곡마다 길어지던 로딩

`Spring Boot WebSocket` `React` `Flutter` `AWS` `Claude Code` · 개인 · 2026.11 ~ 운영 중

<sub><a href="#projects">↑ 목록으로</a></sub>

---

<a name="english-inssa"></a>

### English INSSA 슬랭 데이터 파이프라인

<a href="https://github.com/kimdoodoo12/english-inssa-data-pipeline"><img src="https://img.shields.io/badge/GitHub-english--inssa--data--pipeline-181717?style=for-the-badge&logo=github" alt="저장소" /></a>

<img src="assets/shots/inssa-screens.png" width="100%" alt="파이프라인이 고른 슬랭이 쓰이는 서비스 화면" />

팀 졸업 작품인 영어 슬랭 학습 서비스에서 데이터 파이프라인을 혼자 맡았습니다. 사전에 실린 슬랭 3만여 개 중 실제로 쓰이는 384개를 골라 서비스에 넣었고, 위 화면들이 그 데이터로 돌아갑니다.

주로 고민한 것: 메모리에 올릴 수 없는 덤프 처리, LLM 호출 비용, LLM 결과를 그대로 믿지 않는 법

`Python` `OpenAI API` `pytest` `GitHub Actions` · 졸업 작품 · 2026.03 ~ 06

<sub><a href="#projects">↑ 목록으로</a></sub>

---

<a name="ieum-auction"></a>

### 이음 옥션

<a href="https://github.com/kimdoodoo12/social-auction-platform"><img src="https://img.shields.io/badge/GitHub-social--auction--platform-181717?style=for-the-badge&logo=github" alt="저장소" /></a>

<img src="https://raw.githubusercontent.com/kimdoodoo12/social-auction-platform/main/docs/images/bidding.gif" width="100%" alt="두 사용자가 같은 경매에 입찰하는 실제 화면" />

취약계층이 만든 상품을 협약 기관과 함께 경매로 파는 서비스입니다. 4인 팀의 팀장으로 기획과 스프린트를 이끌었고, 백엔드에서는 서버 재시작 시 경매 종료 복구와 관리자 API를 맡았습니다.

주로 고민한 것: 시작 시각 없이 첫 입찰부터 흐르는 경매 규칙, 동시에 들어온 입찰의 순서

`Spring Boot` `JPA` `Redis` `SSE` `React` · 팀 4명 · 2026.09 ~ 10

<sub><a href="#projects">↑ 목록으로</a></sub>

---

<a name="schedule"></a>

### 시간표 최적화

<a href="https://github.com/kimdoodoo12/schedule_optimization"><img src="https://img.shields.io/badge/GitHub-schedule__optimization-181717?style=for-the-badge&logo=github" alt="저장소" /></a>

<img src="assets/shots/schedule-result.png" width="70%" alt="프로그램이 만든 시간표 결과" />

15~18학점 안에서 공강은 줄이고 하루 수업은 고르게 되는 시간표를 담금질 기법으로 찾는 프로그램입니다. 위 그림은 실제 강의 데이터로 돌린 결과입니다(교수명은 가렸습니다).

`Python` · 개인

<sub><a href="#projects">↑ 목록으로</a></sub>

---

### 그 밖의 프로젝트

| 프로젝트 | 설명 | 기술 |
|---|---|---|
| [AI_Professor](https://github.com/kimdoodoo12/AI_Professor) | 강의 자료(PDF·이미지) 업로드 → OCR → 요약 → OX·객관식 퀴즈 생성 | Django, Tesseract, OpenCV, OpenAI |
| [SwingCalendar](https://github.com/kimdoodoo12/SwingCalendar) | 일정 관리 캘린더 + ODsay API 지하철 경로 안내 | Java Swing |

## 📊 Activity

<img src="https://raw.githubusercontent.com/kimdoodoo12/kimdoodoo12/output/stats.svg" width="100%" alt="모험 기록: 기여 수, 연속 기록, 주 사용 언어" />

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/kimdoodoo12/kimdoodoo12/output/github-snake-dark.svg" />
  <img src="https://raw.githubusercontent.com/kimdoodoo12/kimdoodoo12/output/github-snake.svg" width="100%" alt="contribution snake" />
</picture>
