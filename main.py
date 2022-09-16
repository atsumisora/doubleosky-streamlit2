import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('日本ゲーム業界株価可視化アプリ')

st.sidebar.write("""
# 日本ゲーム業界株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
""")

st.sidebar.write("""
## 表示日数選択
""")

days = st.sidebar.slider('日数', 1, 50, 20)

st.write(f"""
### 過去**{days}日間**の日本ゲーム業界株価
""")

@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()

    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

try:
    st.sidebar.write("""
    ## 株価の範囲指定
    """)

    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください。',
        0.0, 12000.0, (0.0, 12000.0)
    )

    tickers = {
        'サイバーエージェント': '4751.T',
        'ソニー': '6758.T',
        '任天堂': '7874.T',
        'スクウェア・エニックス': '9684.T',
        'バンダイナムコ': '7832.T',
        'カプコン': '9697.T',
        'コロプラ':'3668.T',
        'ネクソン':'3659.T'
    }
    df = get_data(days, tickers)
    companies = st.multiselect(
        '会社名を選択してください。',
        list(df.index),
        ['サイバーエージェント', 'ソニー', '任天堂']
    )
    if not companies:
        st.error('少なくとも一社は選んでください')
    else:
        data = df.loc[companies]
        st.write("### 株価 ",data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Price'}
        )

        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Price:Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            ) 
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        "おっと！なにかエラーが起きているようです"
    )

