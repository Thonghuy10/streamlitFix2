import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def show_insights():
    st.title("🔍 Advanced Data Insights")
    st.write("Deep dive into shopping patterns with advanced analytics and statistical insights.")
    
    # Tải dữ liệu
    data = pd.read_excel("data/shopping_trends.xlsx")
    
    # Interactive correlation analysis
    st.subheader("📊 Correlation Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        numeric_columns = ["Age", "Purchase Amount (USD)", "Review Rating", "Previous Purchases"]
        selected_columns = st.multiselect(
            "Select variables for correlation", 
            numeric_columns, 
            default=numeric_columns
        )
    
    with col2:
        correlation_method = st.selectbox("Correlation Method", ["Pearson", "Spearman"])
    
    if len(selected_columns) >= 2:
        correlation_data = data[selected_columns].corr(method=correlation_method.lower())
        
        fig_heatmap = px.imshow(
            correlation_data, 
            text_auto=True, 
            aspect="auto", 
            title=f"{correlation_method} Correlation Matrix",
            color_continuous_scale="RdBu_r"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Show strongest correlations
        st.write("**Strongest Correlations:**")
        correlations = []
        for i in range(len(correlation_data.columns)):
            for j in range(i+1, len(correlation_data.columns)):
                corr_value = correlation_data.iloc[i, j]
                correlations.append({
                    'Variables': f"{correlation_data.columns[i]} ↔ {correlation_data.columns[j]}",
                    'Correlation': f"{corr_value:.3f}"
                })
        
        correlations_df = pd.DataFrame(correlations)
        correlations_df['Abs_Correlation'] = correlations_df['Correlation'].astype(float).abs()
        top_correlations = correlations_df.nlargest(3, 'Abs_Correlation')[['Variables', 'Correlation']]
        st.dataframe(top_correlations, hide_index=True)
    
    # Customer Segmentation Analysis
    st.subheader("👥 Customer Segmentation")
    
    segment_by = st.selectbox(
        "Segment customers by", 
        ["Purchase Amount", "Age Group", "Review Rating", "Previous Purchases"]
    )
    
    if segment_by == "Purchase Amount":
        # Create purchase amount segments
        data['Segment'] = pd.cut(
            data['Purchase Amount (USD)'], 
            bins=3, 
            labels=['Low Spender', 'Medium Spender', 'High Spender']
        )
        segment_col = 'Segment'
    elif segment_by == "Age Group":
        data['Segment'] = pd.cut(
            data['Age'], 
            bins=[0, 25, 45, 65, 100], 
            labels=['Young (≤25)', 'Adult (26-45)', 'Middle-aged (46-65)', 'Senior (65+)']
        )
        segment_col = 'Segment'
    elif segment_by == "Review Rating":
        data['Segment'] = pd.cut(
            data['Review Rating'], 
            bins=[0, 3.0, 4.0, 5.0], 
            labels=['Low Rating (≤3.0)', 'Medium Rating (3.0-4.0)', 'High Rating (>4.0)']
        )
        segment_col = 'Segment'
    else:  # Previous Purchases
        data['Segment'] = pd.cut(
            data['Previous Purchases'], 
            bins=3, 
            labels=['New Customer', 'Regular Customer', 'Loyal Customer']
        )
        segment_col = 'Segment'
    
    # Create segmentation visualization
    segment_summary = data.groupby(segment_col).agg({
        'Purchase Amount (USD)': ['count', 'mean'],
        'Review Rating': 'mean',
        'Age': 'mean'
    }).round(2)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Segment size pie chart
        segment_counts = data[segment_col].value_counts()
        fig_pie = px.pie(
            values=segment_counts.values, 
            names=segment_counts.index,
            title=f"Customer Distribution by {segment_by}"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Segment metrics bar chart
        segment_metrics = data.groupby(segment_col)['Purchase Amount (USD)'].mean().reset_index()
        fig_bar = px.bar(
            segment_metrics, 
            x=segment_col, 
            y='Purchase Amount (USD)',
            title=f"Average Purchase Amount by {segment_by}"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Advanced Statistical Analysis
    st.subheader("📈 Statistical Analysis")
    
    analysis_type = st.selectbox(
        "Select Analysis Type", 
        ["Descriptive Statistics", "Distribution Analysis", "Outlier Detection"]
    )
    
    if analysis_type == "Descriptive Statistics":
        st.write("**Key Statistics Summary**")
        
        col1, col2 = st.columns(2)
        with col1:
            selected_var = st.selectbox("Select Variable", numeric_columns, key="desc_stats")
        
        with col2:
            group_var = st.selectbox("Group By", ["None", "Gender", "Category", "Season"], key="group_stats")
        
        if group_var == "None":
            stats_df = data[selected_var].describe().to_frame().T
            st.dataframe(stats_df, use_container_width=True)
        else:
            stats_df = data.groupby(group_var)[selected_var].describe()
            st.dataframe(stats_df, use_container_width=True)
    
    elif analysis_type == "Distribution Analysis":
        col1, col2 = st.columns(2)
        with col1:
            dist_var = st.selectbox("Select Variable", numeric_columns, key="dist_var")
        with col2:
            plot_type = st.selectbox("Plot Type", ["Histogram", "Box Plot", "Violin Plot"], key="dist_plot")
        
        if plot_type == "Histogram":
            fig = px.histogram(data, x=dist_var, nbins=30, title=f"Distribution of {dist_var}")
        elif plot_type == "Box Plot":
            fig = px.box(data, y=dist_var, title=f"Box Plot of {dist_var}")
        else:  # Violin Plot
            fig = px.violin(data, y=dist_var, title=f"Violin Plot of {dist_var}")
        
        st.plotly_chart(fig, use_container_width=True)
    
    else:  # Outlier Detection
        outlier_var = st.selectbox("Select Variable for Outlier Detection", numeric_columns, key="outlier_var")
        
        # Calculate IQR
        Q1 = data[outlier_var].quantile(0.25)
        Q3 = data[outlier_var].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = data[(data[outlier_var] < lower_bound) | (data[outlier_var] > upper_bound)]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(data))
        with col2:
            st.metric("Outliers Found", len(outliers))
        with col3:
            st.metric("Outlier %", f"{(len(outliers)/len(data)*100):.1f}%")
        
        # Visualize outliers
        fig = px.box(data, y=outlier_var, title=f"Outlier Detection for {outlier_var}")
        fig.add_hline(y=lower_bound, line_dash="dash", line_color="red", 
                     annotation_text="Lower Bound")
        fig.add_hline(y=upper_bound, line_dash="dash", line_color="red", 
                     annotation_text="Upper Bound")
        st.plotly_chart(fig, use_container_width=True)
        
        if len(outliers) > 0:
            st.write("**Outlier Records:**")
            st.dataframe(outliers[[outlier_var, "Category", "Gender", "Age"]].head(10))
    
    # Top Insights Summary
    st.subheader("💡 Key Insights")
    
    # Calculate key insights
    avg_purchase = data['Purchase Amount (USD)'].mean()
    top_category = data.groupby('Category')['Purchase Amount (USD)'].sum().idxmax()
    top_gender = data.groupby('Gender')['Purchase Amount (USD)'].sum().idxmax()
    peak_season = data.groupby('Season')['Purchase Amount (USD)'].sum().idxmax()
    
    insights = [
        f"💰 Average purchase amount is ${avg_purchase:.2f}",
        f"🏆 Top performing category: {top_category}",
        f"👤 {top_gender} customers generate higher total revenue",
        f"🌟 {peak_season} is the peak shopping season",
        f"📊 {data['Review Rating'].mean():.2f} average customer satisfaction rating"
    ]
    
    for insight in insights:
        st.write(f"• {insight}")