from datetime import datetime
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='Mass Layoffs',  layout='wide', initial_sidebar_state='auto')


st.title('Tech Companies Layoffs (2020-2023)')
st.caption("CS 448B Final Project | Xingshuo Xiao")
st.write("---")

# data
df = pd.read_csv('layoff_clean.csv', index_col=0)
df['date'] = pd.to_datetime(df['date'])
# sanity check - comment out for final work
# st.dataframe(data = df.head(10))

st.subheader("Overview")

st.write(
    """
    Since the onset of the COVID-19 pandemic, various companies have implemented layoffs as a cost-cutting measure.
    Even though the majority of the layoffs was reported in the U.S, the job cutoffs have also taken place in other countries.
    Although COVID-19 seems to be less of a significant threat now, unfortunately, layoffs persist. In this year, prominent
    tech companies including Google, LinkedIn, and Meta have laid off over 240,000 employees due to economic concerns.
    """
    )
st.write(" ")
st.write(" ")
st.write(" ")
date_range = st.slider('Select a time range',
                min_value = datetime(2020, 3, 11, 0, 0, 0),
                max_value = datetime(2023, 11, 3, 0, 0, 0),
                value = (datetime(2021, 6, 1, 0, 0, 0), datetime(2023, 1, 1, 0, 0, 0)), format = "YY-MM-DD")
df_date_range = df[(df['date'] >= date_range[0]) & (df['date'] <= date_range[1])]
df_date = df_date_range.loc[:, ['date', 'total_laid_off']].groupby(by = 'date', sort = False).sum().reset_index()
df_date = df_date.sort_values(['date']).reset_index()
overview1 = px.line(df_date, x = 'date', y='total_laid_off', markers = True,
                    labels = {'date': 'Date', 'total_laid_off': 'Number of Layoffs'})
overview1.update_traces(line_color = "#109618")
st.plotly_chart(overview1, use_container_width = True)

o1, o2 = st.columns([0.8, 0.2])
o2.write(" ")
o2.write(" ")
o2.write(" ")
o2.write('**Countries**')
countries_selection = o2.radio(
    "Select a country to compare with the U.S.",
    ["Canada", "China", "India", "Germany", "Netherlands", "UK"]
)


selected_countries = ['United States']
if countries_selection == "Canada": selected_countries.append('Canada')
if countries_selection == "China": selected_countries.append('China')
if countries_selection == "India": selected_countries.append('India')
if countries_selection == "Germany": selected_countries.append('Germany')
if countries_selection == "Netherlands": selected_countries.append('Netherlands')
if countries_selection == "UK": selected_countries.append('United Kingdom')

df_date_country = df_date_range[df_date_range["country"].isin(selected_countries)].loc[:, ['date', 'country', 'total_laid_off']]
df_date_country = df_date_country.groupby(by = ['date', 'country'], sort = False).sum().reset_index()
df_date_country = df_date_country.sort_values(['date']).reset_index()
overview2 = px.line(df_date_country, x = 'date', y = 'total_laid_off',
                    color = 'country', color_discrete_sequence=px.colors.qualitative.D3, markers = True,
                    labels = {'date': 'Date', 'total_laid_off': 'Number of Layoffs'})
o1.plotly_chart(overview2, use_container_width = True)
st.write("---")

st.subheader("Layoff Trends over Time")
st.write("""
        Layoffs across all industries began in 2020 due to the outbreak of COVID-19 pandemic when most places experienced
        lockdown. The companies need to cut off jobs in order to conquer the economic challenges raised by lockdown.
        Also, when lockdown started, most companies started to work from home (WFH). Some companies found it was not
        necessary to keep that many employees.
""")
st.write("""
        As the pandemic got better in late 2021, the restrictions loosened and the number of job cuts decreased.
        However, most companies still faced severe economic challenges due to the events such as Russia-Ukraine war.
        The inflation rate was still high and the international business was not yet back to normal as some countries like
        China were still enforcing strict pandemic restrictions.
        """)

st.write("""
        Until the end of the year of 2023, layoffs have remained across all industries.
        On Dec. 4, the music-streaming company Spotify announced its third round of layoffs due to the slow economic growth.
        According to the ongoing economic uncertainty, the downsizing trend in companies is expected to continue in 2024.
""")

df_year = df.loc[:, ['year', 'total_laid_off']].groupby(by = 'year').sum().reset_index()
df_year['year'] = df_year['year'].astype(str)
trend_year = px.bar(df_year, x='year', y='total_laid_off',
                    #color = 'total_laid_off', color_continuous_scale = px.colors.sequential.Viridis,
                    color = 'year', color_discrete_map = {'2020': 'steelblue', '2021': 'steelblue', '2022': 'orange', '2023': 'red'},
                    #color = 'year', color_discrete_map = {'2022': 'orange', '2023': 'red'},
                    text_auto=True,
                    labels = {'year': 'Year', 'total_laid_off': 'Number of Layoffs'},
                    title = "Number of layoffs from 2020 to 2023")
trend_year.update_traces(textfont_size = 12.5, textposition = "outside")
trend_year.update_xaxes(type='category')
trend_year.update_layout(showlegend=False)
st.plotly_chart(trend_year, use_container_width = True)
# st.write("---")


df_quarter = df.loc[:, ['quarter', 'total_laid_off']].groupby(by = 'quarter').sum().reset_index()
trend_quarter = px.bar(df_quarter, x = 'quarter', y = 'total_laid_off',
                        labels = {'quarter': 'Quarter', 'total_laid_off': 'Number of Layoffs'},
                        title = "Layoff trends by quarter")
st.plotly_chart(trend_quarter, use_container_width = True)
st.write("---")

st.subheader("Layoffs in Different Countries/Regions")
st.write(
    """
    The United States is not the only country affected by layoffs.
    Because the tech companies, especially the gaints including Google and Amazon, usually have offices overseas,
    when they thought of cut off jobs, they also cut off the ones in other countries.
    The Russian-Ukraine war has had a great impact on the economics in Europe. The high inflation rate leads to layoffs
    or hiring freezes in Europe.
    """
)
st.write(
    """
    The COVID-19 first started in Asia. However, it seems that layoffs did not really start in Asia until 2021.
    According to [8], many tech companies hired too many people during the pandemic to support the increasing
    demand in online services.
    As the COVID related restrictions lifted up gradually, the companies found they did not need that many employees.
    In Southeast Asia, the waves of layoffs began in 2021. The situations are different in China.
    China government had enforced a strict "zero-out" policy on COVID-19 since the start of the pandemic until almost
    the end of 2022. While it was quite effective controlling the spread of the pandemic, the international business in
    China had been frozen for a long time which resulted in mass layoffs in 2022.
    """
)
st.write("")
#g1, g2 = st.columns([0.75, 0.25])
region_selected = st.selectbox('Which region are you interested in?',
            ('World', 'Europe', 'Asia', 'Africa', 'North America', 'South America'))
#st.write("Here is a map - worldwide by default")
geo_df = df.loc[:, ['latitude', 'longitude', 'total_laid_off', 'location', 'country']].groupby(by=['latitude', 'longitude', 'location', 'country']).sum().reset_index()
#px.set_mapbox_access_token(open(".mapbox_token").read())
default_map = px.scatter_geo(df, lat = "latitude", lon = "longitude",
                            hover_name = 'location', size = 'total_laid_off',
                            projection = 'natural earth')
if region_selected == 'Europe':
    default_map.update_geos(scope = 'europe',showcountries = True, showframe = True)
elif region_selected == 'Asia':
    default_map.update_geos(scope = 'asia', showcountries = True, showframe = True)
elif region_selected == 'Africa':
    default_map.update_geos(scope = 'africa', showcountries = True, showframe = True)
elif region_selected == 'North America':
    default_map.update_geos(scope = 'north america', showcountries = True, showframe = True)
elif region_selected == 'South America':
    default_map.update_geos(scope = 'south america', showcountries = True, showframe = True)
else:
    default_map.update_geos(showcountries = True, showframe = True)
st.plotly_chart(default_map, use_contrainer_width = True)

st.write('**Check the countries with the most amount of layoffs**')
topN_countries = st.slider('The number of countries you want to check...', 3, 10, 5)
rank_geo_df = geo_df.loc[:, ['total_laid_off', 'country']].groupby('country').sum().reset_index()
rank_geo_df = rank_geo_df.sort_values(by = 'total_laid_off', ascending = False, ignore_index = True).reset_index()
rank_geo_df = rank_geo_df.loc[:topN_countries-1, :]
geo_bar = px.bar(rank_geo_df, x = 'country', y = 'total_laid_off', text_auto = True,
                labels = {'country': "Countries", "total_laid_off": "Number of Layoffs"})
st.plotly_chart(geo_bar, use_container_width = True)
st.write("---")

st.subheader("Layoffs in United States")
u1, u2 = st.columns([0.7, 0.3])
df_usa = df[df['country'] == 'United States'].reset_index()
#df_usa['year'] = df_usa['year'].astype(str)
df_company = df_usa.loc[:, ['company', 'total_laid_off']].groupby(['company']).sum().reset_index()
df_company = df_company.sort_values(by = 'total_laid_off', ascending = False, ignore_index=True).reset_index()
df_company_top10 = df_company.iloc[:10, :]
top10_companies = df_company_top10['company']
df_company_bar = df_usa[df_usa['company'].isin(top10_companies)].loc[:, ['company',
                        'industry', 'total_laid_off']].groupby(['company', 'industry']).sum().reset_index()
# others = df_usa[~df_usa['company'].isin(top10_companies)].loc[:, ['year', 'total_laid_off']].groupby('year').sum().reset_index()
top10_bar = px.bar(df_company_bar, x = 'company', y = 'total_laid_off',
                color = 'industry', color_discrete_sequence=px.colors.qualitative.D3,
                labels = {'company': "Company", "total_laid_off": "Number of Layoffs"},
                title = 'The top 10 companies with the most reported layoffs in the U.S.')
u1.plotly_chart(top10_bar, use_container_width = True)

u2.write("")
u2.write("")
u2.write("")
year_selection = u2.radio("Select a year to check the company with the most layoffs reported in the U.S.",
    [2020, 2021, 2022, 2023]
)
df_company_year = df_usa[df_usa['year'] == year_selection].loc[:, ['company', 'location', 'industry', 'total_laid_off']].groupby([
                        'company', 'location', 'industry']).sum().reset_index()
df_company_year = df_company_year.sort_values(by = 'total_laid_off', ascending = False, ignore_index=True).reset_index()
most_company_year = df_company_year.head(1)

if year_selection != 2020:
    last_year = df_usa[df_usa['year'] == year_selection - 1]
    last_year = last_year[last_year['company'] == most_company_year.loc[0, 'company']]
    last_year = last_year.loc[:, ['company', 'total_laid_off']].groupby('company').sum().reset_index()
else:
    last_year = []
metric_title = most_company_year.loc[0, 'company'] + " | " + most_company_year.loc[0, 'location'] + " | " + most_company_year.loc[0, 'industry']
if len(last_year) > 0:
    delta_val = (most_company_year.loc[0, 'total_laid_off'] - last_year.loc[0, 'total_laid_off']) / last_year.loc[0, 'total_laid_off']
    delta = str(delta_val*100)[:5] + '%'
    u2.metric(metric_title, value = int(most_company_year.loc[0, 'total_laid_off']), delta = delta)
else:
    u2.metric(metric_title, value = int(most_company_year.loc[0, 'total_laid_off']))

st.write("---")

st.subheader("Layoffs and Fund Raised")
st.write(
    """
    Some believed that layoffs were resulted from struggles in raising funds.
    When the companies had difficulties to raise money, they chose to carry out layoffs in order to cut off their spendings.
    However, many cases show that there is no significant correlation between a company's fundraising and their decisions to layoff.
    Some companies still announced layoffs when a large raise.
    """)

#st.write("number of layoffs vs fund raised -- scattered plot or line plot")
df_non_zero = df[df['total_laid_off'] > 0]
fund_scatter = px.scatter(df_non_zero, x = 'total_laid_off', y = 'funds_raised',
                            #trendline="ols",
                            #color = 'quarter',
                            hover_name="company", hover_data=["date", "total_laid_off","funds_raised"],
                            color_discrete_sequence=px.colors.qualitative.D3,
                            labels = {'total_laid_off': "Number of Layoffs", "funds_raised": "Amount of Funds Raised"}
                            #title = 'Number of layoffs vs. funds raised'
                            )
st.plotly_chart(fund_scatter, use_container_width = True)
st.write("---")

st.caption("Data Source: layoffs.fyi")
st.caption("Some companies did not report the exact number of layoffs in our dataset.")
st.write("---")
############################################################################################################
st.subheader("References")
st.markdown(
    """
    1.  https://www.businessinsider.com/layoffs-sweeping-the-us-these-are-the-companies-making-cuts-2023
    2.  https://www.kaggle.com/datasets/swaptr/layoffs-2022
    3.  https://layoffs.fyi/
    4.  https://mondo.com/insights/mass-layoffs-in-2022-whats-next-for-employees/
    5.  https://money.com/twitter-big-tech-companies-layoffs/
    6.  https://www.reuters.com/markets/europe/european-companies-cut-jobs-economy-sputters-2023-08-31/
    7.  https://www.reuters.com/markets/us/us-layoffs-jumped-november-led-by-retail-tech-report-shows-2023-12-07/
    8.  https://www.eastasiaforum.org/2023/01/13/southeast-asias-tech-take-off-and-layoffs/
    9.  https://www.statista.com/statistics/1127080/worldwide-tech-layoffs-covid-19-biggest/
    """
)

