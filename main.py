import streamlit as st

st.set_page_config(
    page_title="Shift Cipher Decrypter",
    page_icon=":unlock:",
    initial_sidebar_state="expanded",
    menu_items={"About": "This web-based application was developed by :grey-background[Wong Ka Ho] with an open-sourced python library [**Streamlit**](https://github.com/streamlit/streamlit) to provide graphical user interface."}
)

pages = {
    "": [
        st.Page("pages/home_page.py", title="Home", icon=":material/home:")],
    "Tools": [
        st.Page("pages/encrypter_page.py", title="Encrypter", icon=":material/lock:"),
        st.Page("pages/decrypter_page.py", title="Decrypter", icon=":material/lock_open_right:")],
    #"Other": [
    #    st.Page("pages/about_page.py", title="About", icon=":material/info:")]
}

pg = st.navigation(pages)
pg.run()