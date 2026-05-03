import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories,cutoff):
    categorical_map={}
    for i in range(len(categories)):
        if categories.values[i]>= cutoff:
            categorical_map[categories.index[i]]=categories.index[i]
        else:
            categorical_map[categories.index[i]]='Other'
    return  categorical_map      
           
def clean_experience(x):        #cleaning
    if x=='More than 50 years':
        return 50
    if x=='Less than 1 year':
        return 0.5
    return float(x)       #flaot is used to convert the values which are in string to float (numeric) values


def clean_eductaion(x):         # as we are having multiple string values of ed_level so we are taking only those which are important 
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelor'

  # as there is no need to again and again run the below script as streamlit will cache it and run automatically when it is called
def load_data():
    df=pd.read_csv("survey_results_public.csv")
    df=df[["Country","EdLevel","YearsCodePro","Employment","ConvertedComp"]] #keeping only selected columns from 
    df=df.rename({"ConvertedComp":"Salary"},axis=1)
    df=df[df["Salary"].notnull()]
    df=df.dropna()
    df=df[df["Employment"]=="Employed full-time"]
    df=df.drop("Employment",axis=1)
    
    country_map=shorten_categories(df.Country.value_counts(),400)
    df['Country']=df['Country'].map(country_map)
    df=df[df["Salary"]<=250000] # keeps rows with Salary ≤ 250000

    df=df[df["Salary"] >= 10000] #keeps rows with Salary ≥ 10000

    df=df[df['Country']!='Other']#removes rows where Country is "Others"
    df["YearsCodePro"]=df["YearsCodePro"].apply(clean_experience)
    df['EdLevel']=df['EdLevel'].apply(clean_eductaion)
    return df

df=load_data()

def display_explore_page():
    st.title("Explore Software Engineer Salaries")
    st.write(
        """
    ### Stack Overflow Developer Survey 2020
    
    """   
        
    )
    
    data=df["Country"].value_counts()
    
    fig1,ax1=plt.subplots()
    ax1.pie(data,labels=data.index,autopct="1.1f%%",shadow=True,startangle=90)
    ax1.axis("equal") #equal aspect ratio ensures that pie is drawn as a circle
    
    st.write ("""#### Number of Data From Differnet Countries """)
    
    st.pyplot(fig1)
    
    st.write(
        """
        ### Mean Salary Based On Country
        """
        
    )
    
    data=df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)
    
    st.write(
        """
        ### Mean Salary Based On Experience
        """
        
    )
    
    data=df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)
    