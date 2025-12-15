import streamlit as st
from datetime import datetime, time, timedelta
from PIL import Image
import io
st.set_page_config(
    page_title="个人简历生成器",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
    <style>
    /* 全局样式：纯白色背景 + 黑色文字 */
    .stApp {
        background-color: #ffffff !important;
        color: #000000 !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    /* 所有原生组件文字统一为黑色 */
    .stMarkdown, .stText, .stHeader, .stSubheader, .stExpanderHeader,
    .stRadio label, .stCheckbox label, .stSelectbox label, .stSlider label,
    .stFileUploader label, .stTimeInput label, .stDateInput label {
        color: #000000 !important;
    }
    /* 分栏容器：全屏宽度，保留少量内边距 */
    .stColumns {
        width: 100%;
        margin: 0;
        padding: 0 20px;
    }
    /* 表单输入组件：浅灰背景提升体验，黑色文字 */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stSlider > div > div > div,
    .stTimeInput > div > div > input,
    .stDateInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #f8f8f8;
        color: #000000 !important;
        border: 1px solid #dddddd;
        width: 100%;
    }
    /* 折叠面板：白色背景 + 浅灰边框 */
    .stExpander {
        background-color: #ffffff;
        border: 1px solid #dddddd;
        width: 100%;
    }
    /* 简历预览卡片：白色背景 + 轻微阴影，提升层次感 */
    .resume-card {
        background-color: #ffffff;
        border: 1px solid #eeeeee;
        border-radius: 6px;
        padding: 25px;
        color: #000000 !important;
        width: 100%;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    /* 预览区文字样式 */
    .resume-name {
        font-size: 24px;
        font-weight: bold;
        color: #000000 !important;
        margin: 0 0 10px 0;
    }
    .resume-info {
        font-size: 14px;
        color: #000000 !important;
        line-height: 1.8;
        margin: 5px 0;
    }
    .resume-section-title {
        font-size: 18px;
        font-weight: bold;
        color: #000000 !important;
        margin: 25px 0 10px 0;
        padding-bottom: 5px;
        border-bottom: 2px solid #2196F3;
    }
    .resume-content {
        font-size: 14px;
        color: #333333 !important;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; padding: 15px 0; background-color: #ffffff; margin: 0; color: #000000;'>📄 个人简历生成器</h1>", unsafe_allow_html=True)
st.divider()
col_input, col_preview = st.columns([1, 2], gap="large")
with col_input:
    st.header("🎯 个人信息填写")
    
  
    with st.expander("基础信息", expanded=True):
        st.write("**个人照片**（支持JPG/PNG格式）")
        photo_file = st.file_uploader(
            "点击上传头像",
            type=["jpg", "png", "jpeg"],
            accept_multiple_files=False,
            label_visibility="collapsed"
        )
        name = st.text_input("姓名", value="")
        gender = st.radio("性别", ["男", "女", "其他"], horizontal=True)
        position = st.text_input("应聘职位", value="")
        phone = st.text_input("联系电话", value="")
        email = st.text_input("电子邮箱", value="")
        birth_date = st.date_input(
            "出生日期",
            value=datetime(2000, 1, 1),
            min_value=datetime(1980, 1, 1),
            max_value=datetime.now() - timedelta(days=365*18)
        )


    with st.expander("教育与工作", expanded=True):
        education = st.selectbox("学历", ["高中", "大专", "本科", "硕士", "博士"], index=0)
        work_exp = st.slider("工作经验（年）", 0, 20, value=0, format="%d年")
        salary_range = st.slider("期望薪资（元/月）", 5000, 50000, value=(5000, 10000), step=500)
        contact_time = st.time_input("最佳联系时间", value=time(9, 0))

    with st.expander("能力与简介", expanded=True):
        languages = st.multiselect(
            "语言能力", 
            ["中文（母语）", "英语（CET-4）", "英语（CET-6）", "日语（N2）", "韩语（TOPIK3）"], 
            default=[]
        )
        st.write("**专业技能**（可多选）")
        skills = []
        skill_ops = [("Python", False), ("HTML/CSS", False), ("软件测试", False), ("SQL", False), ("自动化测试", False)]
        for skill, checked in skill_ops:
            if st.checkbox(skill, value=checked):
                skills.append(skill)
        intro = st.text_area("个人简介", value="", height=120, placeholder="请简要介绍你的工作经历、专业能力、求职优势等")

with col_preview:
    st.header("📋 简历实时预览")
    st.markdown("<div class='resume-card'>", unsafe_allow_html=True)
    

    avatar_row = st.columns([0.2, 0.8], gap="medium")
    with avatar_row[0]:
        if photo_file:
            img = Image.open(io.BytesIO(photo_file.read()))
            img.thumbnail((150, 180))
            st.image(img, width=150)
        else:
            st.image("https://via.placeholder.com/150x180?text=请上传头像", width=150)
    
    with avatar_row[1]:
        st.markdown(f"<p class='resume-name'>{name if name else '请填写姓名'}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='resume-info'>应聘职位：{position if position else '请填写应聘职位'}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='resume-info'>性别：{gender} | 出生年月：{birth_date.strftime('%Y年%m月')}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='resume-info'>学历：{education} | 工作经验：{work_exp}年</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='resume-info'>联系电话：{phone if phone else '请填写联系电话'} | 电子邮箱：{email if email else '请填写电子邮箱'}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='resume-info'>最佳联系时间：{contact_time.strftime('%H:%M')} | 期望薪资：{salary_range[0]}-{salary_range[1]}元/月</p>", unsafe_allow_html=True)


    st.markdown("<p class='resume-section-title'>专业技能</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='resume-content'>{', '.join(skills) if skills else '请在左侧勾选你的专业技能'}</p>", unsafe_allow_html=True)


    st.markdown("<p class='resume-section-title'>语言能力</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='resume-content'>{', '.join(languages) if languages else '请在左侧选择你的语言能力'}</p>", unsafe_allow_html=True)


    st.markdown("<p class='resume-section-title'>个人简介</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='resume-content'>{intro.replace('\\n', '<br>') if intro else '请在左侧填写个人简介'}</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
