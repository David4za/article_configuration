import re
import streamlit as st
import pandas as pd

config_file = r"C:\Users\dawid.vandermerwe\OneDrive - ERIKS\Dawid Test\Articles\Thomson\Article Configurator\Configurator.xlsx"

# create dfs
hd_df = pd.read_excel(config_file, sheet_name="HD Lin Acc", usecols="A:F")
xd_df = pd.read_excel(config_file, sheet_name="XD Lin Acc", usecols="A:F")

# Ensure both index and len are int
# hd
hd_df['Index'] = hd_df['Index'].astype(int)
hd_df['Len'] = hd_df['Len'].astype(int)
# xd
xd_df['Index'] = xd_df['Index'].astype(int)
xd_df['Len'] = xd_df['Len'].astype(int)

actuator_dfs = {
    "XD": xd_df,
    "HD": hd_df
}

def article_configuration(article_code: str, mapping_df: pd.DataFrame) -> dict:

    result = {}

    for _, row in mapping_df.iterrows():
        variable_name = row['Variable']
        start_index = row['Index'] - 1 # programming starts index at 0
        end_index = start_index + row['Len']
        code_snippet = article_code[start_index:end_index]

        match = mapping_df.loc[mapping_df['Code'] == code_snippet, 'Value']

        if not match.empty:
            result[variable_name] = [match.iloc[0], code_snippet]
        else:
            result[variable_name] = f"NA for {code_snippet}"

    return result

def article_description_one(artilce_data: dict) -> str:

    # convert to df for easier access to data
    df = pd.DataFrame.from_dict(artilce_data, orient='index').reset_index().rename(columns={'index':'Specification', 0:'Value', 1:"Code Snippet"})

    # Motor + Volt
    # get the value and then use index slicing and find to stop by ','
    lin_act = "Lin Act " + df['Value'][0][:df['Value'][0].find(',')]
    
    # Here I am finding the value and then indexing the string
    # in the same line. 

    # get string
    volt_value = df['Value'][0][
        # start from index of "," + 2
        df['Value'][0].find(',') +2 :
        # search the string until "d" then convert
        # to int by using len()
        len(df['Value'][0][:df['Value'][0].find('d')])
        # replace empty space
        ].replace(" ","")
    
    # .loc returns a pandas series, thus we must use
    # .value[0] in order to get the item at index 0
    comm = df.loc[df['Specification'] == 'Electrak Modular Control System options',
                  'Code Snippet'].values[0]
    
    lin_act = lin_act +" " + volt_value + " " + comm

    # kN pattern
    kn_pattern = r"\b\d+(?:\.\d+)?\s*kN\b"
    kn_value = re.search(kn_pattern,str(df['Value'][1])).group()

    #stroke length
    stroke_len = df['Value'][2]
    return lin_act + " " + kn_value.replace(" ","") + " " + stroke_len.replace(" ","")


# ------------------------------------ Streamlit Application ------------------------------------

st.set_page_config(page_title="Thomson Article Configurator")
st.title("Thomson Article Configurator")

# select from the different actuator dataframes
user_lin_act_selection = st.selectbox("Please select the type of actuator", actuator_dfs.keys())

# user inputs the article number
user_article_code = st.text_input("Article Code")

if user_article_code:
    specific_result = article_configuration(user_article_code, actuator_dfs[user_lin_act_selection])
    result_df = pd.DataFrame.from_dict(specific_result, orient='index').reset_index().rename(columns={'index':'Specification', 0:'Value', 1:"Code Snippet"})
    st.dataframe(result_df)

    description_one = article_description_one(specific_result)
    st.text_input("Description 1", value=description_one)
