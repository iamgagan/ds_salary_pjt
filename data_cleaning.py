#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 12:34:02 2020

@author: gagan
"""


import pandas as pd

# reading the data
df =  pd.read_csv("glassdoor_data.csv")


# salary parsing
df = df[df['Salary Estimate'] != '-1']

salary = df['Salary Estimate'].apply(lambda x : x.split('(')[0])
minus_kd = salary.apply(lambda x : x.replace('K','').replace('$',''))

df['min_salary'] = minus_kd.apply(lambda x : int(x.split('-')[0]))
df['max_salary'] = minus_kd.apply(lambda x : int(x.split('-')[1]))

df['avg_salary'] = (df.min_salary + df.max_salary)/2


# company name text only

df['company text'] = df.apply(lambda x : x['Company Name'] if x['Rating']<0 else x['Company Name'][:-3],axis=1)


# state field

state=df['Location'].apply(lambda x : x.replace(" ",""))

state_nm= state.apply(lambda x : x.split(',')[1] if ',' in x else x)

df['job_state'] = state_nm

df['jh']=df['Headquarters'].apply(lambda x : x.replace(" ","").split(',')[1] if ',' in x else x)



df['j1']=df.apply(lambda x : x['jh'] if len(x['job_state']) > 3 else x['job_state'],axis=1)

df=df.drop(['job_state','jh'],axis=1)
df=df.rename({"j1":"job_state"},axis=1)

df['same_state']=df.apply(lambda x: 1 if x.Location==x.Headquarters else 0, axis=1)

#df['job_state'].value_counts()

# age of company

df['age']=df['Founded'].apply(lambda x : x if x<1 else 2020-x)

# parsing of job description( python, etc.)

#python
df['python_yn']=df['Job Description'].apply(lambda x : 1 if 'python' in x.lower() else 0)
#R
df['R_yn']=df['Job Description'].apply(lambda x : 1 if 'R' in x.lower() or 'r studio' 
                                       in x.lower() else 0)
#spark
df['spark_yn']=df['Job Description'].apply(lambda x : 1 if 'spark' in x.lower() else 0)
df.spark_yn.value_counts()
#aws
df['aws_yn']=df['Job Description'].apply(lambda x : 1 if 'aws' in x.lower() else 0)
df.aws_yn.value_counts()
#excel
df['excel_yn']=df['Job Description'].apply(lambda x : 1 if 'excel' in x.lower() else 0)
df.excel_yn.value_counts()


df_clean=df.copy()

df_clean.to_csv("clean_salary_data.csv",index=False)





