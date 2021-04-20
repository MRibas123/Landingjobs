# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 14:47:05 2021

@author: goncalo
"""

import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['axes.edgecolor']='#333F4B'
plt.rcParams['axes.linewidth']=0.8
plt.rcParams['xtick.color']='#333F4B'
plt.rcParams['ytick.color']='#333F4B'

plt.rc('axes', titlesize=20)     # fontsize of the axes title
plt.rc('axes', labelsize=20)     # fontsize of the x and y labels
plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
plt.rc('ytick', labelsize=20)    # fontsize of the tick labels
plt.rc('legend', fontsize=15)    # legend fontsize

save = False # set to "True" if you want to save the figures.

#%% Read the dataset (please have it at the same directory as the code)

xlsx = pd.ExcelFile('Tech Careers Report PT 2021 - Raw Data.xlsx')
df = pd.read_excel(xlsx, 'TCS PT 2021 - raw data')

#%% Divide the dataset by age groups

df_age = (df.groupby(pd.cut(df['Age'], [19,30,50,pd.np.inf], right=False)).mean())

mot = ["Job_Motivator_Work_life_balance", "Job_Motivator_Compensation_and_benefits", 
       "Job_Motivator_Training/Development_programs_at_work", "Job_Motivator_Career_growth_opportunities",	
       "Job_Motivator_Remote_working", "Job_Motivator_Flexible_schedule",
       "Job_Motivator_Company_culture",	"Job_Motivator_The_technologies_I'm_working_with",
       "Job_Motivator_Versatility/Variety_of_projects",	
       "Job_Motivator_Freedom_to_choose_the_clients_and/or_projects",
       "Job_Motivator_Being_autonomous_at_work", 
       "Job_Motivator_How_widely_used_or_impactful_the_product/service_I_work_on_is",
       "Job_Motivator_Environmentally_friendly/responsible_work_practice"]

mot_fresh = ["Work life balance", "Compensation and benefits", 
       "Training/Development programs at work", "Career growth opportunities",	
       "Remote working", "Flexible schedule",
       "Company culture",	"The technologies I'm working with",
       "Versatility/Variety of projects",	
       "Freedom to choose the clients and/or projects",
       "Being autonomous at work", 
       "How widely used or impactful the product/service I work on is",
       "Environmentally friendly/responsible work practice"]

#%% Find top 5 motivators per age groups

scores = [[0 for x in range(len(mot))] for y in range(len(df_age))] 

for i in range(len(df_age)):
    k=0
    for j in mot:
        scores[i][k] = df_age.iloc[i][j]
        k+=1
  
top5_index = []   
top5_score = [[0 for x in range(5)] for y in range(len(df_age))]

for i in range(len(df_age)):
    top5_index.append(sorted(range(len(scores[i])), key=lambda a: scores[i][a]))     
    

for i in range(len(df_age)):
    del top5_index[i][0:(len(scores[0])-5)]  #keep just the top 5
    

flat_top5_index = [item for sublist in top5_index for item in sublist]
flat_top5_index = list(dict.fromkeys(flat_top5_index))
flat_top5_index.sort(reverse=True)

top5_score = [[0 for x in range(len(flat_top5_index))] for y in range(len(df_age))]

for i in range(len(df_age)):
    k=0
    for j in flat_top5_index:
        top5_score[i][k] = scores[i][j]
        k+=1
    
mot_top = []

for i in flat_top5_index:
    mot_top.append(mot_fresh[i])
   
s_young = top5_score[0]
s_middle = top5_score[1]
s_old = top5_score[2]
 
#%% Plot
    
fig = plt.figure(figsize=(11.0, 10.0))
ax = fig.add_subplot(111)

plt.yticks(fontsize=15)

df_young = pd.DataFrame({'Mot':mot_top, 'scores': s_young})
df_middle = pd.DataFrame({'Mot':mot_top, 'scores': s_middle})
df_old = pd.DataFrame({'Mot':mot_top, 'scores': s_old})


df_young.plot(kind='barh', x='Mot', y='scores', ax=ax, position=-0.5, width=0.15)

df_middle.plot(kind='barh', x='Mot', y='scores', ax=ax, position=0.5, width=0.15, color='red')

df_old.plot(kind='barh', x='Mot', y='scores', ax=ax, position=1.5, width=0.15, color='green')

plt.legend(['Young (19 to 29)', 'Middle (30 to 49)', 'Old (50 to 67)'], ncol=3)
plt.grid(linestyle = '--')
ax.yaxis.grid(False)
plt.ylabel('Motivation')
plt.xlabel('Average score (0 - min and 7 - max)')
plt.ylim((-0.5, len(df_young)))

if save:
    plt.savefig('age_mot.png',  bbox_inches='tight')
    
    
    
    
    
    