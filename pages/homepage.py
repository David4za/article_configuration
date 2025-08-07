import streamlit as st

st.title(":material/home: Home Page")
st.markdown(
   """
   **Welcome to the EN07 Article Creation Tool** 👋

This internal tool was built to simplify and streamline the article creation process for Thomson actuators.

**What’s included:**
- ✅ The familiar **Dunker PDF Reader**
- 🧩 The **Thomson Article Configurator** (Alpha version)

---

### 🔧 Thomson Configurator:
Quickly generate Electrak **XD**, **HD**, **MD**, or **GX DC actuators**.  
You’ll get:
- A detailed **article code breakdown**
- A formatted **Article Description 1** for SAP

---

### 🧪 Test Examples:
- **XD**: `XD24B160-0150COORKHSN`  
- **HD**: `HD24B026-0100ELX2NPSD`  
- **GX**: `D24C2KB506M3NN-AMM`  
- **MD**: `MD24A200-0150XXP2NNSD`

---

### 📝 Notes:
- This is an **Alpha release** — functionality may be limited or under development.
- Thomson Prices are not included

---

*Originally developed by Dawid vd M, last update - 07/08/2025.*
"""
)
