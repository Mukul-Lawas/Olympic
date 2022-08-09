import pandas as pd
import streamlit as st
import data_preprocessing as dp
import data_preporessing2 as dp2
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
noc_df = pd.read_csv('noc_regions.csv')

df = dp.preprocess(df,noc_df)

st.sidebar.title('Olympic Analysis')

user_menu = st.sidebar.radio('Select an Option',('Medal Tally','Overall Analysis','Country Wise Analysis','Athlete Wise Analysis'))

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')

    years,countries = dp2.year_country(df)
    year_selected = st.sidebar.selectbox('Years',years)
    country_selected = st.sidebar.selectbox('Country',countries)

    Medal_tally = dp2.fetch_medaltally(df,year_selected,country_selected)

    if year_selected == 'Overall' and country_selected == 'Overall':
        st.title("Overall Tally")
    if year_selected != 'Overall' and country_selected == 'Overall':
        st.title("Medal Tally in " + str(year_selected) + " Olympics")
    if year_selected == 'Overall' and country_selected != 'Overall':
        st.title(country_selected + " overall performance")
    if year_selected != 'Overall' and country_selected != 'Overall':
        st.title(country_selected + " performance in " + str(year_selected) + " Olympics")

    st.table(Medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Major Stats")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Hosts")
        st.title(cities)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Sports")
        st.title(sports)
    with col2:
        st.header("Events")
        st.title(events)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    countries_over_years = dp2.data_over_years(df,'region')
    fig = px.line(countries_over_years, x='Year', y='region')
    st.title("Participating Countries over the years")
    st.plotly_chart(fig)

    Events_over_years = dp2.data_over_years(df, 'Event')
    fig = px.line(Events_over_years, x='Year', y='Event')
    st.title("Events organized over the years")
    st.plotly_chart(fig)

    Athletes_over_years = dp2.data_over_years(df, 'Name')
    fig = px.line(Athletes_over_years, x='Year', y='Name')
    st.title("Athletes participated over the years")
    st.plotly_chart(fig)

    Sports_over_years = dp2.data_over_years(df, 'Sport')
    fig = px.line(Sports_over_years, x='Year', y='Sport')
    st.title("Sports played over the years")
    st.plotly_chart(fig)

    st.title("Most successful Athletes in the hystory of Olympics")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = dp2.most_successful(df, selected_sport)
    st.table(x)


if user_menu == 'Country Wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = dp2.yearwise_country_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    piv_tab = dp2.country_eventwise_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(piv_tab,annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = dp2.most_successful_Athlete_countrywise(df,selected_country)
    st.table(top10_df)


if user_menu == 'Athlete Wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age wrt medals")
    st.plotly_chart(fig)

    x = []
    name_sport = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name_sport.append(sport)

    fig = ff.create_distplot(x, name_sport, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)



    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = dp2.height_weight(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = dp2.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)