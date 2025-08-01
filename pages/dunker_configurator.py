import datetime
import streamlit as st
import pandas as pd

from io import BytesIO

from dunker_reader.pdf_reader_plumber import pdf_reader_plumber
from dunker_reader.inkoop_text import inkoop_text
from dunker_reader.sales_text import sales_text
from dunker_reader.descriptions import description_1, description_2
st.title("📄 Dunker PDF Reader")

uploaded_file = st.file_uploader("Upload your pdf")

current_time = datetime.datetime.now().strftime("%Y-%m-%d")

if uploaded_file:
    st.markdown(
        """
        <p style="color: green; font-size: 18px; font-weight: bold;">
        ✅ PDF uploaded successfully!
        </p>
        """,
        unsafe_allow_html=True,
    )
    try:

        dfs = pdf_reader_plumber(uploaded_file)

        sales_text_df = sales_text(dfs)
        st.subheader("Sales Text")
        with st.expander("Sales DateFrame (Editable)"):
            edited_sales_text_df = st.data_editor(sales_text_df, use_container_width=True)
        edited_sales_text = "\n".join(f"{row['Specification']}: {row['Value']}" for i, row in edited_sales_text_df.iterrows())

        st.subheader("Sales Text")
        st.text(edited_sales_text)

        inkoop_text_df = inkoop_text(dfs,sales_text_df)
        st.subheader("Purchase Text")
        with st.expander("Inkoop DateFrame (Editable)"):
            edited_inkoop_text_df = st.data_editor(inkoop_text_df, use_container_width=True)
        edited_inkoop_text = "\n".join(f"{row['Keys']}: {row['Details']}" for i, row in edited_inkoop_text_df.iterrows())

        st.subheader("Inkoop Text")
        st.text(edited_inkoop_text)

        description_one = description_1(inkoop_text_df, dfs)
        description_two = description_2(inkoop_text_df)

        st.subheader("Descriptions")
        st.text_input("Description 1", description_one)
        st.text_input("Description 2", description_two)

        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            edited_sales_text_df.to_excel(writer, index=False, sheet_name="Sales Text")
            edited_inkoop_text_df.to_excel(writer, index=False, sheet_name="Inkoop Text")
        output.seek(0)

        st.download_button(
            label="Download Data to Excel",
            data=output,
            file_name=f"{current_time} Article Description  {description_one[:5]}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.markdown("Made by Dave")
    except Exception as e:
        st.error(f"An error occured while processing file {e}")

else:
    st.info("Please upload the PDF file") 