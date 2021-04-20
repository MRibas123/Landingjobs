# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 15:29:30 2021

@author: goncalo
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import interpolate

plt.rcParams['axes.edgecolor']='#333F4B'
plt.rcParams['axes.linewidth']=0.8
plt.rcParams['xtick.color']='#333F4B'
plt.rcParams['ytick.color']='#333F4B'

plt.rc('axes', titlesize=20)     # fontsize of the axes title
plt.rc('axes', labelsize=20)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
plt.rc('ytick', labelsize=20)    # fontsize of the tick labels
plt.rc('legend', fontsize=15)    # legend fontsize

save = False # set to "True" if you want to save the figures.

#%% Read the dataset (please have it at the same directory as the code)

xlsx = pd.ExcelFile('Tech Careers Report PT 2021 - Raw Data.xlsx')
df = pd.read_excel(xlsx, 'TCS PT 2021 - raw data')


#%% Prog Language frequency

PL = ['JavaScript', 'Bash/Shell/PowerShell','SQL', 'Java', 'C#', 'Python', 'PHP', 'C++', 'C', 'TypeScript', 'Ruby', 'Swift', 'Objective-C', 
      'VB.NET', 'Assembly', 'R', 'Perl', 'VBA', 'Matlab', 'Go', 'Scala', 'Groovy', 'Coffee Script', 
      'Visual Basic 6', 'Lua', 'Haskell', 'HTML/CSS', 'Kotlin', 'Rust', 'Elixir', 'Clojure', 'WebAssembly',
      'Dart']

PL_count = []

for i in PL:
    PL_count.append(df["Language_"+ i].count())


total = sum(PL_count)

PL_freq = PL_count/total*100


df_PL = pd.DataFrame({'PL':PL, 'freq':PL_freq})
df_PL.sort_values(by=['freq'], inplace=True)

fig = plt.figure(figsize=(10.0, 15.0))
ax = fig.add_subplot(111)

df_PL.plot(kind='barh', x='PL', y='freq', rot=0, ax=ax)
plt.grid(linestyle = '--')
plt.ylabel('Programming Language')
plt.xlabel('%')
ax.get_legend().remove()

#%% Average salary per language group

AvgSal = [] #list for the average salary per Programming Language group
k=0

for i in PL:
    AvgSal.append(df.loc[df["Language_" + i] == i]['Avg_Salary'].sum()/PL_count[k])
    k+=1


df_salary = pd.DataFrame({'PL':PL, 'Avg_Salary': AvgSal})
df_salary.sort_values(by=['Avg_Salary'], inplace=True)

fig = plt.figure(figsize=(10.0, 15.0))
ax = fig.add_subplot(111)

df_salary.plot(kind='barh', x='PL', y='Avg_Salary', rot=0, ax=ax)
plt.grid(linestyle = '--')
plt.ylabel('Programming Language')
plt.xlabel('Average anual salary ($)')

ax.set_xlim([25000, 55000])
ax.get_legend().remove()

#%% Join both bar plots

fig = plt.figure(figsize=(10.0, 20.0))
ax = fig.add_subplot(111)

df_final = pd.DataFrame({'PL':PL, 'freq':PL_freq, 'Avg_Salary':AvgSal })

df_final.sort_values(by=['Avg_Salary'], inplace=True)

df_final.plot(kind='barh',color='cornflowerblue', x='PL', y='freq', ax=ax, position=1, legend=False, width=0.25)


y_axis = ax.axes.get_yaxis()
y_axis.set_visible(False)

ax2 = ax.twiny()

df_final.plot(kind='barh',color='coral', x='PL', y='Avg_Salary', ax=ax2, position=0, legend=False, width=0.25)

plt.grid(linestyle = '--')
plt.ylabel('Programming Language', labelpad=50, fontweight='bold')

ax.set_xlabel('Employees [%]', color='cornflowerblue')
ax.tick_params(axis='x', labelcolor='cornflowerblue')

ax2.set_xlabel('Average anual salary [$]', color='coral', labelpad=15)
ax2.tick_params(axis='x', labelcolor='coral')

if save:
    plt.savefig('Hotprog_sal.png',  bbox_inches='tight')

#%% Pie plot - Employee distribution

top = 5 #top 5

other = df_PL[:-top]['freq'].sum()

df_pie = pd.DataFrame(df_PL[len(df_PL)-top:])
df_pie.sort_values(by=['freq'], ascending=False, inplace=True)
df_other = pd.DataFrame({'PL':'Others' ,'freq':[other]})
df_pie = df_pie.append(df_other)

fig = plt.figure(figsize=(10.0, 10.0))
ax1 = fig.add_subplot(111)

explode = (0, 0, 0, 0, 0, 0.1)
patches, texts, autotexts = ax1.pie(df_pie['freq'], explode=explode, autopct='%1.1f%%', shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(20)

plt.legend(df_pie['PL'])
plt.title('Top-5 most common programming languages', fontweight='bold')

if save:
    plt.savefig('pie_employee_dist.png',  bbox_inches='tight')


#%% Cumulative percentage for average salary
#Useful for understand what is the industry average salary.

total = sum(df['Avg_Salary'])

sorted_sal = df.sort_values(by='Avg_Salary', ascending=True)

p_sal = sorted_sal['Avg_Salary']/total*100

cumperc_sal = []

for i in range(len(df)):
    cumperc_sal.append(p_sal[0:i+1].sum())
    
df_csal = pd.DataFrame({'cumperc':cumperc_sal,'Avg_Salary':sorted_sal['Avg_Salary']})

f = interpolate.interp1d(df_csal['cumperc'], df_csal['Avg_Salary'])

fig = plt.figure(figsize=(14.0, 8.0))
ax = fig.add_subplot(111)

plt.stackplot(df_csal['cumperc'], df_csal['Avg_Salary'], alpha=0.3, color='tab:blue')

x_interp = range(0,101,5)
plt.plot(x_interp, f(x_interp), color='red')

crit_points = [10,25,50,75,90]
plt.scatter(crit_points,f(crit_points), s=100, c='darkblue')

for i, txt in enumerate(f(crit_points)):
    ax.annotate('${:.0f}'.format(txt), (crit_points[i]-5, f(crit_points)[i]+5000),fontsize=20)

plt.grid(linestyle = '--')
plt.xlim([0,100])
plt.ylim(10000, 160000)

plt.ylabel('Average anual salary [$]', labelpad=10)
plt.title(' Average salary distribution', fontweight='bold')

plt.xticks(crit_points, ['Bottom 10%', 'Bottom 25%', 'Average (50%)', 'Top 25%', 'Top 10%'], fontsize=15)
plt.yticks(fontsize=15)

if save:
    plt.savefig('Cumul_avg_sal.png',  bbox_inches='tight')
