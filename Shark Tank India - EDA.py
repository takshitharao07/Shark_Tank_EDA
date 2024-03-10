#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sn


# In[2]:


df=pd.read_csv('Shark Tank India.csv')


# In[3]:


df


# In[4]:


print(df.head())


# In[5]:


#Use info function of the Dataframe to display detail of columns of the dataset.
df.info()


# In[6]:


df.describe()


# In[7]:


# Check the columns in the dataframe
df.columns


# # Pre-processing

# **Drop column**

# In[8]:


#As Company Website columns are irrelevant so i should drop it
df.drop(columns=["Company Website"],inplace=True)


# **Detecting missing values**

# In[9]:


df.isnull().sum()


# In[10]:


df.isnull().sum().sum()


# In[11]:


for i in df.columns:
    if df[i].isnull().sum()>0:
        print(i,'_________', df[i].isnull().sum()*100/df.shape[0] ,'%','________',df[i].dtypes)


# In[12]:


#Checking the missing values of those columns which are of object type
for i in df.columns:
    if df[i].isnull().sum()>0 and df[i].dtypes=='object':
        print(i,'_________',df[i].isnull().sum()*100/df.shape[0],'%','________',df[i].dtypes)


# **Fill missing values & Verify**

# In[13]:


#Inputing the missing values in deal has conditions
df["Deal Has Conditions"].unique()


# In[14]:


#Here nan indicates no conditions so fill nan in Deal has condition
df["Deal Has Conditions"]=df["Deal Has Conditions"].fillna("no")


# In[15]:


df.sample()


# In[16]:


df["Deal Has Conditions"].unique()


# In[17]:


df["All Guest Names"].unique()


# In[18]:


df["All Guest Names"]=df["All Guest Names"].fillna("not present")


# In[19]:


df["All Guest Names"].unique()


# In[20]:


#Missing value % of columns which are of numeric

for i in df.columns:
    if df[i].isnull().sum()>0 and (df[i].dtype=="int32" or df[i].dtype=="float"):
        print(i,'_________',df[i].isnull().sum()*100/df.shape[0],'%','________',df[i].dtypes)


# In[21]:


#Taking male passengers , female passengers , transgender passengers , couple presenters columns

df[['Male Presenters','Female Presenters','Transgender Presenters','Couple Presenters']]


# In[22]:


#From this ablove output we can see that NaN indicates 0 so we fill NaN with 0 in male passengers , female passengers , couple presenters , transgenders

presenters =['Male Presenters','Female Presenters','Transgender Presenters','Couple Presenters']
for i in presenters:
    df[i].fillna(0,inplace=True)


# In[23]:


#Verifying the results whether the missing values in above mentioned columns has been filled or not

df[presenters].isnull().sum().sum()


# **Change data types of columns**

# In[24]:


df[presenters]=df[presenters].astype(int)


# In[25]:


df[presenters].dtypes


# In[26]:


#Filling null values of columns of dtype of float:

for i in df.columns:
    if df[i].isnull().sum()>0 and df[i].dtype=="float":
        df[i].fillna(0,inplace=True)


# In[63]:


df["Number of Sharks in Deal"]=df["Number of Sharks in Deal"].astype(int)


# In[27]:


df.isnull().sum().sum()

Season End _________ 18.939393939393938 % ________ object
Original Air Date _________ 77.52525252525253 % ________ object
Pitchers City _________ 0.25252525252525254 % ________ object
Pitchers State _________ 0.25252525252525254 % ________ object
Cash Burn _________ 88.38383838383838 % ________ object
Has Patents _________ 91.66666666666667 % ________ object
Bootstrapped _________ 99.4949494949495 % ________ object
# In[28]:


objects=["Season End","Original Air Date","Pitchers City","Pitchers State","Cash Burn","Has Patents","Bootstrapped","Invested Guest Name"]
for i in objects:
    print(df[i].unique(),'\n')


# In[60]:


df["Season End"].fillna('Ongoing',inplace=True)
df["Original Air Date"].fillna('',inplace=True)
df["Pitchers City"].fillna('Others',inplace=True)
df["Pitchers State"].fillna('Others',inplace=True)
df["Cash Burn"].fillna('no',inplace=True)
df["Has Patents"].fillna('no',inplace=True)
df["Bootstrapped"].fillna('Funded',inplace=True)
df["Invested Guest Name"].fillna('Others',inplace=True)


# In[56]:


df.isnull().sum().sum()

#No null values


# # EDA

# **Seasons**

# In[31]:


# Number of seasons
df["Season Number"].unique()


# In[32]:


# When the seasons of Shark Tank India started
start = df["Season Start"].unique()
start


# In[33]:


# When the seasons of Shark Tank India ended
end = df["Season End"].unique()
end


# In[34]:


x=pd.DataFrame([[start[0],end[0]],[start[1],end[1]],[start[2],end[2]]],index=["season1","season2","season3"],columns=["start_aired_date","end_aired_date"])
x


# **Episodes**

# In[35]:


# Total number of episodes
np.sum(df.groupby(["Season Number"])["Episode Number"].nunique().values)


# In[36]:


# Episodes in each season
df.groupby(["Season Number"])["Episode Number"].nunique()


# **Pitches & Deals**

# In[37]:


# Entreprenuers participated in the Shark Tank
df["Pitch Number"].nunique()


# In[38]:


# Entreprenuers participated in each season
df.groupby(["Season Number"])["Pitch Number"].count()


# In[214]:


# Group data by season and count pitches
pitch_counts_by_season = df.groupby(["Season Number"])["Pitch Number"].count()

# Create a pie chart
plt.pie(pitch_counts_by_season.values, labels = pitch_counts_by_season.index, autopct = "%.2f%%", colors = sn.husl_palette(l=.5))

# Customize and display the chart as needed (e.g., title, legend)
plt.title("Pitch Distribution by Season")
plt.show()


# In[39]:


# Total number of deals
print("Number of Deals Received: ", df['Received Offer'].count())

# Total number of accepted deals
print("Number of Deals Accepted: ", df['Accepted Offer'].count())


# In[40]:


# check how many company doesn't recieve an offer
Denied_offer = df[df['Received Offer'] == 0]['Startup Name'].nunique()
Denied_offer


# In[41]:


# Unique ideas

df['Has Patents'].count()


# In[42]:


# How many brands telecasted in each episode of each season?
df.groupby(["Season Number","Episode Number"])["Pitch Number"].agg(["count"]).sort_values(by="count",ascending=False)


# # Industry

# In[43]:


# Distribution of industries for the startups
Industries_Category=df['Industry'].value_counts()
Industries_Category


# In[44]:


# Plotting the distribution of industries for all startups
plt.figure(figsize=(10, 6))

#Industries_Category.plot(kind='bar')     #matplotlib

sn.barplot(x=Industries_Category.values, y=Industries_Category.index)   #seaborn
plt.title('Distribution of Industries for All Startups on Shark Tank India')
plt.xlabel('Number of Startups')
plt.ylabel('Industry')
plt.tight_layout()
plt.show()


# In[45]:


#Aggregate on the bases of value_counts
df.groupby(["Season Number"])["Industry"].agg(["value_counts"])


# In[48]:


# Group data by Industry and Season Number
industry_season_counts = df.groupby(['Industry', 'Season Number']).size()
industry_season_counts


# In[49]:


# Group data by Industry and Season Number
industry_season_counts = data.groupby(['Industry', 'Season Number']).size().unstack()

# Plotting multiple bar graphs for each season
for season in industry_season_counts.columns:
    plt.figure(figsize=(12, 6))
    industry_season_counts[season].dropna().sort_values().plot(kind='bar', color='maroon')
    plt.title(f'Industry Distribution for Season {season}')
    plt.xlabel('Industry')
    plt.ylabel('Number of Startups')
    plt.xticks(rotation=45)
    plt.show()


# In[50]:


# Group data by Industry and Season
industry_season_counts = data.groupby(['Industry', 'Season Number']).size().unstack()

# Plotting the bar chart
industry_season_counts.plot(kind='bar', stacked=True, figsize=(12, 8), color=['maroon', '#300096', 'black'])
plt.title('Distribution of Industries Across Seasons')
plt.xlabel('Industry')
plt.ylabel('Number of Startups')
plt.legend(title='Season Number')

plt.show()


# In[85]:


#Top 5 industry
df["Industry"].value_counts()[0:5]


# In[89]:


plt.pie(Industries_Category[0:5].values,labels=Industries_Category[0:5].index,autopct="%.2f%%");


# In[86]:


#Bottom 5 industry 
df["Industry"].value_counts().tail(5)


# In[93]:


plt.pie(Industries_Category.tail(5).values, labels=Industries_Category.tail(5).index, autopct="%.2f%%");


# # Pitcher

# **Gender-wise**

# In[46]:


#Number of Presenters	Male Presenters	Female Presenters	Transgender Presenters
print("Total Number of Presenters:",df['Number of Presenters'].sum())
print("Number of Male Presenters:",df['Male Presenters'].sum())
print("Number of Female Presenters:",df['Female Presenters'].sum())
print("Number of TransgenderPresenters:",df['Transgender Presenters'].sum())


# In[47]:


# Gender distribution across different seasons
season_wise_gender_data = df.groupby('Season Number')[['Number of Presenters', 'Male Presenters', 'Female Presenters', 'Transgender Presenters']].sum()
season_wise_gender_data


# In[133]:


l = ["Male Presenters", "Transgender Presenters", "Female Presenters"]

# Pie Chart
plt.pie( df[l].sum(), labels=l, autopct="%.2f%%", colors=sn.husl_palette(4), explode=[0, 0.2, 0]);
plt.title('Gender Distribution (Pie Chart)')


# **Age-wise**

# In[102]:


df["Pitchers Average Age"].unique()


# In[141]:


plt.subplot(1,2,1)
sn.countplot(x="Pitchers Average Age",data=df,palette=sn.husl_palette(l=.4))
plt.title("pitcher's age count")


# # Location - wise analysis

# In[142]:


df["Pitchers State"].value_counts()


# In[143]:


states=df["Pitchers State"].values
state = ' '.join(states)
state


# In[149]:


pip install wordcloud


# In[152]:


from wordcloud import WordCloud
wordcloud = WordCloud(width=800, height=800, background_color='black').generate(state)
plt.figure(figsize=(14,8), facecolor=None)
plt.imshow(wordcloud)
plt.tight_layout(pad=0)
plt.show()


# In[153]:


df["Pitchers State"].unique()


# In[154]:


df1=df.copy()
index=0
for i in df1["Pitchers State"]:
    if "," in i:
        df1.loc[index,"Pitchers State"]="hybrid state"
    else:
        df1.loc[index,"Pitchers State"]=i
    index=index+1


# In[155]:


df1.head(3)


# In[157]:


df1["Pitchers State"].unique()


# In[ ]:


north=["Delhi","Punjab","Delhi,Punjab","Haryana","Jammu & Kashmir","Uttar Pradesh","Uttarakhand","Himachal Pradesh","Uttarakhand,Uttar Pradesh"]
central=["Madhya Pradesh","Chhattisgarh"]
south=["Karnataka","Telangana",'Kerala',"Tamil Nadu","Goa","Karnataka,Telangana","Karnataka,Andhra Pradesh"]
west=["Gujarat","Maharashtra","Rajasthan"]
east=["Bihar","West Bengal","Jharkhand","Arunachal Pradesh"]
hybrid=["Karnataka,West Bengal","Delhi,Maharashtra","Haryana,Madhya Pradesh","Telangana,Maharashtra","Kerala,Maharashtra","Haryana,West Bengal","Haryana,Maharashtra","Jharkhand,Chhattisgarh","Gujarat,Uttar Pradesh"]


# # Sharks Analysis

# **Sharks Investment Amount**

# In[178]:


# How many sharks participated in the show and what are their names?
df.columns[43:-11:3]


# In[180]:


sharks_names=[]
for i in df.columns[43:-11:3]:
    sharks=i.split(maxsplit=1)
    sharks_names.append(sharks[0])
print(len(sharks_names), "sharks participated \n")
print("following are the names of the sharks ",sharks_names)


# In[181]:


l=[]
for i in df.columns[43:-11:3]:
    s=df[i].sum()

    l.append(s)
l


# In[182]:


plt.bar(sharks_names,l,color="maroon",edgecolor="black")
plt.tight_layout()


# **Sharks participated in each season**

# In[183]:


df_1=df[df["Season Number"]==1]
for i in df.columns[43:-11:3]:
    if df_1[i].sum()==0:
        print(i.split(maxsplit=1)[0],"did not participated in season 1  \n")
    else:
        print(i.split(maxsplit=1)[0],"participated in season 1  \n")


# In[184]:


df_2=df[df["Season Number"]==2]
for i in df.columns[43:-11:3]:
    if df_2[i].sum()==0:
        print(i.split(maxsplit=1)[0],"did not participated in season 2 \n")
    else:
        print(i.split(maxsplit=1)[0],"participated in season 2  \n")


# In[185]:


df_3=df[df["Season Number"]==3]
for i in df.columns[43:-11:3]:
    if df_3[i].sum()==0:
        print(i.split(maxsplit=1)[0],"did not participated in season 3 \n")
    else:
        print(i.split(maxsplit=1)[0],"participated in season 3  \n")


# **Shark invested in each deal**

# In[195]:


l_1=[]
for i in df_1.columns[43:-11:3]: ## season 2
    s=df_1[i].sum() 
    l_1.append(s)

l_1


# In[196]:


l_2=[]
for i in df_2.columns[43:-11:3]: ## season 2
    s=df_2[i].sum()  
    l_2.append(s)

l_2


# In[197]:


l_3=[]
for i in df_3.columns[43:-11:3]: ## season 3
    s=df_3[i].sum()
    l_3.append(s)

l_3


# In[205]:


plt.figure(figsize=(28,7))
plt.subplot(1,3,1)
plt.bar(sharks_names,l_1,color="pink",edgecolor="white")
plt.title("Total amount invested by sharks in season 1",fontweight="black",pad=5,size=15,color="gray")

plt.subplot(1,3,2)
plt.bar(sharks_names,l_2,color="orange",edgecolor="white")
plt.title("Total amount invested by sharks in season 2",fontweight="black",pad=5,size=15,color="gray")

plt.subplot(1,3,3)
plt.bar(sharks_names,l_3,color="red",edgecolor="white")
plt.title("Total amount invested by sharks in season 3",fontweight="black",pad=5,size=15,color="gray")


# # Insights

# In[207]:


df["Number of Sharks in Deal"].unique()


# In[208]:


df[df["Number of Sharks in Deal"]==5][["Startup Name","Business Description"]]

