from bottle import route, run, HTTPError, request
import album

RESOURCES_PATH = "users/"

@route("/")
def hellow():
    return print("Hellow, User!")

@route("/albums/<artist>")
def get_artist(artist):
    albums_list = album.find(artist)
    if not albums_list:
        answer = f"Альбмов {artist} нет в базе данных"
        result = HTTPError(404, answer)
    else:
        album_names = [album.album for album in albums_list]
        result = f"Список альбомов {artist}\n"
        result += "\n".join(album_names)
    return result


@route("/albums/", method="POST")
def create_album():
    year = request.forms.get("year")
    artist = request.forms.get("artist")
    genre = request.froms.get("genre")
    album = request.forms.get("album")

    try:
        year = int(year)
    except ValueError:
        return HTTPError(400, "Год альбома введён некорректно")

    try:
        new_album = album.save_user_info(year, artist, genre, album)
    except AssertionError as err:
        result = HTTPError(400, str(err))
    except album.AlreadyExcists as err:
        result = HTTPError(409, str(err))
    else:
        result = f"Новый альбом успешно созранён", new_album.id

    return result


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)