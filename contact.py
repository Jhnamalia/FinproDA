import streamlit as st

def tampilkan_kontak():
    st.markdown("## 🤝 Let's Connect!")
    st.markdown(
        """
        I'm always open to collaboration, questions, or just a friendly chat.  
        Feel free to reach out through any of the platforms below:
        """
    )

    # LinkedIn badge
    st.markdown(
        "[![LinkedIn](https://img.shields.io/badge/LinkedIn-Jihan%20Amalia-blue?logo=linkedin)](https://www.linkedin.com/in/jihanamalia/)"
    )

    # GitHub badge (diperbaiki)
    st.markdown(
        "[![GitHub](https://img.shields.io/badge/GitHub-Jhnamalia-black?logo=github)](https://github.com/Jhnamalia)"
    )

    # Email
    st.markdown("📧 **Email:** [Jihan.amalia02@gmail.com](mailto:Jihan.amalia02@gmail.com)")

    # WhatsApp
    st.markdown("📱 **WhatsApp:** [Click to chat](https://wa.me/6282217802091)")

    st.markdown("---")
    st.info("Looking forward to hearing from you! 😊")
