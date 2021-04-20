# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 16:43:40 2021

@author: goncalo
"""

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

perk = ["Job_Perk_Meals_allowance/Company_provided_meals_or_snacks",
       "Job_Perk_Transportation_benefit",
       "Job_Perk_Health_benefits",
       "Job_Perk_Fitness_or_wellness_benefit_(ex._gym_membership)",
       "Job_Perk_Computer/_Office_equipment_allowance",
       "Job_Perk_Professional_development_sponsorship",
       "Job_Perk_Annual_bonus",
       "Job_Perk_Long-term_leave",
       "Job_Perk_Parental_leave",
       "Job_Perk_Stock_options_or_shares",
       "Job_Perk_Education_sponsorship",
       "Job_Perk_Child_care"]

perk_fresh = ["Meals allowance/Company provided meals or snacks",
       "Transportation benefit",
       "Health benefits",
       "Fitness or wellness benefit (ex. gym membership)",
       "Computer/ Office equipment allowance",
       "Professional development sponsorship",
       "Annual bonus",
       "Long-term leave",
       "Parental leave",
       "Stock options or shares",
       "Education sponsorship",
       "Child care"]

#%% Find top 5 motivators per age groups

scores = [[0 for x in range(len(perk))] for y in range(len(df_age))] 

for i in range(len(df_age)):
    k=0
    for j in perk:
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
    
perk_top = []

for i in flat_top5_index:
    perk_top.append(perk_fresh[i])
   
s_young = top5_score[0]
s_middle = top5_score[1]
s_old = top5_score[2]

#%% Plot
    
fig = plt.figure(figsize=(11.0, 10.0))
ax = fig.add_subplot(111)

ax.yaxis.set_label_position("right")
ax.yaxis.tick_right()

plt.yticks(fontsize=15)

df_young = pd.DataFrame({'Perk':perk_top, 'scores': s_young})
df_middle = pd.DataFrame({'Perk':perk_top, 'scores': s_middle})
df_old = pd.DataFrame({'Perk':perk_top, 'scores': s_old})


df_young.plot(kind='barh', x='Perk', y='scores', ax=ax, position=-0.5, width=0.15)

df_middle.plot(kind='barh', x='Perk', y='scores', ax=ax, position=0.5, width=0.15, color='red')

df_old.plot(kind='barh', x='Perk', y='scores', ax=ax, position=1.5, width=0.15, color='green')

plt.legend(['Young (19 to 29)', 'Middle (30 to 49)', 'Old (50 to 67)'], ncol=3)
plt.grid(linestyle = '--')
ax.yaxis.grid(False)
plt.ylabel('Job Perks')
plt.xlabel('Average score (0 - min and 7 - max)')
plt.ylim((-0.5, len(df_young)))

plt.gca().invert_xaxis()
    
if save:
    plt.savefig('age_perk.png',  bbox_inches='tight')
    
    
    
    