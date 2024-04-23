from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import requests

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    location = request.form['location']
    term = request.form['term']
    api_key = "API_KEY"

    url = f"https://api.yelp.com/v3/businesses/search?location={location}&term={term}"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    
    if 'businesses' in data:
        restaurants = data['businesses']
        for restaurant in restaurants:
            restaurant['directions_link'] = f"https://www.google.com/maps/dir/{restaurant['location']['address1']}"
        return render_template('results.html', restaurants=restaurants)
    else:
        return render_template('no_results.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)