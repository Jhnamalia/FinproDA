import streamlit as st
import base64

def tampilkan_tentang():
    # Baca gambar sebagai base64
    with open("jihan_amalia.jpg", "rb") as img_file:
        img_bytes = img_file.read()
        img_base64 = base64.b64encode(img_bytes).decode()

    # HTML + CSS untuk tampilkan gambar bulat
    profile_img_html = f"""
        <div style="display: flex; justify-content: flex-end; margin-top: -40px;">
            <img src="data:image/jpeg;base64,{img_base64}" 
                 alt="Profile Picture"
                 style="width: 300px; height: 300px; object-fit: cover; border-radius: 50%;" />
        </div>
    """

    # Layout dua kolom
    col1, col2 = st.columns([2, 1])

    with col2:
        st.markdown(profile_img_html, unsafe_allow_html=True)

    with col1:
        st.markdown("## 👋 Hello, I’m Jihan!")
        st.markdown("🌍 Based in **Jakarta, Indonesia**")
        st.markdown("🎓 Currently joining a **6-month Full Stack Data Science Bootcamp** with [dibimbing.id](https://dibimbing.id)")
        st.markdown("---")
        st.markdown("### 🧠 Final Project Summary")
        st.markdown(
            """
            I have completed my final project as a **Data Analyst**, focusing on hotel booking data in Malaysia for the year 2024.  
            Using **Customer Segmentation Analysis**, I analyzed **6,050 transactions** across three hotels to uncover insights into customer behavior and provide business recommendations.
            """
        )
        st.markdown("📊 Dataset Source: [Kaggle - Hotel Sales 2024](https://www.kaggle.com/datasets/tianrongsim/hotel-sales-2024/data)")
        st.markdown("📎 Project Slide Deck: [Google Slides](https://drive.google.com/file/d/1LLCgBu7N_E8o8ElAO3j3-xVbjisD9w-I/view?usp=drive_link)")
        st.markdown("---")
        st.markdown("### 📬 Contact Me")
        st.markdown("Please feel free to reach out with any Questions, compliments, or concerns. Let’s collaborate and connect!")