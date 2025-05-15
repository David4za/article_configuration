import streamlit as st

# -------- PAGE SETUP --------
homepage = st.Page(
    page=r"C:\Users\dawid.vandermerwe\OneDrive - ERIKS\Desktop\Projects\2025\Projects\Dawid\Work File\Thomson_Config\thomson_venv\pages\homepage.py",
    title="Home Page",
    icon=":material/home_pin:", # this is from Google Material
    default=True
)

dunker_config = st.Page(
    page=r"C:\Users\dawid.vandermerwe\OneDrive - ERIKS\Desktop\Projects\2025\Projects\Dawid\Work File\Thomson_Config\thomson_venv\pages\dunker_configurator.py",
    title="Dunker Article Configurator",
    icon=":material/picture_as_pdf:"
)

thomson_config = st.Page(
    page=r"C:\Users\dawid.vandermerwe\OneDrive - ERIKS\Desktop\Projects\2025\Projects\Dawid\Work File\Thomson_Config\thomson_venv\pages\thomson_configurator.py",
    title="Thomson Article Configurator",
    icon=":material/precision_manufacturing:"
)

# ----- PAGE NAVIGATION ----- 
pg = st.navigation(pages=[homepage, dunker_config, thomson_config])

# ----- RUN NAVIGATION ----- 
pg.run()