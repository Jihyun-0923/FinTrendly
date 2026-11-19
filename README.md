# FinTrendly — AI:GO 제출용 공개 대시보드

OpenAI·네이버 API 호출 없이, 기존 AI 분석 CSV 454건을 읽어서 뉴스 주제와 키워드 변화 추이를 보여주는 **읽기 전용** Streamlit 앱입니다.

## 실행
```
pip install -r requirements.txt
streamlit run app.py
```

## 배포
1. `app.py`, `requirements.txt`, `data/fintrendly_results.csv`, `.gitignore`, `README.md`를 GitHub 저장소 최상위에 업로드합니다. ZIP 파일을 그대로 업로드하는 것이 아니라 압축 해제한 파일을 업로드해야 합니다.
2. https://share.streamlit.io 접속 후 GitHub 저장소, `main` 브랜치, `app.py`를 지정합니다.
3. 배포된 공개 URL을 시크릿 창에서 확인합니다.

## 주의
- 이 앱에는 뉴스 실시간 수집과 AI 재분석 기능이 **없습니다.** 따라서 새 API 이용료가 발생하지 않습니다.
- 포함된 CSV는 기존 AI 분석 결과이며, 기사 제목·출처 링크·AI 분류 내용을 공개합니다. 공개 전 원문과 저작권·개인정보를 확인하세요.
- 실제 매일 누적 서비스로 운영하려면 별도 영구 DB와 접근 통제가 필요합니다.
- **절대로** `.env`, API 키, SQLite DB 파일을 GitHub에 업로드하지 마세요.
