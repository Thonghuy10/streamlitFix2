import streamlit as st
import base64
from datetime import date
from pages.overview import show_overview
from pages.visualizations import show_visualizations
from pages.insights import show_insights

# Cấu hình giao diện
st.set_page_config(
    page_title="Shopping Trends Dashboard",
    page_icon="🛍️",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Load custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    local_css("assets/style.css")
except FileNotFoundError:
    st.warning("Style file not found. Using default styles.")

# Hiệu ứng gradient cho header
def add_bg_gradient():
    st.markdown(
        """
        <style>
        .main-header {
            background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_gradient()

# Hiển thị header đẹp
st.markdown('<div class="main-header"><h1>Shopping Trends Dashboard</h1><p>Advanced analytics and visualization of consumer shopping patterns</p></div>', unsafe_allow_html=True)

# Sidebar nâng cấp
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/shopping-basket.png", width=80)
    st.title("Navigation")
    st.markdown("---")
    
    # Thêm animations vào các nút
    st.markdown(
        """
        <style>
        div[data-testid="stRadio"] > div {
            transition: all 0.3s ease;
        }
        div[data-testid="stRadio"] > div:hover {
            transform: translateX(5px);
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    page = st.radio(
        "📌 Choose a section",
        ["Overview", "Visualizations", "Advanced Insights"],
        key="navigation"
    )
    
    # Thêm metrics tóm tắt trong sidebar
    st.markdown("---")
    st.subheader("Dashboard Summary")
    
    col1, col2 = st.columns(2)
    col1.metric("Total Items", "847")
    col2.metric("Categories", "15")
    
    st.progress(80)
    st.caption("Data completeness: 80%")
    
    # Thêm footer đẹp hơn
    st.markdown("---")
    today = date.today().strftime("%B %d, %Y")
    st.markdown(f"""
    <div style='text-align: center; color: #2c3e50; padding: 10px; background-color: rgba(52,152,219,0.1); border-radius: 5px; border: 1px solid rgba(52,152,219,0.2);'>
        <small><strong>Powered by Streamlit & Python</strong></small><br>
        <small>Updated: {today}</small>
    </div>
    """, unsafe_allow_html=True)

# Container chính với hiệu ứng chuyển trang
main_container = st.container()

with main_container:
    # Hiệu ứng fade-in
    st.markdown(
        """
        <style>
        .fade-in {
            animation: fadeIn 0.8s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        </style>
        <div class="fade-in"></div>
        """,
        unsafe_allow_html=True
    )
      # Nội dung theo trang
    if page == "Overview":
        show_overview()
    elif page == "Visualizations":
        show_visualizations()
    elif page == "Advanced Insights":
        show_insights()

# Thêm watermark subtle
st.markdown(
    """
    <div style='position: fixed; bottom: 10px; right: 10px; opacity: 0.3;'>
    🛍️ Shopping Trends
    </div>
    """,
    unsafe_allow_html=True
)