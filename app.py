import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

# read the imdb top 1000 movies file
movies = pd.read_csv('data/imdb_top_1000.csv')

# create a earnings column from gross by replacing all ,
movies['Earnings'] = movies['Gross'].str.replace(',', '')
movies = movies.astype({'Earnings': float})

# create a new column for year
movies['Year'] = movies['Released_Year']

# there's a stray PG value in the Year column, filter it out
movies['Year'] = movies[movies['Year'] != 'PG']['Year']

# drop null values from Year column
movies['Year'].dropna(inplace=True)

# group by year but retain it as a column (dont make it an index)
groupedMoviesList = movies.groupby('Year', as_index=False)

# get a average of the ratings per year
averageRatingByYear = groupedMoviesList.mean()

# create a line chart out of it
fig = px.line(
    averageRatingByYear,
    x="Year",
    y="IMDB_Rating",
    title='Average movie rating by year (hover to see average earnings)',
    hover_data=["Earnings"])

# Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Average ratings by year"

# Set up the layout
app.layout = html.Div(children=[
    html.H1("Assignment 5 - Sage DS "),
    dcc.Graph(
        id='assignment5',
        figure=fig
    ),
    html.A('Code on Github', href="https://github.com/pinaki-das-sage/assignment5"),
    html.A('Data source', href="https://www.kaggle.com/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows"),
]
)

if __name__ == '__main__':
    app.run_server()
