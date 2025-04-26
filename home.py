import requests
import urllib.parse
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("search.html")

# @app.route("/search")
# def search():
#     query = request.args.get("q")
#     if not query:
#         return "Query cannot be empty", 400

#     # Encode the user query to safely pass in URL
#     encoded_query = urllib.parse.quote(f"id_category_title_published_author:{query}")

#     solr_url = f"http://localhost:8983/solr/lab11_task1/select?q={encoded_query}&q.op=OR&wt=json"

#     response = requests.get(solr_url)

#     if response.status_code != 200:
#         return f"Error querying Solr: {response.status_code}<br><br>{response.text}", 500

#     try:
#         docs = response.json().get("response", {}).get("docs", [])
#     except requests.exceptions.JSONDecodeError:
#         return f"Invalid JSON returned by Solr:<br><br>{response.text}", 500

#     return render_template("search_results.html", results=docs)




# @app.route('/search')
# def search():
#     query = request.args.get('q')
    
#     # Construct Solr URL
#     # http://localhost:8984/solr/lab11_task1/select?indent=true&q.op=OR&q=*%3A*
#     # solr_url = f'http://localhost:8984/solr/lab11_task1/select?q={query}'
#     # http://localhost:8984/solr/lab11_task1/select?indent=true&q.op=OR&q=category%3Ajava
#     # solr_url = f'http://localhost:8984/solr/lab11_task1/select?indent=true&q.op=OR&q=*%3A'
#     solr_url = f'http://localhost:8984/solr/lab11_task1/select?q={query}'
#     print(solr_url)

#     try:
#         response = requests.get(solr_url)
#         response.raise_for_status()  # Check for request errors
#         solr_data = response.json()
#         print(solr_data)
#         docs = solr_data.get("response", {}).get("docs", [])
#     except Exception as e:
#         print(f"Error querying Solr: {e}")
#         docs = []
    
#     return render_template('search_results.html', results=docs)

@app.route('/search')
def search():
    query = request.args.get('q')
    
    # Construct Solr URL
    solr_url = f'http://localhost:8984/solr/lab11_task1/select?q={query}'
    
    try:
        response = requests.get(solr_url)
        response.raise_for_status()  # Check for request errors
        solr_data = response.json()
        docs = solr_data.get("response", {}).get("docs", [])
        
        # Parse the results, extract the first element from lists
        for doc in docs:
            doc['category'] = doc.get('category', [])[0] if doc.get('category') else 'Unknown'
            doc['title'] = doc.get('title', [])[0] if doc.get('title') else 'No Title'
            doc['author'] = doc.get('author', [])[0] if doc.get('author') else 'Unknown'
        
    except Exception as e:
        print(f"Error querying Solr: {e}")
        docs = []
    
    return render_template('search_results.html', results=docs)
