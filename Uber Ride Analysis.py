#!/usr/bin/env python
# coding: utf-8

# # Importing libraries

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import os


# In[ ]:





# In[ ]:





# In[5]:


df = pd.read_csv(r"C:\Users\Soami Computers\Downloads\My Uber Drives.csv")


# In[ ]:





# In[ ]:





# In[6]:


df.head()


# In[7]:


df.tail()


# In[10]:


print(df.shape)


# In[11]:


df.dtypes


# In[12]:


df.isna().sum()


# In[13]:


df[df['END_DATE*'].isna()]


# In[14]:


df.drop(df[df['END_DATE*'].isna()].index,axis=0,inplace=True)
df.isna().sum()


# In[15]:


df.info()


# In[16]:


df.drop(['PURPOSE*'],axis=1,inplace=True)
df.head(2)


# In[17]:


df[df.duplicated()]


# In[18]:


df.drop(df[df.duplicated()].index, axis=0, inplace=True)
df[df.duplicated()]


# In[19]:


#Converting start_date & end_date cols into datetime
df['START_DATE*'] = pd.to_datetime(df['START_DATE*'], format='%m/%d/%Y %H:%M')
df['END_DATE*'] = pd.to_datetime(df['END_DATE*'], format='%m/%d/%Y %H:%M')
df.dtypes


# In[20]:


df['CATEGORY*'].unique()


# In[21]:


df[['CATEGORY*','MILES*']].groupby(['CATEGORY*']).agg(tot_miles=('MILES*','sum'))


# In[25]:


plt.figure()
df[['CATEGORY*','MILES*']].groupby(['CATEGORY*']).agg(tot_miles=('MILES*','sum')).plot(kind='bar')
plt.xlabel('Category')
plt.ylabel('Total Miles')
plt.title('Total Miles per Category')


# In[23]:


len(df['START*'].unique())


# In[24]:


# Top 10 Start places
df['START*'].value_counts(ascending=False)[:10]


# In[58]:


df['START*'].value_counts(ascending=False)[:10].plot(kind='barh',ylabel='Places',xlabel='Pickup Count',
                                                     title='Top 10 Pickup places')


# In[28]:


len(df['STOP*'].unique())


# In[29]:


df['STOP*'].value_counts(ascending=False)[:10].plot(kind='barh',ylabel='Places',xlabel='Pickup Count',
                                                    title='Top 10 Drop places')


# In[30]:


df[df['START*']=='Unknown Location']['START*'].value_counts()


# In[31]:


df[df['STOP*']=='Unknown Location']['STOP*'].value_counts()


# In[32]:


sns.histplot(df['MILES*'],kde=True)


# In[33]:


df.describe().T


# In[34]:


df.head()


# In[35]:


df.groupby(['START*','STOP*'])['MILES*'].apply(print)


# In[36]:


df.groupby(['START*','STOP*'])['MILES*'].sum().sort_values(ascending=False)[1:11]


# In[42]:


def is_roundtrip(df):
    if df['START*'] == df['STOP*']:
        return 'YES'
    else:
        return 'NO'
df['ROUND_TRIP*'] = df.apply(is_roundtrip, axis=1)
sns.countplot(x='ROUND_TRIP*',data=df, order=df['ROUND_TRIP*'].value_counts().index)


# In[43]:


df['ROUND_TRIP*'].value_counts()


# In[44]:


df.dtypes


# In[45]:


df['Ride_duration'] = df['END_DATE*']-df['START_DATE*']
df.head()


# In[46]:


df.loc[:, 'Ride_duration'] = df['Ride_duration'].apply(lambda x: pd.Timedelta.to_pytimedelta(x).days/(24*60) + 
                                                       pd.Timedelta.to_pytimedelta(x).seconds/60)
df.head()


# In[47]:


#Capture Hour, Day, Month and Year of Ride in a separate column
df['month'] = pd.to_datetime(df['START_DATE*']).dt.month
df['Year'] = pd.to_datetime(df['START_DATE*']).dt.year
df['Day'] = pd.to_datetime(df['START_DATE*']).dt.day
df['Hour'] = pd.to_datetime(df['START_DATE*']).dt.hour
df['day_of_week'] = pd.to_datetime(df['START_DATE*']).dt.dayofweek
days = {0:'Mon',1:'Tue',2:'Wed',3:'Thur',4:'Fri',5:'Sat',6:'Sun'}
df['day_of_week'] = df['day_of_week'].apply(lambda x: days[x])
df.head()


# In[48]:


df['month'] = df['month'].apply(lambda x: calendar.month_abbr[x])
df.head()


# In[49]:


print(df['month'].value_counts())


# In[50]:


sns.countplot(x='month',data=df,order=pd.value_counts(df['month']).index,hue='CATEGORY*')


# In[51]:


sns.countplot(x='day_of_week',data=df,order=pd.value_counts(df['day_of_week']).index,hue='CATEGORY*')


# In[52]:


df.groupby('month').mean()['MILES*'].sort_values(ascending = False).plot(kind='bar')
plt.axhline(df['MILES*'].mean(), linestyle='--', color='red', label='Mean distance')
plt.legend()
plt.show()


# In[53]:


sns.countplot(x='Hour',data=df,order=pd.value_counts(df['Hour']).index,hue='CATEGORY*')


# In[54]:


df.head()


# In[55]:


df['Duration_hours'] = df['Ride_duration']/60
df['Speed_KM'] = df['MILES*']/df['Duration_hours']
df.head(2)


# In[56]:


fig, ax = plt.subplots()
sns.histplot(x='Speed_KM',data=df,kde=True,ax=ax)


# In[ ]:




