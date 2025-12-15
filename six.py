import streamlit as st
st.set_page_config(page_title="不一样的视频", layout="centered")
st.title("视频合集")
video_arr = [
    {
        "url": "https://www.w3school.com.cn/example/html5/mov_bbb.mp4",
        "title": "第1集",
        "episode": 1,
        "intro": "这是第1集的视频,主人公是小兔子。"
    },
    {
        "url": "https://www.w3schools.com/html/movie.mp4",
        "title": "第2集",
        "episode": 2,
        "intro": "这是第2集的视频，主角是狮子在咆哮。"
    },
    {
        "url": "https://media.w3.org/2010/05/sintel/trailer.mp4",
        "title": "第3集",
        "episode": 3,
        "intro": "这是第3集的视频，主要是不良人第七季。"
    }
]

if'ind' not in st.session_state:
    st.session_state['ind'] = 0
st.video(video_arr[st.session_state['ind']]['url'],autoplay=True)

def play(i):
    st.session_state['ind'] = int(i)

cols = st.columns(3)
for i in range(len(video_arr)):
    with cols[i]:
        st.button('第' + str(i + 1) + '集', use_container_width=True, on_click =play, args=([i]))# 视频简介区域
st.markdown('<div class="video-intro">', unsafe_allow_html=True)
st.subheader(f"{video_arr[st.session_state['ind']]['title']} 简介")
st.write(video_arr[st.session_state['ind']]['intro'])
st.markdown('</div>', unsafe_allow_html=True)

