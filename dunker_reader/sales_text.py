import pandas as pd

from dunker_reader.inkoop_text import normalize_text, gearbox_check
from dunker_reader.constants import FW_OPTIONS

def sales_text(dfs):
    d = {
        "Specification":["Nominal Speed", "Nominal Torque", "Maximum Torque", "Version", 'Output Shaft Diameter',"Output Shaft Length"],
        "Value":[]
        }
    d["Value"] = [None] * len(d["Specification"])
    sales_text_df = pd.DataFrame(data=d)

    # normalize text to combat the pdf plumber changes
    sales_text_df["norm_spec"] = sales_text_df['Specification'].apply(normalize_text)

    for df in dfs:
        df['Col_3'] = df['Col_1'].apply(normalize_text)

    # d[0:2]
    first_three_index = [sales_text_df.loc[0, "norm_spec"],
                         sales_text_df.loc[1, "norm_spec"],
                         sales_text_df.loc[2, "norm_spec"]]

    for i, spec in enumerate(first_three_index):
        if not i == 2:
            matching_index = (dfs[1]["Col_3"] == spec).idxmax()
            sales_text_df.loc[i, "Value"] = dfs[1].loc[matching_index,"Col_2"]
        # some motors have the text "Maximum torque limted by gearbox" so for these I need to build a special structure
        elif i == 2:
            # Here I use Panda's .str function, that essentially loops through items inside the series for me and allows me to preform string operators i.e. slicing and lower()
            matching_index = (dfs[1]["Col_1"].str[:len("MaximumTorque")].str.lower() == spec.lower()).idxmax()
            sales_text_df.loc[i, "Value"] = dfs[1].loc[matching_index,"Col_2"]


    # Version index 3, will always be in dfs[-1]
    version_index = (dfs[-1]["Col_3"] == sales_text_df.loc[3, "norm_spec"]).idxmax()
    if version_index == 1:
        original_text = dfs[-1].loc[version_index, "Col_2"]
        og_split = original_text.split()
        fw_part = og_split[-1]
        if fw_part[:-2] in FW_OPTIONS:
            updated_fw = fw_part[:-2] + " " + fw_part[-2:]
            original_text = original_text.replace(fw_part, updated_fw)
            sales_text_df.loc[3, "Value"] = original_text
        else:
            original_text = original_text
            sales_text_df.loc[3, "Value"] = original_text
    else:
        sales_text_df.loc[3, "Value"] = 'NA'    

    if gearbox_check(dfs) == True:
        # index 4 & 5
        for i in range(4 ,6):
            gb_spec = sales_text_df.loc[i, "norm_spec"]
            for df in dfs:
                for j, row in df.iterrows():
                    if df.loc[j, "Col_3"] == sales_text_df.loc[i, "norm_spec"]: 
                        if gb_spec in df["Col_3"].values:
                            #gb_index = (df["Col_3"] == gb_spec).idxmax()
                            sales_text_df.loc[i, "Value"] = row['Col_2']
    elif not gearbox_check(dfs):
        for i in range(4,6):
            sales_text_df.loc[i, "Value"] = 'NA'

    sales_text_df.drop('norm_spec', axis=1, inplace=True)    
    return sales_text_df