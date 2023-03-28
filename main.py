import streamlit as st
#st.title("Welcome to PhonePe Pulse Dashboard")

import pandas as pd
import json
import os
import numpy as np

import matplotlib.pyplot as plt

import plotly.express as px
import requests
from PIL import Image
import sqlite3


agg_transaction = pd.read_csv("C:/Users/Admin/Downloads/Aggregated Transaction.csv")
agg_user = pd.read_csv("C:/Users/Admin/Downloads/Aggregated User.csv")
map_transaction = pd.read_csv("C:/Users/Admin/Downloads/Map Transaction.csv")
map_user = pd.read_csv("C:/Users/Admin/Downloads/Map User.csv")
top_transaction=pd.read_csv("C:/Users/Admin/Downloads/Top Transaction.csv")
top_user=pd.read_csv("C:/Users/Admin/Downloads/Top User.csv")

connection = sqlite3.connect("phone_pe_pulse.db")
cursor = connection.cursor()
agg_transaction.to_sql('aggregated_transaction', connection, if_exists='replace')
agg_user.to_sql('aggregated_user', connection, if_exists='replace')
c = map_transaction.to_sql('map_transaction', connection, if_exists='replace')
map_user.to_sql('map_user', connection, if_exists='replace')
top_transaction.to_sql('top_transaction', connection, if_exists='replace')
top_user.to_sql('top_user', connection, if_exists='replace')

#df = pd.read_sql_query("SELECT * from aggregated_transaction", connection)
selected = st.sidebar.selectbox(
    "Select an option", ["Home 🏠", "Basic insights 👀","Search 🔍","About Phonepe👈",]
)


if selected == "Home 🏠":
    #col1,col2 = st.columns(2)
    #with col1:
    st.image(Image.open("C:/Users/Admin/Downloads/phonepehome.png"), width=450)
    st.write("PhonePe  is an Indian digital payments and financial technology in Bengaluru, Karnataka, India. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016.")
        #st.subheader("DOWNLOAD THE APP NOW: https://www.phonepe.com/app-download/")

    #with col1:
    st.video("C:/Users/Admin/Downloads/pulse-video.mp4")
    st.subheader("DOWNLOAD THE APP NOW: https://www.phonepe.com/app-download/")


if selected == "Basic insights 👀":
    st.title("BASIC INSIGHTS")
    st.write("----")
    st.subheader("Let's know some basic insights about the data")
    options = ["--select--",
               "Top 10 states based on year and amount of transaction",
               "Least 10 states based on type and amount of transaction",
               "Top 10 mobile brands based on percentage of transaction",
               "Top 10 Registered-users based on States and District(pincode)",
               "Top 10 Districts based on states and amount of transaction",
               "Least 10 Districts based on states and amount of transaction",
               "Least 10 registered-users based on Districts and states",
               "Top 10 transactions_type based on states and transaction_amount"]
    select = st.selectbox("Select the option",options)



    if select == "Top 10 states based on year and amount of transaction":
        cursor.execute("SELECT DISTINCT State,Transaction_amount,Year,Quarter FROM top_transaction GROUP BY State ORDER BY transaction_amount DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['State','Transaction_amount','Year','Quarter'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.subheader("Top 10 states based on type and amount of transaction")
            st.bar_chart(data=df,x="State",y="Transaction_amount")



    elif select == "Least 10 states based on type and amount of transaction":
        cursor.execute("SELECT DISTINCT State,Transaction_amount,Year,Quarter FROM top_transaction GROUP BY State ORDER BY transaction_amount ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transaction_amount', 'Year', 'Quarter'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.subheader("Least 10 states based on type and amount of transaction")
            st.bar_chart(data=df, x="State", y="Transaction_amount")



    elif select == "Top 10 mobile brands based on percentage of transaction":
        cursor.execute(
            "SELECT DISTINCT brands,Percentage FROM aggregated_user GROUP BY brands ORDER BY Percentage DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(), columns=['brands', 'Percentage'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.subheader("Top 10 mobile brands based on percentage of transaction")
            st.bar_chart(data=df, x="brands", y="Percentage")



    elif select == "Top 10 Registered-users based on States and District(pincode)":
        cursor.execute(
            "SELECT DISTINCT State,District,RegisteredUser FROM top_user GROUP BY State,District ORDER BY RegisteredUser DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'District', 'RegisteredUser'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.subheader("Top 10 Registered-users based on States and District(pincode)")
            st.bar_chart(data=df, x="State", y="RegisteredUser")




    elif select == "Top 10 Districts based on states and amount of transaction":
        cursor.execute(
            "SELECT DISTINCT State,District,amount FROM map_transaction GROUP BY State,District ORDER BY amount DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'District', 'Transaction_amount'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.subheader("Top 10 Districts based on states and amount of transaction")
            st.bar_chart(data=df, x="State", y="Transaction_amount")



    elif select == "Least 10 Districts based on states and amount of transaction":
        cursor.execute(
            "SELECT DISTINCT State,District,amount FROM map_transaction GROUP BY State,District ORDER BY amount ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'District', 'Transaction_amount'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.subheader("Least 10 Districts based on states and amount of transaction")
            st.bar_chart(data=df, x="State", y="Transaction_amount")


    elif select == "Least 10 registered-users based on Districts and states":
        cursor.execute(
            "SELECT DISTINCT State,District,RegisteredUser FROM top_user GROUP BY State,District ORDER BY RegisteredUser ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'District', 'RegisteredUser'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.subheader("Least 10 registered-users based on Districts and states")
            st.bar_chart(data=df, x="State", y="RegisteredUser")


    elif select == "Top 10 transactions_type based on states and transaction_amount":
        cursor.execute(
            "SELECT DISTINCT State,Transaction_type,Transaction_amount FROM aggregated_transaction GROUP BY State,Transaction_type ORDER BY Transaction_amount DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transaction_type', 'Transaction_amount'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.subheader("Top 10 transactions_type based on states and transaction_amount")
            st.bar_chart(data=df, x="State", y="Transaction_amount")



if selected == "Search 🔍":
    Topic = ["","Transaction-Type", "Brand", "Top-Transactions"]
    choice_topic = st.selectbox("Search by", Topic)

# function for transaction type
    def type_(type):
        cursor.execute(
            f"SELECT DISTINCT State,Quarter,Year,Transaction_type,Transaction_amount FROM aggregated_transaction WHERE Transaction_type = '{type}' ORDER BY State,Quarter,Year");
        df = pd.DataFrame(cursor.fetchall(),
                          columns=['State', 'Quarter', 'Year', 'Transaction_type', 'Transaction_amount'])
        return df


    def type_year(year, type):
        cursor.execute(
            f"SELECT DISTINCT State,Year,Quarter,Transaction_type,Transaction_amount FROM aggregated_transaction WHERE Year = '{year}' AND Transaction_type = '{type}' ORDER BY State,Quarter,Year");
        df = pd.DataFrame(cursor.fetchall(),
                          columns=['State', 'Year', "Quarter", 'Transaction_type', 'Transaction_amount'])
        return df


    def type_state(state, year, type):
        cursor.execute(
            f"SELECT DISTINCT State,Year,Quarter,Transaction_type,Transaction_amount FROM aggregated_transaction WHERE State = '{state}' AND Transaction_type = '{type}' And Year = '{year}' ORDER BY State,Quarter,Year");
        df = pd.DataFrame(cursor.fetchall(),
                          columns=['State', 'Year', "Quarter", 'Transaction_type', 'Transaction_amount'])
        return df



    if choice_topic=="Transaction-Type":
        col1,col2,col3 = st.columns(3)
        with col1:
            st.subheader(" -- TYPE -- ")
            transaction_type = st.selectbox("", ["Type", "Financial Services",
                                                          "Merchant payments", "Peer-to-peer payments",
                                                          "Recharge & bill payments", "Others"], 0)
        with col2:
            st.subheader("--YEAR--")
            choice_year = st.selectbox("", ["", "2018", "2019", "2020", "2021", "2022"], 0)
        with col3:
            st.subheader(" --STATE-- ")
            menu_state = ['', 'andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                          'assam', 'bihar', 'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu',
                          'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                          'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh', 'maharashtra', 'manipur',
                          'meghalaya', 'mizoram', 'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                          'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal']
            choice_state = st.selectbox("", menu_state, 0)

        if transaction_type:
            col1,col2,col3, = st.columns(3)
            with col1:
                st.subheader(f'{transaction_type}')
                st.write(type_(transaction_type))
        if transaction_type and choice_year:
            with col2:
                st.subheader(f' in {choice_year}')
                st.write(type_year(choice_year,transaction_type))
        if transaction_type and choice_state and choice_year:
            with col3:
                st.subheader(f' in {choice_state}')
                st.write(type_state(choice_state,choice_year,transaction_type))



# functions for Brand
    def brand_(brand_type):
        cursor.execute(
            f"SELECT State,Year,Quarter,brands,Percentage FROM aggregated_user WHERE brands='{brand_type}' ORDER BY State,Year,Quarter,brands,Percentage DESC");
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Year', "Quarter", 'brands', 'Percentage'])
        return df


    def brand_year(brand_type, year):
        cursor.execute(
            f"SELECT State,Year,Quarter,brands,Percentage FROM aggregated_user WHERE Year = '{year}' AND brands='{brand_type}' ORDER BY State,Year,Quarter,brands,Percentage DESC");
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Year', "Quarter", 'brands', 'Percentage'])
        return df


    def brand_state(state, brand_type, year):
        cursor.execute(
            f"SELECT State,Year,Quarter,brands,Percentage FROM aggregated_user WHERE State = '{state}' AND brands='{brand_type}' AND Year = '{year}' ORDER BY State,Year,Quarter,brands,Percentage DESC");
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Year', "Quarter", 'brands', 'Percentage'])
        return df

    if choice_topic == "Brand":
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("-- BRANDS--")
            mobiles = ["", 'Xiaomi', 'Vivo', 'Samsung', 'Oppo', 'Realme', 'Apple', 'Huawei', 'Motorola', 'Tecno',
                       'Infinix',
                       'Lenovo', 'Lava', 'OnePlus', 'Micromax', 'Asus', 'Gionee', 'HMD Global', 'COOLPAD', 'Lyf',
                       'Others']
            brand_type = st.selectbox("search by", mobiles, 0)

        with col2:
            st.subheader("-- 5 YEARS --")
            choice_year = st.selectbox("Year", ["", "2018", "2019", "2020", "2021", "2022"], 0)

        with col3:
            st.subheader("-- 36 STATES --")
            menu_state = ["", 'uttar-pradesh', 'jharkhand', 'puducherry', 'rajasthan', 'odisha', 'nagaland',
                          'chandigarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'assam', 'haryana', 'jammu-&-kashmir',
                          'tamil-nadu', 'himachal-pradesh', 'ladakh', 'bihar', 'maharashtra', 'uttarakhand',
                          'karnataka', 'lakshadweep', 'andhra-pradesh', 'sikkim', 'madhya-pradesh', 'mizoram',
                          'kerala', 'manipur', 'arunachal-pradesh', 'andaman-&-nicobar-islands', 'delhi', 'tripura',
                          'chhattisgarh', 'meghalaya', 'goa', 'west-bengal', 'telangana', 'gujarat', 'punjab']
            choice_state = st.selectbox("", menu_state, 0)

        if brand_type:
            col1, col2, col3, = st.columns([2,2,2],gap="small")
            #st.markdown("## :violet[BRAND]")
            with col1:
                st.subheader(f'{brand_type}')
                st.write(brand_(brand_type))
        if brand_type and choice_year:
            with col2:
                st.subheader(f' in {choice_year}')
                st.write(brand_year(brand_type, choice_year))
        if brand_type and choice_state and choice_year:
            with col3:
                st.subheader(f' in {choice_state}')
                st.write(brand_state(choice_state, brand_type, choice_year))



# function for toptransactions
    def transaction_state(_state):
        cursor.execute(
            f"SELECT State,Year,Quarter,District,Transaction_count,Transaction_amount FROM top_transaction WHERE State = '{_state}' GROUP BY State,Year,Quarter")
        df = pd.DataFrame(cursor.fetchall(),
                          columns=['State', 'Year', "Quarter", 'District', 'Transaction_count', 'Transaction_amount'])
        return df


    def transaction_year(_state, _year):
        cursor.execute(
            f"SELECT State,Year,Quarter,District,Transaction_count,Transaction_amount FROM top_transaction WHERE Year = '{_year}' AND State = '{_state}' GROUP BY State,Year,Quarter")
        df = pd.DataFrame(cursor.fetchall(),
                          columns=['State', 'Year', "Quarter", 'District', 'Transaction_count', 'Transaction_amount'])
        return df


    def transaction_quarter(_state, _year, _quarter):
        cursor.execute(
            f"SELECT State,Year,Quarter,District,Transaction_count,Transaction_amount FROM top_transaction WHERE Year = '{_year}' AND Quarter = '{_quarter}' AND State = '{_state}' GROUP BY State,Year,Quarter")
        df = pd.DataFrame(cursor.fetchall(),
                          columns=['State', 'Year', "Quarter", 'District', 'Transaction_count', 'Transaction_amount'])
        return df


    if choice_topic == "Top-Transactions":
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader(" SELECT STATE ")
            menu_state = ['', 'andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                          'assam', 'bihar', 'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu',
                          'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                          'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh', 'maharashtra', 'manipur',
                          'meghalaya', 'mizoram', 'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                          'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal']
            choice_state = st.selectbox("State", menu_state, 0)
        with col2:
            st.subheader(" SELECT YEAR ")
            choice_year = st.selectbox("Year", ["", "2018", "2019", "2020", "2021", "2022"], 0)
        with col3:
            st.subheader(" SELECT Quarter ")
            menu_quarter = ["", "1", "2", "3", "4"]
            choice_quarter = st.selectbox("Quarter", menu_quarter, 0)

        if choice_state:
            with col1:
                st.subheader(f'{choice_state}')
                st.write(transaction_state(choice_state))
        if choice_state and choice_year:
            with col2:
                st.subheader(f'{choice_year}')
                st.write(transaction_year(choice_state, choice_year))
        if choice_state and choice_quarter:
            with col3:
                st.subheader(f'{choice_quarter}')
                st.write(transaction_quarter(choice_state, choice_year, choice_quarter))

if selected == "About Phonepe👈":
    st.image(Image.open("C:/Users/Admin/Downloads/PhonePe-Pulse33.jpg"))
    st.subheader("Founded     :  2015")
    st.subheader("Headquarters:  Bengaluru, Karnataka, India")
    st.subheader("Founders    :  Sameer Nigam , Rahul Chari, Burzin Engineer ")
    st.subheader("Parent      :  Walmart")
    st.subheader("Subsidiaries:  Solvy Tech Solutions Pvt Ltd")
    st.subheader("Type of business: Private")
    st.subheader("Type of site    : Financial technology")






