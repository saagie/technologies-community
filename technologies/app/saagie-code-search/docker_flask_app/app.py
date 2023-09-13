from flask import Flask, render_template, request
from utils import get_databases, get_results, load_model, load_codes_and_embeddings, get_functions_from_repo, encode_new_database
app = Flask(__name__)

# Get the list of previously saved databases
# databases = get_databases()

# Load the model and the databases
load_model()
load_codes_and_embeddings()

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get the list of previously saved databases
    databases = get_databases()

    if request.method == 'POST':
        query = request.form['query']
        selected_database = request.form['database']
        new_database = request.form.get('new-db', '')

        # If a new GitHub repository is provided
        if new_database:
            # Parse the GitHub repository to get all the Python functions inside
            functions, paths = get_functions_from_repo(new_database)
            # Encode those functions
            encode_new_database(new_database, functions, paths)
            # Update the list of databases
            load_codes_and_embeddings()
            databases = get_databases()


        # Get the search results
        results, path_results, similarities, colors = get_results(query, selected_database, databases, N=10)

        # Render the HTML page with the search results
        return render_template('results_v2.html', query=query, selected_database=selected_database, results=results, path_results=path_results, similarities=similarities, colors=colors, databases=databases)
    else:
        # Render the HTML page without search results (no query submitted yet)
        return render_template('results_v2.html', databases=databases)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')