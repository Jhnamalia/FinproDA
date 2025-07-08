import streamlit as st

st.set_page_config(page_title='First Portofolio Jihan', layout= 'wide', page_icon=':rocket:')

st.title('My Portfolio')
st.header('Data Analyst Final Project')

# Tambahkan judul dengan latar belakang hitam dan teks putih
st.sidebar.markdown("""
    <div style="background-color: #8D8741; border-radius: 8px; padding: 10px; text-align: center;">
        <h3 style="color: #FBEEC1; margin: 0;">My Page</h3>
    </div>
""", unsafe_allow_html=True)

# Radio button
page = st.sidebar.radio('**Choose what you want to know**', ['About Me','Projects','Customer Segmentation', 'Contacts'])


if page == 'Contacts':
    import contact
    contact.tampilkan_kontak()

if page == 'About Me':
    import about
    about.tampilkan_tentang()

if page == 'Projects':
    import project
    project.tampilkan_dashboard()    

if page == 'Customer Segmentation':
    import custseg
    custseg.tampilkan_segmentasi()