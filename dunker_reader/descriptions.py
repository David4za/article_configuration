from dunker_reader.inkoop_text import gearbox_check

def description_1(inkoop_text_df, dfs):
    if gearbox_check(dfs):
        return f"{inkoop_text_df.loc[0, 'Details']} + {inkoop_text_df.loc[1, 'Details']}"
    else:
        return f"{inkoop_text_df.loc[0, 'Details']}"

def description_2(inkoop_text_df):
    description_parts = []
    for i in range(2, 5):
        detail = inkoop_text_df.loc[i, "Details"]
        if detail != "NA":
            description_parts.append(detail) 
    
    return ' + '.join(description_parts)