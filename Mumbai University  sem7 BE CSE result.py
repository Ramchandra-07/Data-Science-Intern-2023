# Importing libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from scipy.stats import scoreatpercentile


# load the data set and provide the path

df=pd.read_csv("C:/Users/ARCHANA/Desktop/Internship projects/MU result/result.csv")

df.fillna(method="ffill",inplace=True)  #Fill the null values

district_map = {'Mumbai':'Mumbai City', 'Kalyan': 'Thane', 'Panvel': 'Raigad',
                'Thane': 'Thane', 'Karjat': 'Raigad', 'Vasai': 'Palghar', 'Sangameshwar': 'Ratnagiri','Andheri' : 'Mumbai Suburbs', 'BORIVALI' : 'Mumbai Suburbs', 'Kankavli' : 'Sindhudurg',
                'Khed' : 'Pune', 'Shahapur' : 'Thane', 'Palghar' : 'Palghar', 'Tala' : 'Raigad',
                'Malvan': 'Sindhudurg', 'Uran': 'Raigad','Wada': 'Palghar',}

df['district'] = df['centre'].map(district_map)

df_obj= df.select_dtypes(['object'])
df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

my_districts = ['Mumbai City','Mumbai Suburbs','Palghar','Thane']
df = df[ (df['district'].isin(my_districts)) & (df['status'].isin(['Successful','Unsuccessful'])) & (df['year_of_admission'] == 2019)]


unwanted = ['prn','centre','clg_id','year_of_admission']
df.drop(unwanted, axis=1,inplace=True)

df.reset_index(drop=True,inplace=True)

title = 'Mumbai University B.E (comp) Semester Results '

df.head()


# plot unsuccessful candidates across the district

temp = pd.DataFrame(df.groupby(['district','status']).size(),columns=['count'])
temp.reset_index(inplace=True, level = ['district', 'status'])

fig = go.Figure()
fig.add_trace(go.Bar(
    x=temp['district'].unique().tolist(),
    y=temp[temp['status']=='Successful']['count'].tolist(),
    name='successful',
    marker_color='indianred',
    texttemplate="%{y}",
    textposition="outside"))
fig.add_trace(go.Bar(
    x=temp['district'].unique().tolist(),
    y=temp[temp['status']=='Unsuccessful']['count'].tolist(),
    name='unsuccessful',
    marker_color='lightsalmon',
    texttemplate="%{y}",
    textposition="outside"
))

fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.update_layout(title_text = title + '- Un/successful candidates per district')
fig.show()

# plot successful candidates by gender across the district
temp = pd.DataFrame(df[df['status'] == 'Successful'].groupby(['district', 'gender']).size(), columns=['count'])
temp.reset_index(inplace=True, level=['district', 'gender'])

fig = go.Figure()
fig.add_trace(go.Bar(
    x=temp['district'].unique().tolist(),
    y=temp[temp['gender'] == 'M']['count'].tolist(),
    name='male',
    marker_color='indianred',
    texttemplate="%{y}",
    textposition="outside"

))
fig.add_trace(go.Bar(
    x=temp['district'].unique().tolist(),
    y=temp[temp['gender'] == 'F']['count'].tolist(),
    name='female',
    marker_color='lightsalmon',
    texttemplate="%{y}",
    textposition="outside"

))
fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.update_layout(title_text= title + '- Successful candidates per gender per district')
fig.show()

# plot successful candidates per gender
temp = pd.DataFrame(df[df['status'] == 'Successful'].groupby('gender').size(),columns=['count'])
temp.reset_index(inplace=True, level = ['gender'])

# pull is given as a fraction of the pie radius
fig = go.Figure(data=[go.Pie(labels=temp['gender'], values=temp['count'], pull=[0.2, 0])])
fig.update_layout(title_text = title + '- Successful candidates per gender')
fig.show()

# plot Unsuccessful candidates per gender
temp = pd.DataFrame(df[df['status'] == 'Unsuccessful'].groupby('gender').size(),columns=['count'])
temp.reset_index(inplace=True, level = ['gender'])

# pull is given as a fraction of the pie radius
fig = go.Figure(data=[go.Pie(labels=temp['gender'], values=temp['count'], pull=[0.2, 0])])
fig.update_layout(title_text = title + '- Unsuccessful candidates per gender')
fig.show()

# plot heatmap for gradepoints vs sgpi of successful MALE candidates across all the districts
temp = df[(df['status'] == 'Successful') & (df['gender'] == 'M')].reset_index(drop=True)
fig = px.density_heatmap(temp, x="total_gradepoints", y="sgpi", nbinsx=20, nbinsy=20, color_continuous_scale="edge")
fig.update_layout(title_text = title + '- Successful male candidates gradepoints vs sgpi heatmap')
fig.show()

#Majority of the successful Male candidates in the specified district have sgpi between 8 & 8.49

# plot heatmap for gradepoints vs sgpi of successful MALE candidates across all the districts
temp = df[(df['status'] == 'Successful') & (df['gender'] == 'F')].reset_index(drop=True)
fig = px.density_heatmap(temp, x="total_gradepoints", y="sgpi", nbinsx=20, nbinsy=20, color_continuous_scale="edge")
fig.update_layout(title_text = title + '- Successful female candidates gradepoints vs sgpi heatmap')
fig.show()
#Majority of the successful Male candidates in the specified district have sgpi between 8.25 & 8.74

#plot percentile curve of successful male candidates
temp = df[(df['status'] == 'Successful') & (df['gender'] == 'M')].reset_index(drop=True)
a=list(range(1,101)) # precentile range
b = [scoreatpercentile(temp["sgpi"],i) for i in a]
temp2 = pd.DataFrame({'percentile': a, 'value': b}, columns=['percentile', 'value'])

# Create traces
fig = go.Figure()
fig.add_trace(go.Scatter(x=temp2['percentile'], y=temp2['value'],
                    mode='lines',
                    name='lines'))
fig.update_layout(title_text = title + '- Percentile curve of successful male candidates')
fig.show()

#plot percentile curve of successful female candidates
temp = df[(df['status'] == 'Successful') & (df['gender'] == 'F')].reset_index(drop=True)
a=list(range(1,101)) # precentile range
b = [scoreatpercentile(temp["sgpi"],i) for i in a]
temp2 = pd.DataFrame({'percentile': a, 'value': b}, columns=['percentile', 'value'])

# Create traces
fig = go.Figure()
fig.add_trace(go.Scatter(x=temp2['percentile'], y=temp2['value'],
                    mode='lines',
                    name='lines'))
fig.update_layout(title_text = title + '- Percentile curve of successful female candidates')
fig.show()





























