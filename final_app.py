import streamlit as st
import pandas as pd
import plotly.express as px

def get_dataframe_from_excel():
    # 读取Excel销售数据
    df = pd.read_excel('supermarket_sales.xlsx',
                       sheet_name='销售数据',
                       skiprows=1,
                       index_col='订单号')
    # 提取交易小时数
    df['小时数'] = pd.to_datetime(df["时间"], format="%H:%M:%S").dt.hour
    return df
def add_sidebar_func(df):
    with st.sidebar:
        st.header("请筛选数据：")
        
        # 城市筛选（支持空选，空选则不限制城市）
        city_unique = df["城市"].unique()
        city = st.multiselect("请选择城市：", options=city_unique, default=city_unique)
        
        # 顾客类型筛选（支持空选，空选则不限制顾客类型）
        customer_type_unique = df["顾客类型"].unique()
        customer_type = st.multiselect("请选择顾客类型：", options=customer_type_unique, default=customer_type_unique)
        
        # 性别筛选（支持空选，空选则不限制性别）
        gender_unique = df["性别"].unique()
        gender = st.multiselect("请选择性别：", options=gender_unique, default=gender_unique)
    
    # 动态构建筛选条件：仅包含有选择的类别
    filter_conditions = []
    if city:  # 城市有选择时，添加城市筛选
        filter_conditions.append(f"城市 == @city")
    if customer_type:  # 顾客类型有选择时，添加类型筛选
        filter_conditions.append(f"顾客类型 == @customer_type")
    if gender:  # 性别有选择时，添加性别筛选
        filter_conditions.append(f"性别 == @gender")
    
    # 拼接筛选条件（无选择时，条件为空，即返回全部数据）
    if filter_conditions:
        df_selection = df.query(" & ".join(filter_conditions))
    else:
        df_selection = df  # 所有类别都空选时，返回全部数据
    
    return df_selection
def product_line_chart(df):
    # 按产品类型统计销售额并绘图
    sales_by_product_line = df.groupby(by=["产品类型"])["总价"].sum().sort_values()
    fig_product_sales = px.bar(
        sales_by_product_line,
        x="总价",
        y=sales_by_product_line.index,
        orientation="h",
        title="<b>按产品类型划分的销售额</b>",
    )
    return fig_product_sales

def hour_chart(df):
    # 按小时统计销售额并绘图
    sales_by_hour = df.groupby(by=["小时数"])["总价"].sum()
    fig_hour_sales = px.bar(
        sales_by_hour,
        x=sales_by_hour.index,
        y="总价",
        title="<b>按小时划分的销售额</b>",
    )
    return fig_hour_sales

def main_page_demo(df):
    # 主页面布局与指标展示
        # 先判断数据是否为空
    if df.empty:
        st.warning("当前筛选条件下无数据，请调整筛选选项！")
        return  # 数据为空时直接返回，不执行后续指标计算
    st.title(":bar_chart: 销售仪表板")
        # 关键指标
    left_key_col, middle_key_col, right_key_col = st.columns(3)
    total_sales = int(df["总价"].sum())
    average_rating = round(df["评分"].mean(), 1)
    star_rating_string = ":star:" * int(round(average_rating, 0))
    average_sale_by_transaction = round(df["总价"].mean(), 2)

    with left_key_col:
        st.subheader("总销售额：")
        st.subheader(f"RMB ¥ {total_sales:,}")
    with middle_key_col:
        st.subheader("顾客评分的平均值：")
        st.subheader(f"{average_rating} {star_rating_string}")
    with right_key_col:
        st.subheader("每单的平均销售额：")
        st.subheader(f"RMB ¥ {average_sale_by_transaction}")

    st.divider()  # 水平分割线
    # 图表展示
    left_chart_col, right_chart_col = st.columns(2)
    with left_chart_col:
        hour_fig = hour_chart(df)
        st.plotly_chart(hour_fig, use_container_width=True)
    with right_chart_col:
        product_fig = product_line_chart(df)
        st.plotly_chart(product_fig, use_container_width=True)

def run_app():
    # 应用启动配置
    st.set_page_config(
        page_title="销售仪表板",
        page_icon=":bar_chart:",
        layout="wide"
    )
    # 数据读取与筛选
    sale_df = get_dataframe_from_excel()
    df_selection = add_sidebar_func(sale_df)
    # 渲染主页面
    main_page_demo(df_selection)

if __name__ == "__main__":
    run_app()
