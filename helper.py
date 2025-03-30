import numpy as np
import pandas as pd

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall':
        temp_df = medal_df[medal_df['region'] == country]
    elif country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    else:
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]
    
    if country != 'Overall':
        x = temp_df.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().reset_index()
    else:
        x = temp_df.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().reset_index()
        x = x.sort_values('Gold', ascending=False)
    
    x['total'] = x[['Gold', 'Silver', 'Bronze']].sum(axis=1)
    return x.astype({'Gold': 'int', 'Silver': 'int', 'Bronze': 'int', 'total': 'int'})

def country_year_list(df):
    years = sorted(df['Year'].unique().tolist())
    years.insert(0, 'Overall')
    
    countries = sorted(df['region'].dropna().unique().tolist())
    countries.insert(0, 'Overall')
    
    return years, countries

def data_over_time(df, col):
    temp_df = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    temp_df.columns = ['Year', 'Count']
    return temp_df.sort_values(by='Year')

def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    
    x = temp_df['Name'].value_counts().reset_index().head(15)
    x.columns = ['Name', 'Medals']
    x = x.merge(df[['Name', 'Sport', 'region']], on='Name', how='left').drop_duplicates()
    return x[['Name', 'Medals', 'Sport', 'region']]

def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal']).drop_duplicates()
    new_df = temp_df[temp_df['region'] == country]
    return new_df.groupby('Year')['Medal'].count().reset_index()

def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal']).drop_duplicates()
    new_df = temp_df[temp_df['region'] == country]
    return new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)

def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    
    x = temp_df['Name'].value_counts().reset_index().head(10)
    x.columns = ['Name', 'Medals']
    x = x.merge(df[['Name', 'Sport']], on='Name', how='left').drop_duplicates()
    return x[['Name', 'Medals', 'Sport']]

def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region']).copy()
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    return athlete_df if sport == 'Overall' else athlete_df[athlete_df['Sport'] == sport]

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').size().reset_index(name='Male')
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').size().reset_index(name='Female')
    
    final = men.merge(women, on='Year', how='left').fillna(0)
    return final
