from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import plotly.express as px

app = Flask(__name__)
# Replace 'sqlite:///example.db' with your actual database connection string
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

# Define a simple model for demonstration purposes
class ExampleData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    column1 = db.Column(db.String(50))
    column2 = db.Column(db.Float)

# Create some sample data
db.create_all()
sample_data = [
    ExampleData(column1='A', column2=1.5),
    ExampleData(column1='B', column2=2.0),
    ExampleData(column1='C', column2=3.2),
]
db.session.bulk_save_objects(sample_data)
db.session.commit()

@app.route('/')
def index():
    # Fetch data from the database
    data = db.session.query(ExampleData.column1, ExampleData.column2).all()

    # Convert data to a Pandas DataFrame
    df = pd.DataFrame(data, columns=['column1', 'column2'])

    # Create a Plotly figure
    figure = create_plotly_figure(df)

    return render_template('index.html', plot=figure.to_html(full_html=False))

def create_plotly_figure(df):
    # Create a Plotly figure (scatter plot in this example)
    figure = px.scatter(df, x='column1', y='column2', title='Interactive Database Visualization')

    return figure

if __name__ == '__main__':
    app.run(debug=True)
