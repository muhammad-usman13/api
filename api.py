from flask import Flask, request, jsonify
import pandas as pd
app = Flask(__name__)

def load_data():
    try:
        df = pd.read_csv('data_new.csv', encoding='utf-8')
        return df
    except FileNotFoundError:
        return None
    
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the API!', 'endpoints': ['/search?query={query}']})


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')

    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    df = load_data()

    if df is None:
        return jsonify({'error': 'CSV file not found'}), 404

    results = df[df['title'].str.contains(query, case=False)]    
    data = {'results': results.to_dict(orient='records')}

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
