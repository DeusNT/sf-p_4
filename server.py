from bottle import route
from bottle import run
from bottle import request
from bottle import HTTPError

import DB_manager


@route("/albums/<artist>")
def find(artist):
    albums = DB_manager.find_album(artist)
    alb_count = len(albums)
    if alb_count != 0:
        if alb_count > 1:
            alb_word = "albums"
        else:
            alb_word = "album"
        result = "%s released %s %s:<br><br>" % (artist, alb_count, alb_word) + "<br>".join(albums)
        return result
    else:
        return HTTPError(400, "%s is not listed in the database" % artist)


@route("/albums", method="POST")
def add():
    year = request.forms.get("year")
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album = request.forms.get("album")
    if not (None in [year, artist, genre, album]):
        return DB_manager.add_album(year, artist, genre, album)
    else:
        return "Please, fill all attributes: year, artist, genre and album"


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)