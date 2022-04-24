import pandas as pd

#BSEG_BKPF --> main transactional data 
#TCURR --> exchange rate table

#extract TCURR and then merge it with BSEG_BKPF to get FX_RATE
def TCURR_extract_merge():
    global BSEG_BKPF, TCURR
    try:
        TCURR = pd.read_csv("TCURR.csv")
        TCURR = TCURR[['MANDT','KURST','FCURR','TCURR', 'UKURS','LAST_DTM']]
        TCURR= TCURR.rename(columns={
            'MANDT': 'CLIENT','KURST': 'FX_TYPE',
            'FCURR': 'FROM_CUR','TCURR': 'TO_CUR',
            'UKURS': 'FX_RATE','LAST_DTM': 'LAST_DATETIME'})
        TCURR["LAST_DATE"] = TCURR["LAST_DATETIME"].astype(str).str[:8]
        TCURR['LAST_DATE'] = pd.to_datetime(TCURR['LAST_DATE'], format ='%Y%m%d', errors = 'coerce')
        del TCURR["LAST_DATETIME"]
    except FileNotFoundError:
        print("TCURR Table not found.")
        TCURR = pd.DataFrame(columns=['CLIENT','FX_TYPE','FROM_CUR','TO_CUR', 'FX_RATE','LAST_DATE']) 
    #merging TCURR with BSEG_BKPF
    BSEG_BKPF = BSEG_BKPF.merge(TCURR[["FROM_CUR","FX_RATE","LAST_DATE"]], left_on=["DOC_CURRENCY","POSTING_DATE"],\
         right_on=["FROM_CUR","LAST_DATE"], how='left')
    BSEG_BKPF = BSEG_BKPF.drop(["FROM_CUR","LAST_DATE"], axis =1)

#run function
TCURR_extract_merge()


#in order to get highest materiality of accounting document we will get value with below condition
def Calculate_USD_Value(row):
    if row.LOCAL_CURRENCY == "USD":
        if row.AMOUNT_LOCAL_CUR_ABS != 0:
            return row.AMOUNT_LOCAL_CUR_ABS  #------1 leaf
        else:   #if row.AMOUNT_LOCAL_CUR_ABS == 0:
            if row.AMOUNT_GROUP_CUR_ABS !=0:
                return row.AMOUNT_GROUP_CUR_ABS  #------2 leaf
            else: #if row.AMOUNT_GROUP_CUR_ABS ==0:
                if row.AMOUNT_DOC_CUR_ABS !=0:
                    if row.DOC_CURRENCY=="USD":
                        return row.AMOUNT_DOC_CUR_ABS  #------3 leaf
                    else: #if row.DOC_CURRENCY!="USD":
                        return row.AMOUNT_DOC_CUR_ABS * row.FX_RATE #------4 leaf
                else: #if row.AMOUNT_DOC_CUR_ABS ==0:
                    return 0                       #------5 leaf
    
    else: #if row.LOCAL_CURRENCY != "USD":
        if row.AMOUNT_GROUP_CUR_ABS !=0:   
            return row.AMOUNT_GROUP_CUR_ABS #------6 leaf
        else: #if row.AMOUNT_GROUP_CUR_ABS ==0:
            if row.AMOUNT_DOC_CUR_ABS !=0:
                if row.DOC_CURRENCY=="USD":
                    return row.AMOUNT_DOC_CUR_ABS  #------9 leaf
                else: #if row.DOC_CURRENCY !="USD": 
                    return row.AMOUNT_DOC_CUR_ABS * row.FX_RATE  #------8 leaf
            else: #if row.AMOUNT_DOC_CUR_ABS ==0:
                return 0   #------7 leaf

BSEG_BKPF["CALCULATED_USD_ABS"] = BSEG_BKPF[["LOCAL_CURRENCY", "AMOUNT_LOCAL_CUR_ABS", "AMOUNT_GROUP_CUR_ABS",\
    "DOC_CURRENCY","AMOUNT_DOC_CUR_ABS","FX_RATE"]].apply(Calculate_USD_Value, axis=1)
