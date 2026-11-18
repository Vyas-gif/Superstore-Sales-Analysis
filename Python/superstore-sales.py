#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
df=pd.read_csv("myprojects.csv")


# In[6]:


print(df.head())
print(df.shape)
print(df.info())
print(df.isnull().sum())
print(df.duplicated().sum())


# In[8]:


df.columns


# In[10]:


df.dtypes


# In[12]:


df["Order Date"]=pd.to_datetime(df["Order Date"],format="mixed",dayfirst=False)
df["Ship Date"]=pd.to_datetime(df["Ship Date"],format="mixed",dayfirst=False)


# In[15]:


print(df[["Order Date","Ship Date"]].dtypes)


# In[16]:


print(df.isnull().sum())
print(df.describe())


# In[30]:


total_sales=df["Sales"].sum()
total_profit=df["Profit"].sum()
total_orders=df["Order ID"].nunique()
total_customers=df["Customer ID"].nunique()


# In[23]:


category_sales=df.groupby("Category")["Sales"].sum()
print(category_sales.sort_values(ascending=False))


# In[25]:


region_sales=df.groupby("Region")["Sales"].sum()
print(region_sales.sort_values(ascending=False))


# In[27]:


category_profit=df.groupby("Category")["Profit"].sum()
print(category_profit.sort_values(ascending=False))


# In[31]:


print("Total Sales:", df["Sales"].sum())

print("Total Profit:", df["Profit"].sum())

print("Total Orders:", df["Order ID"].nunique())

print("Total Customers:", df["Customer ID"].nunique())


# In[32]:


df["Year-Month"]=df["Order Date"].dt.to_period("M")
monthly_sales=df.groupby("Year-Month")["Sales"].sum()
print(monthly_sales)


# In[33]:


monthly_sales.plot(kind="line",figsize=(12,5),
                   marker="o")
plt.title("monthly Sales Trend")
plt.xlabel("month")
plt.ylabel("Sales")
plt.grid()
plt.show()


# In[37]:


top_products=(df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10))
print(top_products)   


# In[39]:


subcategory_profit=df.groupby("Sub-Category")["Profit"].sum().sort_values()
print(subcategory_profit)


# In[40]:


discount_analysis=df.groupby("Discount").agg({"Sales":'sum',"Profit":"sum"})
print(discount_analysis)


# In[41]:


segment_sales=df.groupby("Segment")["Sales"].sum().sort_values(ascending=False)
print(segment_sales)


# In[42]:


subcategory_profit.plot(
    kind="bar",
    figsize=(12, 6)
)

plt.title("Profit by Sub-Category")
plt.xlabel("Sub-Category")
plt.ylabel("Total Profit")
plt.xticks(rotation=45)
plt.axhline(y=0)
plt.tight_layout()
plt.show()


# In[43]:


import pandas as pd
import csv

df.to_csv(
    "myprojects.csv",
    index=False,
    encoding="utf-8",
    quoting=csv.QUOTE_ALL
)


# In[45]:


get_ipython().system('pip install mysql-connector-python')
print(df.shape)
print(df.columns.tolist())


# In[46]:


import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vyas@sql",
    database="superstore_analysis"
)

print("Connected successfully!")


# In[47]:


print(df.shape)


# In[49]:


cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS superstore_python")

cursor.execute("""
CREATE TABLE superstore_python (
    `Row ID` INT,
    `Order ID` VARCHAR(30),
    `Order Date` DATETIME,
    `Ship Date` DATETIME,
    `Ship Mode` VARCHAR(30),
    `Customer ID` VARCHAR(30),
    `Customer Name` VARCHAR(100),
    `Segment` VARCHAR(30),
    `Country` VARCHAR(100),
    `City` VARCHAR(100),
    `State` VARCHAR(100),
    `Postal Code` VARCHAR(20),
    `Region` VARCHAR(30),
    `Product ID` VARCHAR(30),
    `Category` VARCHAR(50),
    `Sub-Category` VARCHAR(50),
    `Product Name` VARCHAR(255),
    `Sales` DECIMAL(15,4),
    `Quantity` INT,
    `Discount` DECIMAL(5,2),
    `Profit` DECIMAL(15,4)
)
""")

conn.commit()

print("Table created successfully!")


# In[51]:


# Remove Year-Month from SQL import
df_import = df.drop(
    columns=["Year-Month"],
    errors="ignore"
).copy()

print(df_import.shape)


# In[52]:


df_import["Order Date"] = pd.to_datetime(
    df_import["Order Date"]
).dt.to_pydatetime()

df_import["Ship Date"] = pd.to_datetime(
    df_import["Ship Date"]
).dt.to_pydatetime()


# In[53]:


import pandas as pd
import numpy as np

def convert_value(value):
    if pd.isna(value):
        return None

    if isinstance(value, np.generic):
        return value.item()

    return value

values = [
    tuple(convert_value(v) for v in row)
    for row in df_import.itertuples(index=False, name=None)
]

print("Prepared records:", len(values))


# In[54]:


columns = [f"`{col}`" for col in df_import.columns]

sql = f"""
INSERT INTO superstore_python ({','.join(columns)})
VALUES ({','.join(['%s'] * len(columns))})
"""

cursor.executemany(sql, values)

conn.commit()

print("Imported records:", cursor.rowcount)


# In[55]:


cursor.execute("""
SELECT COUNT(*) FROM superstore_python
""")

print(cursor.fetchone())


# In[ ]:




