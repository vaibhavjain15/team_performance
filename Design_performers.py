
# coding: utf-8

# In[20]:

import glob
import pandas as pd
from datetime import timedelta as dt
import matplotlib.pyplot as plt
import numpy as np
from numpy import arange


# In[21]:

path =r'C:\Users\HP\Desktop'
filenames = glob.glob(path + "/*.xls")


# In[22]:

dfs = []
for filename in filenames:
    dfs.append(pd.read_excel(filename, encoding='utf-8'))



# In[23]:

df = dfs[0]
print(df.columns)    #cloumns inside in dataframe
l= len(df)
print(l)


# In[24]:

df_new = df.drop(df.columns[[4, 5, 9, 10, 11, 12, 13, 14, 15 ,16]], axis=1)
df_new['Task Start'] =  [d.date() for d in df_new['Task Start']]
#print(df_new['Task Start'])
df_new['Task End'] = [d.date() for d in df_new['Task End']]
#print(df_new['Task End'])
df_new['SLA Days'] = df_new['Task End'] - df_new['Task Start']
df_new['SLA Days'] = [int(i.days) for i in df_new['SLA Days']] 
#print(df_new['SLA Days'])


# In[25]:

a = df_new['Task Name'].value_counts()

b = [a[0], a[1], a[2]]
num_cols = ["PostGroomsInventoryMgmt", "CompleteDesign", "PreDesign"]
bar_heights = b
bar_positions = arange(3) + 1
tick_positions = range(1,4)
fig, ax = plt.subplots()

ax.bar(bar_positions, bar_heights, 0.5)
ax.set_xticks(tick_positions)
ax.set_xticklabels(num_cols)

ax.set_xlabel('Design Tasks')
ax.set_ylabel('No Of Tasks Closed')
ax.set_title('Total Design Tasks closed(2016)')
plt.show()

#outcome
#PostGroomsInventoryMgmt    17767
#CompleteDesign              6937
#PreDesign                   5494


# In[26]:

#***Classification on the basis of pre-design**
df_pre_design = df_new[df_new['Task Name'] == 'PreDesign']
types_of_projects = df_pre_design['Project Name'].value_counts()
no_of_performers = df_pre_design['Performer'].value_counts()
#print(no_of_performers)   #total pre-design tasks have been closed by performer in 2016
#print(types_of_projects)
#print(df_pre_design['Performer']).


# In[27]:

offshore_performer = ['gupta.diksha','umarye.rujuta', 'bhatnagar.pankhuri', 'rai.arpit','gupta.ruhi','balasundaram.vishwar','mahajan.ishita','a.marshell', 'valli.vaishnavee', 'badhe.shashikant', 'chunduri.sreeharsha', 'meher.shalini', 'vyas.sanket', 'jain.vaibhav', 'rajendiran.bharani', 'auti.swati', 'palanisamy.senthil', 'pandit.subodh']
#df_pre_design = df_pre_design[df_pre_design['Performer'] == x for x in offshore_performer]

df_pre_design = df_pre_design[df_pre_design['Performer'].isin(offshore_performer)]
a1 = df_pre_design['Performer'].value_counts()  #total projects closed per offshore designer
bar_heights = []
for i in range(0,len(offshore_performer)):
    bar_heights.append(a1[i])
print(bar_heights)    
bar_positions = arange(18) + 1
tick_positions = range(1,19)
fig, ax1 = plt.subplots()
ax1.bar(bar_positions, bar_heights, 0.5)
ax1.set_xticks(tick_positions)
ax1.set_xticklabels(a1.index, rotation=90)
ax1.set_xlabel('offshore_performer')
ax1.set_ylabel('No Of Projects Closed')
ax1.set_title('Project Pre-design Closed by Offshore in 2016')
plt.show()

no_of_offshore_deisgners = df_pre_design['Performer'].unique()
print(df_pre_design.columns)
Pre_design_closed_within_SLA = df_pre_design[df_pre_design['SLA Days'] < 7]
#print(Pre_design_closed_within_SLA)
Pre_design_not_closed_within_SLA = df_pre_design[df_pre_design['SLA Days'] > 6]
#print(Pre_design_not_closed_within_SLA)     #There are projects which were having jeops/exceptions due to issues
plt.plot(Pre_design_closed_within_SLA['Project CL Cnt'])
plt.xlabel('Pre_design(CLs)_closed_within_SLA')
plt.show()
plt.plot(Pre_design_not_closed_within_SLA['Project CL Cnt'] )
plt.xlabel('Pre_design(CLs)_not_closed_within_SLA')
plt.show()
performer_closed_within_SLA = Pre_design_closed_within_SLA['Performer'].value_counts()
performer_didnt_close_within_SLA = Pre_design_not_closed_within_SLA['Performer'].value_counts()
#print(performer_closed_within_SLA)
#print(performer_didnt_close_within_SLA)


# In[28]:

#our aim is here to find the projects where it takes much time and analyse on which types of projects we need more focus
#we are taking first list of top_6 offshore folks who had closed most of projects after 6 days 
#since there are total 18 offshore designers we have taken so we will distribute them on the basis of max projects closed within SLA and not closed within SLA

#performer closed(c) within SLA i.e. before 7 days
top_6_c = performer_closed_within_SLA[:6]    
med_6_c = performer_closed_within_SLA[6:12]
last_6_c = performer_closed_within_SLA[12:18]

#performer not closed(nc) within SLA i.e. closed after 6 days
top_6_nc = performer_didnt_close_within_SLA[:6]    
med_6_nc = performer_didnt_close_within_SLA[6:12]
last_6_nc = performer_didnt_close_within_SLA[12:18]
print(top_6_nc)
top_6_Pre_design_not_closed_within_SLA = Pre_design_not_closed_within_SLA[Pre_design_not_closed_within_SLA['Performer'].isin(top_6_nc.index)]
top_6_Pre_design_not_closed_within_SLA = top_6_Pre_design_not_closed_within_SLA.fillna(0)
#print(top_6_Pre_design_not_closed_within_SLA['Project CL Cnt'])
med_6_Pre_design_not_closed_within_SLA = Pre_design_not_closed_within_SLA[Pre_design_not_closed_within_SLA['Performer'].isin(med_6_nc.index)]
med_6_Pre_design_not_closed_within_SLA = med_6_Pre_design_not_closed_within_SLA.fillna(0)
last_6_Pre_design_not_closed_within_SLA = Pre_design_not_closed_within_SLA[Pre_design_not_closed_within_SLA['Performer'].isin(last_6_nc.index)]
last_6_Pre_design_not_closed_within_SLA = last_6_Pre_design_not_closed_within_SLA.fillna(0)
#print(med_6_Pre_design_not_closed_within_SLA['Project Name'].unique())

project_types = {"PMD", "EarthLink Re-Assign", "NNI", "Hub", "Mileage Reduction", "SWITCHED", "LSEF", "HSEF", "Retraction", "ILEC", "site"}
a2 = {}    #performers in max_projects_in_top_6_nc have been distributed on the basis of project type. 
a3 = {}    #performers in max_projects_in_med_6_nc have been distributed on the basis of project type.
a4 = {}    #performers in max_projects_in_last_6_nc have been distributed on the basis of project type.
for i in project_types:
    a2[i] = top_6_Pre_design_not_closed_within_SLA[top_6_Pre_design_not_closed_within_SLA['Project Name'].str.contains(i)]
    a3[i] = med_6_Pre_design_not_closed_within_SLA[med_6_Pre_design_not_closed_within_SLA['Project Name'].str.contains(i)]
    a4[i] = last_6_Pre_design_not_closed_within_SLA[last_6_Pre_design_not_closed_within_SLA['Project Name'].str.contains(i)]


max_CLs_project_types_top_6_nc = {}
max_CLs_project_types_med_6_nc = {}
max_CLs_project_types_last_6_nc = {}
for i in a2:
    max_CLs_project_types_top_6_nc[i] = sum(a2[i]['Project CL Cnt'])
    max_CLs_project_types_med_6_nc[i] = sum(a3[i]['Project CL Cnt'])
    max_CLs_project_types_last_6_nc[i] = sum(a4[i]['Project CL Cnt'])
    
print(max_CLs_project_types_top_6_nc)
print(max_CLs_project_types_med_6_nc)
print(max_CLs_project_types_last_6_nc)


# In[29]:


plt.bar(range(len(max_CLs_project_types_top_6_nc)), max_CLs_project_types_top_6_nc.values(), align='center', color='green')
plt.xticks(range(len(max_CLs_project_types_top_6_nc)), max_CLs_project_types_top_6_nc.keys(), rotation=90)
plt.xlabel("Project Types")
plt.ylabel("Project CL Count(no of circuits)")
plt.title("Max_CLs_project_types_top_6_nc")
plt.show()

plt.bar(range(len(max_CLs_project_types_med_6_nc)), max_CLs_project_types_med_6_nc.values(), align='center')
plt.xticks(range(len(max_CLs_project_types_med_6_nc)), max_CLs_project_types_med_6_nc.keys(), rotation=90)
plt.xlabel("Project Types")
plt.ylabel("Project CL Count(no of circuits)")
plt.title("Max_CLs_project_types_med_6_nc")
plt.show()


plt.bar(range(len(max_CLs_project_types_last_6_nc)), max_CLs_project_types_last_6_nc.values(), align='center', color='red')
plt.xticks(range(len(max_CLs_project_types_last_6_nc)), max_CLs_project_types_last_6_nc.keys(), rotation=90)
plt.xlabel("Project Types")
plt.ylabel("Project CL Count(no of circuits)")
plt.title("Max_CLs_project_types_last_6_nc")
plt.show()

#ax1.bar(bar_positions, bar_heights_1, 0.5)
#ax1.set_xticks(tick_positions)
#ax1.set_xticklabels(, rotation=90)
#ax1.set_xlabel('offshore_performer')
#ax1.set_ylabel('No Of Projects Closed')
#ax1.set_title('Project Pre-design Closed by Offshore in 2016')
#plt.show()


# looks like we need to work on project types NNI, LSEF, Hub Consolidation & Mileage Reduction mainly to find out reasons and performers to put more effort.
# 
# 

# In[30]:


#looks like we need to work on project types NNI, LSEF, Hub Consolidation & Mileage Reduction mainly to find out reasons and performers to put more effort.###so far we have analysed that we need to focus more on project types NNI, LSEF consolidation, Mileage Reduction(bit) & Hub Consolidation###

##now lets find out performers in each of project types to know who should take care the most##

NNI_projects = Pre_design_not_closed_within_SLA[Pre_design_not_closed_within_SLA['Project Name'].str.contains("NNI")]
performers_NNI_projects = NNI_projects['Performer'].value_counts()

plt.bar(range(len(performers_NNI_projects)), performers_NNI_projects.values, align='center', color='purple')
plt.xticks(range(len(performers_NNI_projects)), performers_NNI_projects.index, rotation=90)
plt.title("Performers for NNI Consolidation project type")
plt.xlabel("Performers")
plt.ylabel("No Of Projects")
plt.show()


# In[31]:

### LSEF consolidation###
LSEF_projects = Pre_design_not_closed_within_SLA[Pre_design_not_closed_within_SLA['Project Name'].str.contains("LSEF")]
performers_LSEF_projects = LSEF_projects['Performer'].value_counts()

plt.bar(range(len(performers_LSEF_projects)), performers_LSEF_projects.values, align='center', color='green')
plt.xticks(range(len(performers_LSEF_projects)), performers_LSEF_projects.index, rotation=90)
plt.title("Performers for LSEF Consolidation project type")
plt.xlabel("Performers")
plt.ylabel("No Of Projects")
plt.show()


# In[32]:

###Mileage Reduction

Mileage_Reduction_projects = Pre_design_not_closed_within_SLA[Pre_design_not_closed_within_SLA['Project Name'].str.contains("Mileage Reduction")]
performers_Mileage_Reduction_projects = Mileage_Reduction_projects['Performer'].value_counts()

plt.bar(range(len(performers_Mileage_Reduction_projects)), performers_Mileage_Reduction_projects.values, align='center', color='blue')
plt.xticks(range(len(performers_Mileage_Reduction_projects)), performers_Mileage_Reduction_projects.index, rotation=90)
plt.title("Performers for Mileage_Reduction project type")
plt.xlabel("Performers")
plt.ylabel("No Of Projects")
plt.show()


# In[33]:

###Hub Consolidaton

Hub_projects = Pre_design_not_closed_within_SLA[Pre_design_not_closed_within_SLA['Project Name'].str.contains("Hub")]
performers_Hub_projects = Hub_projects['Performer'].value_counts()

plt.bar(range(len(performers_Hub_projects)), performers_Hub_projects.values, align='center', color='orange')
plt.xticks(range(len(performers_Hub_projects)), performers_Hub_projects.index, rotation=90)
plt.title("Performers for Hub Consolidation project type")
plt.xlabel("Performers")
plt.ylabel("No Of Projects")
plt.show()


# In[41]:

#from above 4 graphs we can say that in each types of projects there are different performers who need to work
#NNI - arpit & Bharani needs improvement 
#LSEF - swat,ishita,ruhi & vishwa needs improvement
#Mileage Reduction - Bharani & Sree Harsha needs improvement
#HUB - swati & Vishwa needs improvement

#offshore_performer = ['gupta.diksha','umarye.rujuta', 'bhatnagar.pankhuri', 'rai.arpit','gupta.ruhi','balasundaram.vishwar','mahajan.ishita','a.marshell', 'valli.vaishnavee', 'badhe.shashikant', 'chunduri.sreeharsha', 'meher.shalini', 'vyas.sanket',
#'jain.vaibhav', 'rajendiran.bharani', 'auti.swati', 'palanisamy.senthil', 'pandit.subodh']
designers = {}

for i in offshore_performer:
    designers[i] = Pre_design_not_closed_within_SLA[Pre_design_not_closed_within_SLA['Performer'].str.contains(i)]
    
#print(designers.items())
## to find individual designers performance as per project types
d1 = {}
#d = 0 

def find_project(a):
    d = {}
    for j in project_types:
        b = a['Project Name'].str.contains(j)
        d[j] = a[b]['Project Name'].count()
    return d

for i in designers: 
    d1 = find_project(designers[i])
    plt.bar(range(len(d1)), d1.values(), align='center', color='red')
    plt.xticks(range(len(d1)), d1.keys(), rotation=90)
    plt.xlabel("Project Types")
    plt.ylabel("No Of Projects")
    plt.title(i)
    plt.show()
    #print(d1)




# Here we can see individual performance and their capability in 2016. we have seen in analysis where they need improvement and in some area where we can work more. 

# In[81]:

#Finally we have checked individuals capability in last year.
#How many projects they havent worked on yet. 

total_project_types = {}
avg_project_types = {}
for i in project_types:
    total_project_types[i] = Pre_design_not_closed_within_SLA[Pre_design_not_closed_within_SLA['Project Name'].str.contains(i)]
    avg_project_types[i] = np.mean(total_project_types[i]['Project CL Cnt'])

print(avg_project_types)    
def average(a):
    d = {}
    for j in project_types:
        b = a['Project Name'].str.contains(j)
        #print(a[b]['Project CL Cnt'])
        d[j] = np.mean(a[b]['Project CL Cnt'])
    return d

for i in designers:
    d2 = average(designers[i])
    print(d2.keys())
    gridnumber = range(1,2)
    b1 = plt.bar(range(len(d2)), d2.values(), width=0.4, label="Individual projects closed(not within SLA)", align="center")
    b2 = plt.bar(range(len(d2)), avg_project_types.values(), color="red", width=0.4, label="Average projects closed(not within SLA)", align="center")
    plt.ylim([0,10])
    plt.xlim([0,11])
    plt.xlabel("Project Types")
    plt.ylabel("Average projects closed(not within SLA)")
    plt.title(i)
    plt.xticks(range(len(d2)), d1.keys(), rotation=90)
    plt.legend()
    plt.show()



# In[ ]:




# In[ ]:



