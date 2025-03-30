import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

# Load Data
import zipfile
##df = pd.read_csv('athlete_events.csv')
with zipfile.ZipFile("archive.zip", "r") as z:
    with z.open("athlete_events.csv") as file:
        df = pd.read_csv(file)
##region_df = pd.read_csv('noc_regions.csv')
with zipfile.ZipFile("archive.zip", "r") as z:
    with z.open("athlete_events.csv") as file:
        df = pd.read_csv(file)
    
    with z.open("noc_regions.csv") as file:
        region_df = pd.read_csv(file)

df = preprocessor.preprocess(df, region_df)

# Sidebar
st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)
    
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    st.title(f"{selected_country} Performance in {selected_year} Olympics" if selected_year != 'Overall' else f"{selected_country} Overall Performance")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    stats = {
        "Editions": df['Year'].nunique() - 1,
        "Hosts": df['City'].nunique(),
        "Sports": df['Sport'].nunique(),
        "Events": df['Event'].nunique(),
        "Athletes": df['Name'].nunique(),
        "Nations": df['region'].nunique()
    }
    
    st.title("Top Statistics")
    for idx, (key, value) in enumerate(stats.items()):
        st.metric(label=key, value=value)
    
    for category in ['region', 'Event', 'Name']:
        data_over_time = helper.data_over_time(df, category)
        fig = px.line(data_over_time, x="Year", y="Count", title=f"{category} over the years")
        st.plotly_chart(fig)
    
    st.title("No. of Events over time (Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    event_pivot = df.drop_duplicates(['Year', 'Sport', 'Event']).pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count')
    sns.heatmap(event_pivot.fillna(0).astype('int'), annot=True, ax=ax)
    st.pyplot(fig)
    
    st.title("Most Successful Athletes")
    selected_sport = st.selectbox('Select a Sport', sorted(['Overall'] + df['Sport'].unique().tolist()))
    st.table(helper.most_successful(df, selected_sport))

if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    selected_country = st.sidebar.selectbox('Select a Country', sorted(df['region'].dropna().unique().tolist()))
    
    st.title(f"{selected_country} Medal Tally over the years")
    st.plotly_chart(px.line(helper.yearwise_medal_tally(df, selected_country), x="Year", y="Medal"))
    
    st.title(f"{selected_country} Excels in the following sports")
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(helper.country_event_heatmap(df, selected_country), annot=True, ax=ax)
    st.pyplot(fig)
    
    st.title(f"Top 10 Athletes of {selected_country}")
    st.table(helper.most_successful_countrywise(df, selected_country))

if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    
    age_groups = [athlete_df['Age'].dropna()]
    labels = ['Overall Age']
    for medal in ['Gold', 'Silver', 'Bronze']:
        age_groups.append(athlete_df[athlete_df['Medal'] == medal]['Age'].dropna())
        labels.append(f'{medal} Medalist')
    
    st.title("Distribution of Age")
    st.plotly_chart(ff.create_distplot(age_groups, labels, show_hist=False, show_rug=False))
    
    st.title("Distribution of Age wrt Sports (Gold Medalists)")
    x, name = [], []
    for sport in [s for s in df['Sport'].unique() if s in ['Basketball', 'Judo', 'Football', 'Athletics']]:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)
    st.plotly_chart(ff.create_distplot(x, name, show_hist=False, show_rug=False))
    
    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sorted(['Overall'] + df['Sport'].unique().tolist()))
    fig, ax = plt.subplots()
    sns.scatterplot(data=helper.weight_v_height(df, selected_sport), x='Weight', y='Height', hue='Medal', style='Sex', ax=ax)
    st.pyplot(fig)
    
    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"], title="Male vs Female Participation")
    st.plotly_chart(fig)
