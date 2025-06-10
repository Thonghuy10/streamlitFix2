import streamlit as st
import pandas as pd

def show_overview():
    st.title("Shopping Trends Overview")
    st.write("Explore key insights from shopping trends data.")

    # Tải dữ liệu
    data = pd.read_excel("data/shopping_trends.xlsx")
    
    # Hiển thị thông tin tổng quan về dataset
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", len(data))
    with col2:
        st.metric("Total Categories", data["Category"].nunique())
    with col3:
        st.metric("Avg Purchase Amount", f"${data['Purchase Amount (USD)'].mean():.2f}")
    with col4:
        st.metric("Avg Rating", f"{data['Review Rating'].mean():.2f}")

    st.markdown("---")
    
    # Bộ lọc tương tác
    st.subheader("🔍 Filter Dataset")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        gender = st.selectbox("Select Gender", ["All"] + sorted(data["Gender"].unique().tolist()))
    with col2:
        category = st.selectbox("Select Category", ["All"] + sorted(data["Category"].unique().tolist()))
    with col3:
        season = st.selectbox("Select Season", ["All"] + sorted(data["Season"].unique().tolist()))

    # Áp dụng bộ lọc
    filtered_data = data.copy()
    if gender != "All":
        filtered_data = filtered_data[filtered_data["Gender"] == gender]
    if category != "All":
        filtered_data = filtered_data[filtered_data["Category"] == category]
    if season != "All":
        filtered_data = filtered_data[filtered_data["Season"] == season]
    
    # Hiển thị số lượng records sau khi filter
    st.write(f"**Showing {len(filtered_data)} of {len(data)} records**")
    
    # Hiển thị dữ liệu đã được filter
    st.subheader("📊 Dataset")
    st.dataframe(filtered_data, use_container_width=True)