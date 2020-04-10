import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_data = pd.read_csv("Certificate_data.csv")

course_data = pd.read_excel("CourseDetails.xlsx")

user_data = pd.read_excel("User_Data.xlsx")

total_data = pd.merge(df_data,user_data, on ='Email')

new_df = total_data
new_df = pd.merge(new_df,course_data, on ='Course')

rating_setting = new_df[['CourseID','Course','Curriculum Completion Percentage','Rate','UserID']]


rating_setting['Rate'] = np.where(rating_setting['Curriculum Completion Percentage'].between(80,100),5,rating_setting['Rate'])
rating_setting['Rate'] = np.where(rating_setting['Curriculum Completion Percentage'].between(60,79),4,rating_setting['Rate'])
rating_setting['Rate'] = np.where(rating_setting['Curriculum Completion Percentage'].between(40,59),3,rating_setting['Rate'])
rating_setting['Rate'] = np.where(rating_setting['Curriculum Completion Percentage'].between(20,39),2,rating_setting['Rate'])
rating_setting['Rate'] = np.where(rating_setting['Curriculum Completion Percentage'].between(0,19),1,rating_setting['Rate'])

new_df['Rate'] = rating_setting['Rate']

final_df = new_df.loc[:,['UserID','Name','Email','User Last Access','CourseID','Course','Rate','Curriculum Completion Percentage']]

final_df.isnull().sum(axis=0)

# replacing null values in the all columns with string 'unknown'
final_df['User Last Access'] = final_df['User Last Access'].replace(np.nan, 'unknown')
final_df['Rate'] = final_df['Rate'].replace(np.nan, '0')
final_df['Curriculum Completion Percentage'] = final_df['Curriculum Completion Percentage'].replace(np.nan, '0')


final_df.to_excel("Data_DF.xlsx", index= False)


