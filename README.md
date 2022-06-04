# **Solution for data-processing (dkatalis_amaan)**

## 1. Instalation & run docker container (run python scripts solution.py)

a. Please install docker first before doing next step, this is step installation docker for ubuntu https://linuxhint.com/install_configure_docker_ubuntu/

b. Create folder for example, i create folder home with name docker-python using command **mkdir docker-python** 

d. Go to folder docker-python **cd docker-python**

e. Clone this github to that folder using command **git clone https://github.com/Ferdila-doank/dkatalis_amaan**

d. Go to folder dkatalis_amaan **cd dkatalis_amaan**

f. Build docker container (this container will be name as dkatalis_amaan) using command **docker build -t dkatalis_amaan .**

g. To run that docker using command **docker run dkatalis_amaan**

h. if you want see the coding solution use command **docker run -it dkatalis_solution /bin/bash**, and then goto solution folder and use command **nano solution.py** to see code 

## 2. Tasks
1. Visualize the complete historical table view of each tables in tabular format in stdout (hint: print your table)

  a. table account 
  
  this data originaly from source data (df_log)
  ![image](https://user-images.githubusercontent.com/55681442/171983234-30849666-ce26-4de0-99bc-d4c5f944d431.png)
  this data table contain last update data based on last json file processed (df).
  ![image](https://user-images.githubusercontent.com/55681442/171983415-7bfade6a-9dec-49af-aa4b-a4578b84bb59.png)
  
  b. table card 
  
  this data originaly from source data (df_log)
  ![image](https://user-images.githubusercontent.com/55681442/171986526-512b3370-806d-4a1e-8461-93a18ad22834.png)
  this data contain last update data based on last json file processed (df).
  ![image](https://user-images.githubusercontent.com/55681442/171986537-e875719d-9d9c-4724-9514-c80dfb8ef895.png)

  c. table savings accounts
  
  this data originaly from source data (df_log)
  ![image](https://user-images.githubusercontent.com/55681442/171986581-aa419cb6-1dfd-42a6-8604-570a66e59e69.png)
  this data contain last update data based on last json file processed (df).
  ![image](https://user-images.githubusercontent.com/55681442/171986598-6667f356-98ca-4584-80b9-7013987e6168.png)
  
2. Visualize the complete historical table view of the denormalized joined table in stdout by joining these three tables (hint: the join key lies in the `resources` section, please read carefully)

  this data join all data in card with account 
  ![image](https://user-images.githubusercontent.com/55681442/171990108-c26738c3-f482-4e91-881d-5b677f49fa3b.png)
  this data join all data in saving_account with account 
  ![image](https://user-images.githubusercontent.com/55681442/171990143-038de618-ec82-4191-b1c5-8661a1fe1b4a.png)

3. From result from point no 2, discuss how many transactions has been made, when did each of them occur, and how much the value of each transaction?  
   Transaction is defined as activity which change the balance of the savings account or credit used of the card
   
   a. transaction in card table join with account (credit used) have 3 transaction
   ![image](https://user-images.githubusercontent.com/55681442/171986685-7f1b71b7-371d-4e3c-bc80-41c94d52f343.png)
   
   b. transaction in saving account joint with account have 4 transaction (change balance)
   ![image](https://user-images.githubusercontent.com/55681442/171986733-98bf5b0b-c3e9-4dad-9fdd-e8745f5f98bd.png)

## 2. Logic solution.py

the logic of code solution.py is :
1. In init method will be declare path of data source (account, card and saving account) and declare column for each data 
2. Create method processing data. in this method will be process each data in folder source. Json file will be transform to data frame(with tabular format) and store in df_log variable. Also will create other dataframe contain update data based on .json file fo example in account first json create 1 row and then in second json update phone number to new value. so in df will store original data from json and in df_log will be contain last update data based on last json file processed json file. 

  this is sample df_log

  ![image](https://user-images.githubusercontent.com/55681442/171990306-afc366d8-38a0-4e1c-8ddb-89b4bad0bd20.png)

  ![image](https://user-images.githubusercontent.com/55681442/171990322-41bfafdf-d41c-4ded-8a2e-e14944aa8a14.png)

  this sample df

  ![image](https://user-images.githubusercontent.com/55681442/171990339-6f475e0a-a71c-46e1-a9fa-fcb7c8ff528d.png)

  ![image](https://user-images.githubusercontent.com/55681442/171990383-ad1f636b-f4f9-4619-affe-445ef3f41a32.png)

  In that picture show in index 0 create new data in df and df_log (create same data). But in index 1 because the json only update field phone_number, so in df_log contain only data phone_number but in df in index 1 get value from index 0 and update data phone_number 

3. Created method all_card_trans, this method is to join data df_acc with df_card with key is column card_id

  ![image](https://user-images.githubusercontent.com/55681442/171990769-8633066f-fce9-4433-b8f5-e8f5b70020a6.png)

4. Created method all_sv_trans, this method is to join data df_sv_acc with df_card with key is column savings_account_id

  ![image](https://user-images.githubusercontent.com/55681442/171990805-90b6e467-0a44-4b6f-b692-c193a8b1f0b8.png)

5. Created method card_trans, this method processing data in df_card only with credit value != 0 and join with df_acc with key card_id
  ![image](https://user-images.githubusercontent.com/55681442/171986685-7f1b71b7-371d-4e3c-bc80-41c94d52f343.png)

6. Create metho sav_trans, this method processing data in df_sv_acc with change saving balance and join with df_acc with key savings_account_id
   ![image](https://user-images.githubusercontent.com/55681442/171986733-98bf5b0b-c3e9-4dad-9fdd-e8745f5f98bd.png)
  

