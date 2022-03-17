from flask import Flask, render_template, url_for, redirect, request
import requests

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/")
def show_landing_page():
    return render_template("landing-page.html")


@app.route("/search", methods=['POST'])
def form_submit():
    user_query = request.form['search_query']  # matches name attribute of query string input (HTML)
    redirect_url = url_for('.search_imdb', query_string=user_query)  # match search_imdb function name (Python flask)
    return redirect(redirect_url)


@app.route("/search/<query_string>", methods=['GET'])
def search_imdb(query_string):
    API_KEY = 'INSERT_API_KEY_HERE'
    search_movies_url = f"https://imdb-api.com/en/API/SearchTitle/{API_KEY}/{query_string}"
    movie_metadata_url = f"https://imdb-api.com/en/API/Title/{API_KEY}/"

    try:
        search_movies_response = requests.get(search_movies_url)
        movie = search_movies_response.json()['results'][0]

        movie_info_response = requests.get(movie_metadata_url + movie['id'])
        
        return render_template(
            "search-result.html", 
            movie=movie,
            movie_info=movie_info_response.json()
        )
    except:
        return render_template("error404.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
