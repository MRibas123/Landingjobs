#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


# # Excel open

# In[3]:


xls = pd.ExcelFile('Tech Careers Report PT 2021 - Raw Data.xlsx')


# In[4]:


xls.sheet_names


# In[5]:


data = xls.parse('TCS PT 2021 - raw data')


# In[6]:


data.columns


# # Data

# In[7]:


#Choosing meaningfull features from the excel
data_stats= data[['ID','Job_Role','Avg_Salary','Age','Way_Into_Tech','Way_Into_Tech_Other','Education_Level','Working_Experience']]


# In[8]:


data_stats.set_index(['ID'], inplace = True)


# In[9]:


data_stats.head()


# In[10]:


#To have Way_Into_tech and Way_Into_Tech_Other all in the same column.
data_stats['Way_Into_Tech'].fillna(data_stats.Way_Into_Tech_Other)


# In[11]:


data_stats.drop('Way_Into_Tech_Other', axis=1, inplace = True)


# # Languages & Frameworks

# In[12]:


#Choosing meaningfull features from the excel
data_languages = data[['ID','Language_JavaScript','Language_Bash/Shell/PowerShell','Language_SQL', 'Language_Java','Language_C#','Language_Python','Language_PHP','Language_C++','Language_C','Language_TypeScript','Language_Ruby','Language_Swift','Language_Objective-C','Language_VB.NET','Language_Assembly','Language_R','Language_Perl','Language_VBA','Language_Matlab','Language_Go','Language_Scala','Language_Groovy','Language_Coffee Script','Language_Visual Basic 6','Language_Lua','Language_Haskell','Language_HTML/CSS','Language_Kotlin','Language_Rust','Language_Elixir','Language_Clojure','Language_WebAssembly','Language_Dart','Language_Languages_Other']]


# In[13]:


#Have the data with 1 and 0
data_languages.fillna(0,inplace =True)


# In[14]:


data_languages.replace(r'[A-Za-z]+',1,regex=True,inplace = True)


# In[15]:


#Choosing meaningfull features from the excel
data_frameworks = data[['ID','Framework_jQuery', 'Framework_.NET','Framework_Angular/Angular.js','Framework_Ruby on Rails','Framework_React','Framework_Django','Framework_Laravel','Framework_Spring','Framework_Vue.js','Framework_Express','Framework_Meteor','Framework_Flask','Framework_Ember.js','Framework_Drupal','Framework_OutSystems','Framework_Framework_Other']]


# In[16]:


#Have the data with 1 and 0
data_frameworks.fillna(0,inplace =True)


# In[17]:


data_frameworks.replace(r'[A-Za-z]+',1,regex=True,inplace = True)


# In[18]:


data_frameworks['Framework_Framework_Other'].replace("'-", 1,inplace = True)


# In[19]:


display(data_frameworks,data_languages)


# # Data Processing and Cleaning

# In[20]:


data_stats


# In[21]:


data_stats.isnull().sum()


# In[22]:


data_stats[data_stats.isnull().any(axis=1)]


# In[23]:


#Only 83 rows with NaN which represent 2% of the data. Will Remove them.
data_stats.dropna(inplace=True)


# In[24]:


data_stats.isnull().sum()
#No nulls now.


# In[25]:


print(data_stats['Way_Into_Tech'].unique())
print(len(data_stats['Way_Into_Tech'].unique()))
#3 different values, so will use the dummies function to have 6 new features with 0 and 1


# In[26]:


data_stats = pd.get_dummies(data_stats, columns=['Way_Into_Tech'])
data_stats


# In[27]:


data_stats['Working_Experience'].unique()


# In[28]:


data_stats['Working_Experience'] = data_stats['Working_Experience'].apply(lambda x: ['No working experience', 'Less than 1 year', 'Between 1 - 3 years', 'Between 3 - 6 years','Between 6 - 9 years','More than 9 years'].index(x))


# In[29]:


#Check values in Education_Level
print(data_stats.Education_Level.unique())
display(data_stats[data_stats['Education_Level'] == 'I prefer not to answer'])


# In[30]:


#preprocess Education_Level data.

def number_edu_level(row):
    if row['Education_Level'] == 'Basic Education':
        return 0
    elif row['Education_Level'] == 'High School Education' or row['Education_Level'] == 'Trade/technical/vocational training':
        return 1
    elif row['Education_Level'] == 'Bachelor degree' or row['Education_Level'] =='University drop out':
        return 2
    elif row['Education_Level'] == 'Masters degree':
        return 3
    elif row['Education_Level'] == 'Doctoral degree':
        return 4
    elif row['Way_Into_Tech_University'] == 1:
        return 3
    
data_stats['Education_Level'] = data_stats.apply(number_edu_level, axis=1)


# In[31]:


data_stats['Education_Level'].value_counts()


# In[32]:


data_stats[data_stats.isnull().any(axis=1)]


# In[33]:


data_stats = data_stats.fillna({'Education_Level':int(data_stats['Education_Level'].median())})

#Fill the prefer not to say with the median of Education Level


# ## Final Data for clustering

# In[46]:


final_data = data_stats.merge(data_frameworks, how= 'inner', on= 'ID').merge(data_languages, how='inner', on= 'ID').set_index('ID')


# ### Job Role analysis

# In[48]:


grouped_role = final_data.groupby('Job_Role').mean()
display(grouped_role.T)


# In[49]:


# Higher paid job roles have higher age and working experience mean.
#CTO has a diverse knowledge of languages(Ruby, Go...)
#Product Owner/Product Manager and Project Manager are more Self-taught
#JavaScript and SQL are the most known languages inside de high paid jobs


# ### Creating dummies also for job role

# In[50]:


data = pd.get_dummies(final_data, columns=['Job_Role'])
data.head()


# ## Clustering

# In[51]:


ks = range(1, 20)
inertias = []

for k in ks:
    model = KMeans(n_clusters=k)
    model.fit(data)
    inertias.append(model.inertia_)


# In[52]:


plt.plot(ks, inertias)
plt.xlabel('number of clusters')
plt.ylabel('inertia')
plt.xticks(ks)
plt.show()


# In[59]:


# 3 clusters are probably better.


# ### Scaling data

# In[53]:


scaler = StandardScaler()

data_scaled = data.copy()
scaler.fit(data_scaled)

data_scaled = pd.DataFrame(scaler.transform(data_scaled), index = data.index, columns = data.columns)


# ### 3 Clusters

# In[64]:


knn = KMeans(n_clusters=3, random_state = 100 )

data_knn = data_scaled.copy()
knn.fit_predict(data_knn)

data_knn['label'] = knn.labels_

data_cluster = pd.DataFrame(scaler.inverse_transform(data_knn.iloc[:,:-1]), columns = data.columns, index = data.index)

data_cluster['label'] = data_knn['label']


# In[65]:


grouped_data = data_cluster.groupby('label').mean().T


# ### Grouped labels

# In[67]:


pd.set_option('display.max_rows', None, 'display.max_columns', None)
grouped_data[2] = grouped_data[2].round(6)
grouped_data


# In[ ]:


#Group 0 - High paid
#Group 1 - Medium paid
#Group 2 - Low paid

#0 - More Self-taught than the others
#1 - More Uni
#2 - More codebootcamp (with almost no meaning)

#0 Frameworks - Framework_Flask/Framework_Framework_Other
#1 Frameworks - Framework_jQuery/Framework_.NET(huge)
#2 Frameworks - Framework_Angular/Angular.js/Framework_Laravel/Framework_React/Framework_Django/Framework_Spring/Framework_Vue.js/Framework_Express

#0 Languages - Language_Python/Language_R/Language_Languages_Other
#1 Languages - Language_Bash/Shell/PowerShell/Language_SQL/Language_C#/Language_VB.NET
#2 Languages - Language_JavaScript(Huge)/Language_PHP/Language_TypeScript/Language_HTML/CSS

#0 Job_role - Data Scientist/Data Engineer/DevOps Engineer/Project Manager
#1 Job_role - Back-End Developer/Technical Team Leader
#2 Job_role - Full-Stack Developer/ Front-end Developer


# ## Graphic Visualization

# In[68]:


frame_works = grouped_data.loc['Framework_jQuery':'Framework_Framework_Other']
languages = grouped_data.loc['Language_JavaScript':'Language_Languages_Other']
job_roles = grouped_data.loc['Job_Role_Back-End Developer':'Job_Role_UX/UI Designer']


# ### Framework

# In[71]:


fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111)
plt.yticks(fontsize=12)

frame_works.plot(kind='barh', ax=ax, position=0.5)
plt.show()


# ### Languages

# In[72]:


fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111)
plt.yticks(fontsize=12)


languages[(languages>0.1).any(1)].plot(kind='barh', ax=ax, position=0.5)
plt.show()


# ### Job Roles

# In[73]:


fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111)
plt.yticks(fontsize=12)

job_roles.plot(kind='barh', ax=ax, position=0.5)
plt.show()


# In[76]:


data_cluster['label'].value_counts()


# In[ ]:




