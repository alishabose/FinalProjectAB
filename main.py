import requests
from flask import Flask, render_template, request, session, redirect
from key import LASTFM_API_KEY, secret_key

# My LAST FM KEY
LASTFM_API_URL = "http://ws.audioscrobbler.com/2.0/"
LASTFM_API_KEY = LASTFM_API_KEY

# MY OPENLIB URL
OPENLIBRARY_API_URL = "https://openlibrary.org/search.json"
app = Flask(__name__)

# MY FLASK SESSION KEY
app.secret_key = secret_key # REPLACE WITH FLASK KEY (ANY NUMBERS WORK)

def search_lastfm(query):

    url = f"{LASTFM_API_URL}?method=track.search&track={query}&api_key={LASTFM_API_KEY}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        tracks = response.json()['results']['trackmatches']['track']

        # MAKING SURE TRACK EXISTS
        valid_tracks = []
        for track in tracks:
            if 'url' in track and track['url'] != '':
                valid_tracks.append(track)
        return valid_tracks
    else:
        return []


def collect_songs_by_genre(keywords, max_songs):
    collected_songs = []
    seen_songs = set()

    while len(collected_songs) < max_songs and keywords:
        for keyword in keywords:
            if len(collected_songs) >= max_songs:
                break

            print(f"Searching for tracks related to: {keyword}")
            tracks = search_lastfm(keyword)

            # FILTERS OUT PODCASTS, SHOWS, ETC. (NOT EXHAUSTIVE LIST)
            if tracks:
                for track in tracks:
                    track_info = (track['name'], track['artist'])
                    if (track_info not in seen_songs and
                            "episode" not in track['name'].lower() and
                            "podcast" not in track['name'].lower() and
                            "ep" not in track['name'].lower() and
                            "chapter" not in track['name'].lower() and
                            "comic" not in track['name'].lower() and
                            "audiobook" not in track['name'].lower() and
                            "narrative" not in track['name'].lower() and
                            "dialogue" not in track['name'].lower() and
                            "story" not in track['name'].lower() and
                            "lecture" not in track['name'].lower() and
                            "newspaper" not in track['name'].lower() and
                            "show" not in track['name'].lower() and
                            "soundtrack" not in track['name'].lower()):
                        seen_songs.add(track_info)
                        collected_songs.append({
                            "name": track['name'],
                            "artist": track['artist'],
                            "url": track.get('url', 'No URL available')
                        })
                        break
            else:
                print(f"No tracks found for {keyword}.")

    return collected_songs


def get_book_details(book_title):

    query = book_title.lower().replace(' ', '+')
    url = f"{OPENLIBRARY_API_URL}?q={query}"

    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            books = data.get('docs', [])

            if books:
                book = books[0]
                title = book.get('title', 'No title found')
                author = book.get('author_name', ['Unknown author'])[0]
                cover_id = book.get('cover_i', None)
                cover_url = f'https://covers.openlibrary.org/b/id/{cover_id}-L.jpg' if cover_id else None
                summary = book.get('description', 'No description available')
                subjects = book.get('subject', [])
                return {
                    'title': title,
                    'author': author,
                    'cover_url': cover_url,
                    'summary': summary,
                    'subjects': subjects
                }
            else:
                return None
        except Exception as e:
            print(f"Error getting book details, so sorry: {e}")
            return None
    else:
        return None


def create_playlist_for_book(book_title, max_songs=15):

    book_details = get_book_details(book_title)
    if book_details:
        subjects = book_details['subjects']

        playlist = collect_songs_by_genre(subjects, max_songs)

        return book_details, playlist
    else:
        return None, None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        book_title = request.form['book_title']
        book_details, playlist = create_playlist_for_book(book_title, max_songs=15)

        if book_details:
            session['book_details'] = book_details
            session['playlist'] = playlist
            return render_template('confirm_book.html', book_details=book_details)
        else:
            return render_template('index.html', error="No book found with that title.")

    return render_template('index.html')

# THIS IS IN CASE THE USER PICKS THE WRONG BOOK/WRONG RESULT
@app.route('/confirm', methods=['POST'])
def confirm_book():
    if 'confirm' in request.form:
        return render_template('playlist.html', book_details=session['book_details'], playlist=session['playlist'])
    elif 'go_back' in request.form:
        return redirect('/')


@app.route('/playlist', methods=['POST'])
def playlist():
    if 'book_details' in session and 'playlist' in session:
        book_details = session['book_details']
        playlist = session['playlist']
        return render_template('playlist.html', book_details=book_details, playlist=playlist)
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
