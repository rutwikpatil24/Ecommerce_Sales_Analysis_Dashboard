#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pandas numpy openpyxl sqlalchemy pymysql')


# In[6]:


# step 1: Import Required Libraries

import pandas as pd
import numpy as np


# In[9]:


# step 2: Load Dataset

df = pd.read_excel('Ecommerce_Unclean_Project.xlsx')


# In[10]:


# step 3: Explore The Dataset
# View First 5 Records

df.head()


# In[11]:


#View Dataset Information

df.info


# In[12]:


# Statistical Summary
df.describe()


# In[14]:


# Dataset Shape
df.shape


# In[16]:


# step 4: Checking Missing Values

df.isnull().sum()


# In[17]:


#Step 5: Check Duplicate Records

df.duplicated().sum()


# In[21]:


# Remove Duplicate Records 

df.drop_duplicates(inplace=True)


# In[22]:


# Step 6: Replace Invalid Values
# replace Common Invalid Values With Nan

df.replace(['N/A','NULL',''],np.nan,inplace=True)


# In[23]:


# Remove Extra Spaces

df = df.apply(lambda x: x.str.strip() if x.dtype == 'objetcs' else x)


# In[24]:


# Step 8: Standardize Text Format
# Convert Text Into Proper Case.

df['Customer_Name'] = df['Customer_Name'].str.title()

df['City'] = df['City'].str.title()

df['State'] = df['State'].str.title()


# In[25]:


# Step 9: Validate Email Addresses
# Keep Only Valid Email Records.

df = df[df['Email'].str.contains('@',na=False)]


# In[29]:


# Step 10: Convert Date Column

df['Order_Date']=pd.to_datetime(df['Order_Date'],format='%d-%m-%Y',errors='coerce')
df['Delivery_Date']=pd.to_datetime(df['Delivery_Date'],format='%d-%m-%Y',errors='coerce')


# In[31]:


# Step 11: Convert Numeric Values

cols = ['Qty','Unit_Price','Discount']

for c in cols:
    df[c] = pd.to_numeric(df[c],errors='coerce')


# In[32]:


# Step 12: Reomve Invalid Quantity
# Remove record having negative or zero quantity

df = df[df['Qty']>0]


# In[35]:


# Step 13: Fill Missing Values

df['Discount']= df['Discount'].fillna(0)

df['Phone'] = df['Phone']. fillna('unknown')

df['Delivery_Date'] = df['Delivery_Date'].fillna(df['Order_Date'])


# In[36]:


# Step 14: Feature Engineering
# Total Sales

df['Sales']= df['Qty']*df['Unit_Price']


# In[37]:


df


# In[38]:


# Net Amount

df['Net_Amount']=df['Sales']-(df['Sales']*df['Discount']/100)


# In[39]:


df


# In[40]:


# Profit (Example: 20%)

df['Profit']=df['Net_Amount']*0.20


# In[41]:


df


# In[42]:


# Order Month

df['Month']=df['Order_Date'].dt.month_name()


# In[43]:


df


# In[45]:


# Order Year

df['Year']=df['Order_Date'].dt.year


# In[46]:


df


# In[47]:


# Weekday

df['Weekday']=df['Order_Date'].dt.day_name()


# In[48]:


df


# In[49]:


# Step 15: Final Data Validation 

df.info()


# In[52]:


df.isnull().sum()


# In[53]:


df.describe()


# In[55]:


# Step 16: Export Clean Data
df.to_csv('Clean_Ecommerce.csv',index=False)


# In[57]:


import os 
print(os.getcwd())


# In[64]:


# Step 17: Import Data Into MySQL

from sqlalchemy import create_engine
from sqlalchemy.engine import URL

url = URL.create(
    "mysql+pymysql",
    username="root",
    password="",
    host="localhost",
    database="ecommerce"
)
engine = create_engine(url)


# In[65]:


# Export Dataframe to MySQL
df.to_sql(
    name='order',
    con=engine,
    if_exists='replace',
    index=False
)



# In[ ]:




