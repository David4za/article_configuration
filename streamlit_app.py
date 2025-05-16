import streamlit as st

# -------- PAGE SETUP --------
homepage = st.Page(
    page=r"pages/homepage.py",
    title="Home Page",
    icon=":material/home_pin:", # this is from Google Material
    default=True
)

dunker_config = st.Page(
    page=r"pages/dunker_configurator.py",
    title="Dunker Article Configurator",
    icon=":material/picture_as_pdf:"
)

thomson_config = st.Page(
    page=r"pages/thomson_configurator.py",
    title="Thomson Article Configurator",
    icon=":material/precision_manufacturing:"
)

# ----- PAGE NAVIGATION ----- 
pg = st.navigation(
    {
    # Key to remember here is each page needs to be a in a list
    "Home Page":[homepage],
    "Configurators":[dunker_config, thomson_config],
    }
)

# ----- RUN NAVIGATION ----- 
pg.run()
