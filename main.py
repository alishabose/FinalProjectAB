
#set up APIs
#OpenLibrary & Spotify

def get_apis():

    #OpenLibrary API
    #working!
    openlibrary_baseurl = "https://openlibrary.org"

    #Spotify API
    #waiting on approval to create an app, then will get my secret & ID
    spotify_id = ""
    spotify_secret = ""
    spotify_token = authenticate_spotify(spotify_id, spotify_secret)

    return spotify_token, openlibrary_baseurl

#get book data from OpenLibrary with book title as user input
#nook title, cover, summary
#keywords from the summary

def get_book_data(book_title):

    url = "https://api.openlibrary.org/books/" + book_title
    response = requests.get(url)

    #write code to get the title, cover, and summary (JSON)
    return title, cover_url, summary

def extract_keywords(summary):
    #use summary from above for this function
    #create a list of important keywords from the summary

    return list(keywords)

#het songs from Spotify that match keywords
#filter songs based on genre

def get_songs(keywords, spotify_token):
    #hets songs on Spotify based on the keywoerds

    playlist = []
    for keyword in keywords:
        #call spotify URL
        #loop through tracks and find matching genres/keyword
        for track in tracks:
            #sorting feature
            playlist.append(track)
    return playlist

#create playlist with book cover and songs (8-10)

def create_playlist(book_data, playlist):

    #create a final playlist out of the book title, cover, and all the songs
    final_playlist = {
        title, cover, playlist
    }

    return final_playlist

#show playlist with HTML & CSS nicely

#uses flask like in our last assignment, design the page
#also not completely done yet

def css_playlist(final_playlist):
    from flask import Flask, render_template

    app = Flask(__name__)

    @app.route("/")
    def home():
        return render_template("base.html", playlist=final_playlist)

    app.run(debug=True)

def main():
    #create & authenticateAPIs
    openlibrary_base_url, spotify_token = get_apis()

    #get book data (title from user, data from API)
    book_title = input("Enter the title of the book: ")
    book_data = get_book_data(book_title)

    #get keywords
    keywords = extract_keywords(book_data["summary"])

    #get matching songs
    songs = get_songs(keywords, spotify_token)

    #get playlist
    playlist = create_playlist(book_data, songs)

    #create playlist
    css_playlist(playlist)