from pathlib import Path
from collections import Counter
import pandas as pd
import streamlit as st

st.set_page_config(page_title="FinTrendly | 금융 뉴스 트렌드", page_icon="📈", layout="wide")
DATA = Path(__file__).parent / "data" / "fintrendly_results.csv"

@st.cache_data
def load_data():
    data = pd.read_csv(DATA, dtype={"id": str})
    for col in ["title", "category", "keywords", "rationale", "url"]:
        data[col] = data[col].fillna("").astype(str)
    data["date"] = pd.to_datetime(data["date"], errors="coerce").dt.date
    return data.dropna(subset=["date"])

st.title("📈 FinTrendly")
st.caption("AI 기반 금융 뉴스 분석 및 시장 트렌드 시각화 대시보드")
st.info("📌 AI:GO 제출용 시연 화면입니다. 사전에 수집·분석한 뉴스만 보여주며, 새로운 뉴스 수집이나 유료 AI API 호출은 실행하지 않습니다.")

if not DATA.exists():
    st.error("분석 CSV 파일이 없습니다. data/fintrendly_results.csv를 확인하세요.")
    st.stop()

df = load_data()
if df.empty:
    st.warning("표시할 뉴스가 없습니다.")
    st.stop()

st.sidebar.header("분석 조건")
dates = sorted(df["date"].unique())
chosen_dates = st.sidebar.date_input("분석 기간", value=(dates[0], dates[-1]), min_value=dates[0], max_value=dates[-1])
if isinstance(chosen_dates, tuple) and len(chosen_dates) == 2:
    start, end = chosen_dates
else:
    start, end = dates[0], dates[-1]
options = sorted(df["category"].unique())
selected = st.sidebar.multiselect("금융 주제", options, default=options)
filtered = df[(df["date"] >= start) & (df["date"] <= end) & df["category"].isin(selected)].copy()

if filtered.empty:
    st.warning("선택한 조건에 해당하는 뉴스가 없습니다.")
    st.stop()

counts = filtered["category"].value_counts()
issues = Counter()
for keywords in filtered["keywords"]:
    for word in set(x.strip() for x in keywords.split(",") if x.strip()):
        issues[word] += 1

m1, m2, m3, m4 = st.columns(4)
m1.metric("선택 기간 뉴스", f"{len(filtered):,}건")
m2.metric("분류 주제", f"{len(counts)}개")
m3.metric("추출 키워드 종류", f"{len(issues):,}개")
m4.metric("데이터 최신 발행일", str(max(filtered["date"])))

left, right = st.columns(2)
with left:
    st.subheader("주제별 뉴스 건수")
    st.bar_chart(counts.rename("기사 수"), horizontal=True)
with right:
    st.subheader("날짜별 뉴스 건수")
    per_day = filtered.groupby("date").size().rename("기사 수")
    st.line_chart(per_day)

st.subheader("날짜·주제별 뉴스 언급량")
by_date_topic = filtered.groupby(["date", "category"]).size().unstack(fill_value=0)
st.line_chart(by_date_topic)

st.subheader("주요 키워드 TOP 10")
st.caption("AI가 기사별로 추출한 키워드의 등장 *기사 수* 기준입니다. 실제 기사 본문의 전체 단어 출현 횟수는 아닙니다.")
if issues:
    st.bar_chart(pd.Series(dict(issues.most_common(10)), name="기사 수"), horizontal=True)

st.subheader("주요 관심 이슈 3개")
st.caption("선택 기간에 가장 많은 기사에 붙은 키워드를 기준으로 자동 선정한 요약 목록입니다. 시장 영향이나 미래 가격을 예측하지 않습니다.")
for i, (keyword, n) in enumerate(issues.most_common(3), start=1):
    examples = filtered[filtered["keywords"].str.contains(keyword, regex=False, case=False)].head(3)
    with st.expander(f"{i}. {keyword} — 관련 기사 {n}건", expanded=(i == 1)):
        for _, r in examples.iterrows():
            st.markdown(f"- [{r['title']}]({r['url']}) ({r['date']})")

st.subheader("AI 뉴스 분류 결과")
show = filtered.sort_values("date", ascending=False)[["date", "title", "category", "keywords", "rationale", "url"]].rename(columns={"date":"발행일", "title":"기사 제목", "category":"분류", "keywords":"핵심 키워드", "rationale":"분류 근거", "url":"기사 링크"})
st.dataframe(show, use_container_width=True, hide_index=True, column_config={"기사 링크":st.column_config.LinkColumn("기사 링크")})
st.download_button("현재 필터 결과 CSV 내려받기", data=show.to_csv(index=False).encode("utf-8-sig"), file_name="fintrendly_public_results.csv", mime="text/csv")
st.caption("분류·키워드·근거는 AI 생성 결과이며 사람의 전수 검증이 완료된 정보가 아닙니다. 뉴스 API 검색 결과의 표본이므로 전체 금융 뉴스 시장을 대표하지 않습니다.")
