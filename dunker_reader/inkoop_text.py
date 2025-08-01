"""
Consider, a lot of the tools were made using Jupyter
due to the nature of the PDF was read, so at times
the code is more confusing than it should be.
"""
import re
import pandas as pd

from dunker_reader.constants import GEARBOX_OPTION, ENCODER_OPTIONS, BRAKE_OPTIONS, FW_OPTIONS

def gearbox_check(dfs=None):
    """
    Gearbox position is always at the same spot
    Thus, we can hard code the chceker
    """
    if dfs == None:
        raise ValueError("dfs must be provided")
    # ensure Col_1 exist and the df has enough variables
    if "Col_1" in dfs[0].columns and len(dfs[0]) > 1:
        index_1 = dfs[0]['Col_1'][1]

        # Check if the gearbox option is in index_1
        for item in GEARBOX_OPTION:
            if item in index_1.split(): # splits the index_1 into multiple pieces
                return True
    return False # if it does not exist 

def normalize_text(text):
    return text.replace(" ", "").lower()

def inkoop_text(dfs, sales_text_df):
    d = {
        "Keys":["Motor","Gearbox","Brake","Encoder","Cover","FW","Sachnumber"],
        "Details":[None]
        }
    d["Details"] = [None] * len(d["Keys"])
    inkoop_text_df = pd.DataFrame(data=d)
    
    # Motor
    
    """
    This part is spliting the motor text and looking if the 
    motor FW is there and then adds the space between e.g., dProIO
    """

    original_text = dfs[0].loc[0, "Col_1"]
    og_split = original_text.split()
    fw_part = og_split[-1]

    if fw_part[:-2] in FW_OPTIONS:
        updated_fw = fw_part[:-2] + " " + fw_part[-2:]
        original_text = original_text.replace(fw_part, updated_fw)
    else:
        original_text = original_text

    for df in dfs:
        for i in df.index:
            if df.loc[i, "Col_3"] == "nominalmotorvoltage":
                motor_voltage = df.loc[i, "Col_2"]
                motor_voltage = motor_voltage.replace(" ","")
                break
            else:
                motor_voltage = False
        if motor_voltage:
            break
  
    inkoop_text_df.loc[0,"Details"] = original_text + " " + motor_voltage
    

    # Gearbox
    if gearbox_check(dfs=dfs) == True:
        inkoop_text_df.loc[1,"Details"] = dfs[0].loc[1, "Col_1"]
    else:
        inkoop_text_df.loc[1,"Details"] = "NA"
    
    if gearbox_check(dfs=dfs) == True:
        gb_reducation = ""
        for df in dfs:
            """
            initially i was using enumerate but that is only for iterable items such as lists. 
            For items inside of a df one must use .iterrows()

            here i is still the index and then row is the content 
            within the cells i.e. index , Col_1 , Col_2
            """
            for i,row in df.iterrows():
                if row['Col_3'] == "reduction":
                    # here, my loc returns a df, thus I need to use iloc as it returns based on the index which in this new df will be 0
                    gb_reducation = row['Col_2']
                    gb_match = re.search(r'=(.*)', gb_reducation)
                    if gb_match:
                        gb_reducation = gb_match.group(1).strip()
                        break
        
        inkoop_text_df.loc[1, "Details"] = f'{inkoop_text_df.loc[1, "Details"]} ({gb_reducation})'

    raw_attachment_list = []
    attachment_list = []

    if gearbox_check(dfs=dfs) == True and len(dfs[0]["Col_1"]) > 1:
        # Use range function more often, it is powerful
        for i in range(2, len(dfs[0]["Col_1"])):
            raw_attachment_list.append(dfs[0]['Col_1'][i])

    elif gearbox_check(dfs=dfs) == False and len(dfs[0]["Col_1"]) > 1:
        for i in range(1, len(dfs[0]["Col_1"])):
            raw_attachment_list.append(dfs[0]['Col_1'][i])
            
    for i in raw_attachment_list:
        item = i.split('+')
        # use extend instead of append. Append creates a [] within the initial [] but extend just well... extends
        attachment_list.extend(item)

    brake_found = False
    encoder_found = False

    for i,j in enumerate(attachment_list):
        if j.replace(" ","") in BRAKE_OPTIONS:
            inkoop_text_df.loc[2,"Details"] = attachment_list[i].replace(" ","")
            brake_found = True
            continue
        elif j[:2] in ENCODER_OPTIONS:
            inkoop_text_df.loc[3,"Details"] = attachment_list[i]
            encoder_found = True
            break

    if not brake_found:
        inkoop_text_df.loc[2,"Details"] = 'NA'

    if not encoder_found:
        inkoop_text_df.loc[3,"Details"] = 'NA'
          
    # Brake text 

    if brake_found:
        for df in dfs:
            if df.loc[0,"Col_1"] == "Attachment":
                for i,j in enumerate(df['Col_1']):
                    if df.loc[i,"Col_2"] == "Poweroffbrake":
                        brake_type = 'R'
                        break
                    elif df.loc[i,"Col_2"] == "Poweronbrake":
                        brake_type = 'A'
                        break
                    else:
                        brake_type = 'NA'

                    """
                    This was a later somewhat makeshift fix
                    """               
                    if brake_type != "NA":
                        brake_voltage = normalize_text(dfs[-1].loc[dfs[-1]['Col_1'] == "Brakevoltage", 'Col_2'].values[0].strip())
                        brake_voltage = " "+brake_voltage[:2]+"V"
                        inkoop_text_df.loc[inkoop_text_df['Keys'] == 'Brake', 'Details'] = inkoop_text_df.loc[inkoop_text_df['Keys'] == 'Brake', 'Details'] + brake_type + brake_voltage
                    else:
                        inkoop_text_df.loc[inkoop_text_df['Keys'] == 'Brake', 'Details'] = inkoop_text_df.loc[inkoop_text_df['Keys'] == 'Brake', 'Details'] + brake_type

        # cover details
    cover_status = False
    for df in dfs:
        for i, row in df.iterrows():
                if row["Col_3"] == "protectioncover":
                    cover_status = row["Col_2"]
                    break
                else:
                    cover_status = False
    
    for df in dfs:
        for i, row in df.iterrows():
            if row["Col_3"] == "protectionclass":
                protection_class = row["Col_2"]
                break
            else:
                protection_class = "NA"
        
    if not cover_status:
        inkoop_text_df.loc[4,"Details"] = "NA"
    elif  cover_status == "Yes":
        inkoop_text_df.loc[4,"Details"] = protection_class
    else:
        inkoop_text_df.loc[4,"Details"] = "NA"

    # encoder details

    encoder_channel = False
    for df in dfs:
        if df.loc[0, "Col_1"] == "Attachment":
            for i,j in enumerate(df["Col_1"]):
                if df.loc[i,"Col_1"] == "EncoderChannels":
                    encoder_channel = df.loc[i, "Col_2"]
                    break
                else:
                    encoder_channel = False


    for df in dfs:
        if df.loc[0, "Col_1"] == "Attachment":
            for i,j in enumerate(df["Col_1"]):
                if df.loc[i,"Col_1"] == "EncoderResolution":
                    encoder_resolution = df.loc[i, "Col_2"]
                    e_stop_sign = encoder_resolution.find('p')
                    encoder_resolution = encoder_resolution[:e_stop_sign-1]
                    break
                else:
                    encoder_resolution = False

    for df in dfs:
        if df.loc[0, "Col_1"] == "Attachment":
            for i,j in enumerate(df["Col_1"]):
                if df.loc[i,"Col_1"] == "EncodersupplyVoltage":
                    encoder_volt = df.loc[i, "Col_2"]+"V"
                    break
                else:
                    encoder_volt = False

    encoder_text_p1 = ""
    encoder_text_p2 = ""


    if encoder_channel:
        encoder_text = str(inkoop_text_df.loc[3, "Details"])

        # using re, match the data pattern 
        pattern =  re.match(r"(\D*)(\d+)(\D*)", encoder_text)

        if pattern:
            encoder_text_p1 = pattern.group(1) + pattern.group(2)
            encoder_text_p2 = pattern.group(3)
            
        else:
            encoder_text_p1 = encoder_text

    if not encoder_channel:
        inkoop_text_df.loc[3, "Details"] = "NA"
    elif not str(encoder_text_p2) == "":
        inkoop_text_df.loc[3, "Details"] = encoder_text_p1 + f'-{encoder_channel}-{encoder_resolution.strip()}{encoder_text_p2} {encoder_volt}'
    else:
        inkoop_text_df.loc[3, "Details"] = encoder_text_p1 + f'-{encoder_channel}-{encoder_resolution.strip()} {encoder_volt}'

    inkoop_text_df.loc[0, "Details"] = re.sub(r'(\d+)\sX\s(\d+)', r'\1X\2', inkoop_text_df.loc[0, "Details"])

    # FW

    if dfs[0].iloc[-1]["Col_1"] != "FW":
        inkoop_text_df.loc[5, "Details"] = "NA"
    else:
        inkoop_text_df.loc[5, "Details"] = sales_text_df.loc[3, "Value"]
            
    # Sachnumbers

    sachnumbers = dfs[0]["Col_2"].tolist()
    sach_string = ", ".join(str(x) for x in sachnumbers)
    inkoop_text_df.loc[6, "Details"] = sach_string

    return inkoop_text_df