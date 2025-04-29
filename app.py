from flask import Flask, render_template, request, redirect
import pandas as pd
import csv
import os

app = Flask(__name__)

# --- Load the Spotify CSV Data ---
csv_path = "spotify.csv"
try:
    df = pd.read_csv(csv_path)
    df.rename(columns={'track_name': 'name', 'artists': 'artist', 'track_genre': 'genre'}, inplace=True)
except Exception as e:
    print(f"❌ Error loading Spotify CSV: {e}")
    df = pd.DataFrame()  # Fallback empty DataFrame

# --- Home/Login Route ---
@app.route('/')
def home():
    return render_template('login.html')

# --- Handle Login Form Submission ---
@app.route('/login', methods=['POST'])
def login():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    # Save user info to users.csv
    user_file = 'users.csv'
    file_exists = os.path.isfile(user_file)

    with open(user_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Name', 'Email', 'Phone'])  # Header
        writer.writerow([name, email, phone])

    return redirect('/main')

# --- Main Page (Recommendation UI) ---
@app.route('/main')
def main():
    return render_template('index.html')

# --- Song Search API ---
@app.route('/search', methods=['GET'])
def search_songs():
    artist = request.args.get('artist', '').strip().lower()
    genre = request.args.get('genre', '').strip().lower()

    filtered_df = df.copy()

    if artist:
        filtered_df = filtered_df[filtered_df['artist'].str.lower().str.contains(artist, na=False)]
    if genre:
        filtered_df = filtered_df[filtered_df['genre'].str.lower().str.contains(genre, na=False)]

    if filtered_df.empty:
        return {'message': 'No matching songs found.'}

    if 'popularity' in filtered_df.columns:
        filtered_df = filtered_df.sort_values(by="popularity", ascending=False)

    results = filtered_df[['name', 'artist', 'genre', 'popularity']].to_dict(orient="records")
    return results

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True)




