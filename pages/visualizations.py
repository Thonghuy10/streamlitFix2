import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show_visualizations():
    st.title("📈 Interactive Data Visualizations")
    st.write("Explore shopping trends through interactive charts and filters.")
    
    # Tải dữ liệu
    data = pd.read_excel("data/shopping_trends.xlsx")
    
    # Sidebar filters cho toàn bộ visualizations
    st.sidebar.subheader("🎛️ Visualization Filters")
    
    # Filters
    selected_categories = st.sidebar.multiselect(
        "Select Categories", 
        options=data["Category"].unique(), 
        default=data["Category"].unique()[:5]
    )
    
    selected_genders = st.sidebar.multiselect(
        "Select Genders", 
        options=data["Gender"].unique(), 
        default=data["Gender"].unique()
    )
    
    age_range = st.sidebar.slider(
        "Age Range", 
        min_value=int(data["Age"].min()), 
        max_value=int(data["Age"].max()), 
        value=(int(data["Age"].min()), int(data["Age"].max()))
    )
    
    # Áp dụng filters
    filtered_data = data[
        (data["Category"].isin(selected_categories)) &
        (data["Gender"].isin(selected_genders)) &
        (data["Age"] >= age_range[0]) &
        (data["Age"] <= age_range[1])
    ]
    
    if len(filtered_data) == 0:
        st.warning("No data matches your filters. Please adjust your selection.")
        return
    
    st.write(f"**Displaying data for {len(filtered_data)} records**")
    
    # Chart 1: Interactive Purchase Amount Analysis
    st.subheader("💰 Purchase Amount Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        chart1_type = st.selectbox("Chart Type", ["Bar Chart", "Box Plot", "Violin Plot"])
    with col2:
        group_by = st.selectbox("Group By", ["Category", "Gender", "Season"])
    
    if chart1_type == "Bar Chart":
        fig1 = px.bar(
            filtered_data.groupby(group_by)["Purchase Amount (USD)"].mean().reset_index(),
            x=group_by, 
            y="Purchase Amount (USD)",
            title=f"Average Purchase Amount by {group_by}",
            color=group_by
        )
    elif chart1_type == "Box Plot":
        fig1 = px.box(
            filtered_data, 
            x=group_by, 
            y="Purchase Amount (USD)",
            title=f"Purchase Amount Distribution by {group_by}",
            color=group_by
        )
    else:  # Violin Plot
        fig1 = px.violin(
            filtered_data, 
            x=group_by, 
            y="Purchase Amount (USD)",
            title=f"Purchase Amount Distribution by {group_by}",
            color=group_by
        )
    
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)
    
    # Chart 2: Age vs Purchase Amount Scatter Plot
    st.subheader("👥 Age and Purchase Patterns")
    
    col1, col2 = st.columns(2)
    with col1:
        color_by = st.selectbox("Color By", ["Gender", "Category", "Season"], key="scatter_color")
    with col2:
        size_by = st.selectbox("Size By", ["Purchase Amount (USD)", "Review Rating", "Previous Purchases"])
    
    fig2 = px.scatter(
        filtered_data,
        x="Age",
        y="Purchase Amount (USD)",
        color=color_by,
        size=size_by,
        hover_data=["Category", "Season", "Review Rating"],
        title="Age vs Purchase Amount",
        opacity=0.7
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Chart 3: Category Performance Dashboard
    st.subheader("📊 Category Performance")
    
    metric_choice = st.selectbox(
        "Select Metric", 
        ["Purchase Amount (USD)", "Review Rating", "Previous Purchases"]
    )
    
    category_data = filtered_data.groupby("Category").agg({
        "Purchase Amount (USD)": ["sum", "mean", "count"],
        "Review Rating": "mean",
        "Previous Purchases": "mean"
    }).round(2)
    
    if metric_choice == "Purchase Amount (USD)":
        chart_data = category_data[("Purchase Amount (USD)", "sum")].reset_index()
        chart_data.columns = ["Category", "Total Purchase Amount"]
        fig3 = px.bar(chart_data, x="Category", y="Total Purchase Amount", 
                     title="Total Purchase Amount by Category")
    elif metric_choice == "Review Rating":
        chart_data = category_data[("Review Rating", "mean")].reset_index()
        chart_data.columns = ["Category", "Average Rating"]
        fig3 = px.bar(chart_data, x="Category", y="Average Rating", 
                     title="Average Review Rating by Category")
    else:
        chart_data = category_data[("Previous Purchases", "mean")].reset_index()
        chart_data.columns = ["Category", "Average Previous Purchases"]
        fig3 = px.bar(chart_data, x="Category", y="Average Previous Purchases", 
                     title="Average Previous Purchases by Category")
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # Chart 4: Time Series / Seasonal Analysis
    st.subheader("🌟 Seasonal Analysis")
    
    seasonal_metric = st.selectbox(
        "Seasonal Metric", 
        ["Purchase Amount (USD)", "Review Rating", "Item Count"],
        key="seasonal"
    )
    
    if seasonal_metric == "Item Count":
        seasonal_data = filtered_data.groupby(["Season", "Gender"]).size().reset_index(name="Count")
        fig4 = px.bar(seasonal_data, x="Season", y="Count", color="Gender",
                     title="Number of Purchases by Season and Gender", barmode="group")
    else:
        seasonal_data = filtered_data.groupby(["Season", "Gender"])[seasonal_metric].mean().reset_index()
        fig4 = px.line(seasonal_data, x="Season", y=seasonal_metric, color="Gender",
                      title=f"Average {seasonal_metric} by Season and Gender", markers=True)
    
    st.plotly_chart(fig4, use_container_width=True)
    
    # Interactive Summary Statistics
    st.subheader("📋 Summary Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Top 5 Categories by Purchase Volume**")
        top_categories = filtered_data.groupby("Category")["Purchase Amount (USD)"].sum().nlargest(5)
        st.dataframe(top_categories)
    
    with col2:
        st.write("**Purchase Distribution by Gender**")
        gender_dist = filtered_data.groupby("Gender")["Purchase Amount (USD)"].agg(['count', 'mean', 'sum'])
        st.dataframe(gender_dist)