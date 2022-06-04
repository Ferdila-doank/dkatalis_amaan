import os
from timeit import repeat
import pandas as pd
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")
pd.options.display.max_columns = None
pd.options.display.max_rows = None

class solution:

    def __init__(self):

        #setup path source data (accounts, cards, savings_accounts)
        self.path_acc = "/usr/app/src/data/accounts"
        self.path_card = "/usr/app/src/data/cards"
        self.path_saving_account = "/usr/app/src/data/savings_accounts"
        
        #setup field for log_accounts, log_cards, log_savings_account
        self.list_column_acc = ['log_id','ts','op','account_id','address','email','name','phone_number','savings_account_id','card_id']    
        self.list_column_card = ['log_id','ts','op','card_id','card_number','credit_used','monthly_limit','status']
        self.list_column_sv_acc = ['log_id','ts','op','savings_account_id','balance','interest_rate_percent','status']

    def processing_data(self,data):
        
        #setup variable path & column based on parameter (account/card/saving_account) for log dataframe
        if data == "account":
            path_source = self.path_acc
            list_column = self.list_column_acc
        elif data == "card":
            path_source = self.path_card
            list_column = self.list_column_card
        elif data == "saving_account":
            path_source = self.path_saving_account
            list_column = self.list_column_sv_acc

        #setup variable column for dataframe
        list_column_table = list_column
        
        # initialize empty df_log & df 
        df_log = pd.DataFrame(columns = list_column)
        df = pd.DataFrame(columns = list_column_table)

        # listing file based on path
        list_file = os.listdir(path_source)
        list_file.sort()

        # processing file in folder one by one
        for i in list_file:

            #read json data source 
            df_temp_acc = pd.read_json(path_source + "/" + i)  

            #extract data for json with op == "c" 
            if (df_temp_acc['op'].unique()[0]) == "c":

                dict_log = {}
                dict_empty = dict.fromkeys(list_column)

                #make dictionary to extract value based on column (for df_log)
                for j in list_column:
                    
                    for row in df_temp_acc.index:
                        if row == j:
                            dict_temp = {j : df_temp_acc['data'][row]}
                            dict_log.update(dict_temp) 
                    
                    dict_temp = {"log_id" : df_temp_acc['id'].unique()[0],"ts": datetime.fromtimestamp(int(df_temp_acc['ts'].unique()[0])/1000), "op" : "c"}
                    dict_log.update(dict_temp)
                
                for j in dict_empty:
                    if j in dict_log:
                        pass
                    else:
                        dict_temp = {j : ""}
                        dict_log.update(dict_temp)

                df_log = df_log.append(dict_log,ignore_index=True)

                #copy value from df_log to df 
                dict_table = dict_log

                df = df.append(dict_table,ignore_index=True)

            #extract data for json with op == "u" 
            if (df_temp_acc['op'].unique()[0]) == "u":

                df.loc[len(df)] = df.iloc[len(df)-1,:]

                #make dictionary to extract value based on column (for df_log)    
                dict_log = {}
                dict_empty = dict.fromkeys(list_column)

                #update df based on value of dict_temp
                for j in list_column:
                    
                    for row in df_temp_acc.index:
                        if row == j:
                            dict_temp = {j : df_temp_acc['set'][row]}
                            dict_log.update(dict_temp) 
                            
                            df.loc[len(df)-1,row] = df_temp_acc['set'][row]
                    
                    df.loc[len(df)-1,'op'] = df_temp_acc['op'].unique()[0]
                    df.loc[len(df)-1,'ts'] = datetime.fromtimestamp(int(df_temp_acc['ts'].unique()[0])/1000)


                for j in dict_empty:
                    if j in dict_log:
                        pass
                    else:
                        dict_temp = {j : ""}
                        dict_log.update(dict_temp)

                dict_temp = {"log_id" : df_temp_acc['id'].unique()[0],"ts": datetime.fromtimestamp(int(df_temp_acc['ts'].unique()[0])/1000), "op" : "u"}
                dict_log.update(dict_temp)
                
                #create data for df_log
                df_log = df_log.append(dict_log,ignore_index=True)
                
        return (df,df_log)

    def all_card_trans(self,df_acc,df_card):
        card_id = df_card["card_id"].unique()
        
        df_temp_acc = df_acc.loc[df_acc['card_id'].isin(card_id)][["account_id","address","email","name", "phone_number","card_id"]]  
        df_all_card_trans = pd.merge(df_card,df_temp_acc,on="card_id")

        return(df_all_card_trans)        

    def all_sv_trans(self,df_acc,df_sv_acc):
        sv_acc_id = df_sv_acc["savings_account_id"].unique()
        df_temp_sv_acc = df_acc.loc[df_acc['savings_account_id'].isin(sv_acc_id)][["account_id","address","email","name", "phone_number","savings_account_id"]] 

        df_temp_sv_acc2 = pd.DataFrame(columns=["account_id","address","email","name", "phone_number","savings_account_id"])
        df_temp_sv_acc2.loc[0] = df_temp_sv_acc.loc[len(df_temp_sv_acc)-1]

        df_all_card_trans = pd.merge(df_sv_acc,df_temp_sv_acc2,on="savings_account_id")

        return(df_all_card_trans) 

    def card_trans(self,df_acc,df_card):

        df_temp_card = df_card.loc[df_card["credit_used"] != 0]
        #df_temp_card = df_card[(df_card["status"] == "ACTIVE") & (df_card["op"] == "u")]

        card_id = df_temp_card["card_id"].unique()
        df_temp_acc = df_acc.loc[df_acc['card_id'].isin(card_id)][["account_id","address","email","name", "phone_number","savings_account_id","card_id"]]     

        df_card_trans = pd.merge(df_temp_card,df_temp_acc,on="card_id")
        
        return df_card_trans

    def sav_trans(self,df_acc,df_sav_acc):

        list_column = df_sav_acc.columns.values.tolist() 
        df_temp_sav_acc = pd.DataFrame(columns = list_column)

        list_balance = df_sav_acc.loc[df_sav_acc["balance"] != 0][["balance"]]
        list_balance = list_balance['balance'].unique()
        
        for i in list_balance:
            temp_balance = df_sav_acc.loc[df_sav_acc["balance"] == i]
            df_temp_sav_acc = df_temp_sav_acc.append(temp_balance.iloc[0,:])

        sav_id = df_sav_acc["savings_account_id"].unique()
        df_temp_acc = df_acc.loc[df_acc['savings_account_id'].isin(sav_id)][["account_id","address","email","name", "phone_number","savings_account_id"]] 

        df_temp_acc2 = pd.DataFrame(columns=["account_id","address","email","name", "phone_number","savings_account_id"])
        df_temp_acc2.loc[0] = df_temp_acc.loc[len(df_temp_acc)-1]

        df_sav_acc_trans = pd.merge(df_temp_sav_acc,df_temp_acc2,on="savings_account_id")
        
        return df_sav_acc_trans

 if __name__ == '__main__':

    #create object bank from class solution
    bank = solution()

    #run method bank.processing data fro processing data account 
    df_acc,df_log_acc = bank.processing_data("account")

    #print df_log_acc get from processing file source account
    print("\n Original data from file source account (tabular format)")
    print(df_log_acc)

    #print df_acc get from processing file source & update base on value 
    print("\n Update data based on file source account (tabular format)")
    print(df_acc)

    #run method bank.processing data fro processing data card 
    df_card,df_log_card = bank.processing_data("card")

    #print df_log_acc get from processing file source card
    print("\n Original data from file source card (tabular format)")
    print(df_log_card)    

    #print df_acc get from processing file source & update base on value
    print("\n Update data based on file source card (tabular format)")
    print(df_card)

    #run method bank.processing data fro processing data saving_account 
    df_sv_acc,df_log_sv_acc = bank.processing_data("saving_account")

    #print df_log_acc get from processing file source saving account
    print("\n Original data from file source saving account (tabular format)")
    print(df_log_sv_acc)    

    #print df_acc get from processing file source & update base on value
    print("\n Update data based on file source card (tabular format)")    
    print(df_sv_acc)

    #run method bank.all_card_trans (all data card join with account)
    df_all_card_trans = bank.all_card_trans(df_acc,df_card)

    #print df_all_card_trans (all data card join with account)
    print("\n all data card join with account")
    print(df_all_card_trans)

    #run method bank.all_sv_trans (all data saving account join with account)
    df_all_sv_acc = bank.all_sv_trans(df_acc,df_sv_acc)

    #print df_all_card_trans (all data card join with account)
    print("\n all data saving account join with account")   
    print(df_all_sv_acc)

    #processing card transaction (credit value != 0) using method bank.card_trans 
    df_card_trans = bank.card_trans(df_acc,df_card)

    #print card transaction (credit value != 0)
    print ("\n Card transaction (credit value != 0)")
    print(df_card_trans)

    #processing savings accounts transaction (change balance) using method bank.sav_trans 
    df_sav_acc = bank.sav_trans(df_acc,df_sv_acc)

    print("\n Savings accounts transaction (change balance)")
    print(df_sav_acc)
