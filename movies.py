from flask import make_response, abort
from config import db
from models import Directors, Movies, MoviesSchema
from datetime import datetime
from sqlalchemy import desc


def read_all():
    """
    This function responds to a request for /api/movies
    with the complete list of movies, sorted by release_date 

    :return:                json list of all movies for all director
    """
    # Query the database for all the movies
    movies = Movies.query.order_by(Movies.id).all()

    # Serialize the list of movies from our data
    Movies_schema = MoviesSchema(many=True)
    data = Movies_schema.dump(movies)
    return data


def create(director_id, movies):
    """
    This function creates a new movie related to the passed in directors id.

    :param directors_id:       Id of the directors the movie is related to
    :param movie:            The JSON containing the movie data
    :return:                201 on success, 406 on invalid json data, 409 in existing data
    """

    required = ['budget', 'original_title', 'overview', 'popularity',
                'release_date', 'revenue', 'tagline', 'title', 'uid',
                'vote_average', 'vote_count']

    # user have to send department, gender, name, and uid
    if len(movies) != 11:
        abort(
            406, f"you have send invalid data! make sure you only send data with this key {required}.")

    valid_send_data = [x for x in movies if x not in required]
    if len(valid_send_data) != 0:
        abort(
            406, f"you have send invalid data! make sure you only send data with this key {required}")

    body_uid = movies.get("uid")
    body_original_title = movies.get("original_title")

    # get the parent directors
    directors = Directors.query.filter(
        Directors.id == director_id).one_or_none()

    uid = Movies.query.filter(
        Movies.uid == body_uid).one_or_none()

    original_title = Movies.query.filter(
        Movies.original_title == body_original_title).one_or_none()

    # Was a directors found?
    if directors is None:
        abort(404, f"directors not found for Id: {director_id}")

    if uid is not None:
        abort(409, f"Movies with UId: {body_uid} already exists")

    if original_title is not None:
        abort(
            409, f"Movies with original title: {body_original_title} already exists")

    # Create a movie schema instance
    schema = MoviesSchema()
    new_movies = schema.load(movies, session=db.session)

    # Add the movie to the directors and database
    directors.movies.append(new_movies)
    db.session.commit()

    # Serialize and return the newly created movie in the response
    data = schema.dump(new_movies)

    return data, 201


def read_one(movie_id):
    """
    This function responds to a request for
    /api/movies/{movie_id}
    with one matching movie for the associated director

    :param director_id:       Id of director the movie is related to
    :param movie_id:         Id of the movie
    :return:                json string of movie contents
    """
    # Query the database for the movie
    movies = (
        Movies.query.join(Directors, Directors.id == Movies.director_id)
        .filter(Movies.id == movie_id)
        .one_or_none()
    )

    # Was a movie found?
    if movies is not None:
        movies_schema = MoviesSchema()
        data = movies_schema.dump(movies)
        return data

    # Otherwise, nope, didn't find that movie
    else:
        abort(404, f"Movies not found for Id: {movie_id}")


def update(director_id, movie_id, movies):
    """
    This function updates an existing movie related to the passed in
    director id.

    :param director_id:       Id of the director the movie is related to
    :param movie_id:         Id of the movie to update
    :param content:            The JSON containing the movie data
    :return:                200 on success
    """
    required = ['budget', 'original_title', 'overview', 'popularity',
                'release_date', 'revenue', 'tagline', 'title', 'uid',
                'vote_average', 'vote_count']

    # user have to send department, gender, name, and uid
    if len(movies) != 11:
        abort(
            406, f"you have send invalid data! make sure you only send data with this key {required}.")

    valid_send_data = [x for x in movies if x not in required]
    if len(valid_send_data) != 0:
        abort(
            406, f"you have send invalid data! make sure you only send data with this key {required}")

    body_uid = movies.get("uid")
    body_original_title = movies.get("original_title")

    update_movies = (
        Movies.query.filter(Directors.id == director_id)
        .filter(Movies.id == movie_id)
        .one_or_none()
    )

    update_uid = Movies.query.filter(
        Movies.uid == body_uid
    ).one_or_none()

    update_original_title = Movies.query.filter(
        Movies.original_title == body_original_title).one_or_none()

    # Did we find an existing movie?
    if update_movies is not None:
        if update_uid is not None and update_uid.id != update_movies.id:
            abort(409, f"Unique id {body_uid} already exists!")

        if update_original_title is not None and update_original_title.id != update_movies.id:
            abort(
                409, f"Original title {body_original_title} already exists!")

        # turn the passed in movie into a db object
        schema = MoviesSchema()
        update = schema.load(movies, session=db.session)

        # Set the id's to the movie we want to update
        update.id = update_movies.id
        update.director_id = update_movies.director_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated movie in the response
        data = schema.dump(update_movies)

        return data, 200

    # Otherwise, nope, didn't find that movie
    else:
        abort(404, f"Movies not found for Id: {movie_id}")


def delete(movie_id):
    """
    This function deletes a movie from the movie structure

    :param director_id:   Id of the director the movie is related to
    :param movie_id:     Id of the movie to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the movie requested
    movies = (
        Movies.query.filter(Movies.id == movie_id)
        .one_or_none()
    )

    # did we find a movie?
    if movies is not None:
        db.session.delete(movies)
        db.session.commit()
        return make_response(
            f"Movies with Id {movie_id} deleted", 200
        )

    # Otherwise, nope, didn't find that movie
    else:
        abort(404, f"Movies not found for Id: {movie_id}")


def get_movies_by_date_range(start_date, end_date):
    """
    This function responds to a request for
    /api/movies/{start_date}/{end_date}
    with one matching movie for the associated director

    :param movie_id:         Id of the movie
    :return:                json string of movie contents
    """

    check_date = check_valid_date(start_date, end_date)

    if check_date == 'invalid':
        abort(400, f"Please insert a valid date with format Year-Month-date, example : 2010-12-29. And start date must be lower than end date")

    movies = Movies.query.filter(Movies.release_date.between(
        start_date, end_date)).order_by(Movies.release_date)

    if movies is None:
        abort(
            404, f"Cannot find the movies by date with range from {start_date} - {end_date}")

    movies_schema = MoviesSchema(many=True)
    data = movies_schema.dump(movies)
    return data


# this function has made to help validation function get_movies_by_date
def check_valid_date(start, end):
    """
    this function has been created to help function get_movies_by_date_range 
          to validate a date is it valid or not
    """

    if start != "" and end != "":
        try:
            d1 = datetime.strptime(str(start), "%Y-%m-%d").date()
            d2 = datetime.strptime(str(end), "%Y-%m-%d").date()

            if d1 > d2:  # d1 must lower than d2
                return 'invalid'

            return 'valid'
        except ValueError:
            return 'invalid'
    else:
        return 'invalid'


# get movies by its rating
def get_movies_by_rating(rating):
    """
    This function responds to a request for
    /api/movies/get_by_rating/{rating}
    with one matching movie for the associated director

    :param rating:         vote_average of the movies
    :return:                json string of movie contents
    """

    movies = Movies.query.filter(
        Movies.vote_average >= rating).order_by(Movies.vote_average)

    if movies is None:
        abort(
            404, f"Cannot find the movies with rating : {rating}")

    movies_schema = MoviesSchema(many=True)
    data = movies_schema.dump(movies)
    return data


# total networth
def get_networth_movie(movie_id):
    """
    This function responds to a request for
    /api/movies/get_networth/{movie_id}
    with one matching movie for the associated director

    :param movie_id:         Id of the movies
    :return:                json string of movie contents
    """

    movies = (
        Movies.query.join(Directors, Directors.id == Movies.director_id)
        .filter(Movies.id == movie_id)
        .one_or_none()
    )

    # Was a movie found?
    if movies is not None:
        movies_schema = MoviesSchema()
        data = movies_schema.dump(movies)

        response_data = {'uid': data['uid'],
                         'original_title': data['original_title'],
                         'id': data['id'],
                         'title': data['title'],
                         'revenue': data['revenue'],
                         'budget': data['budget'],
                         'directors': {
            'id': data['directors']['id'],
            'name': data['directors']['name']
        },
            'networth': data['revenue'] - data['budget']
        }
        return response_data

    # Otherwise, nope, didn't find that movie
    else:
        abort(404, f"Movies not found for Id: {movie_id}")


def get_movies_by_name(movies_name):
    """
    This function responds to a request for api/directors/get_by_name/{director_name}
    with one matching director from director

    :param director_name:   name of director to find
    :return:            director matching name

    use LIKE%name% method
    """
    search = f"%{movies_name}%"
    # posts = Post.query.filter(Post.tags.like(search)).all()

    movies = Movies.query.filter(Movies.original_title.like(search)).all()

    if movies is None:
        abort(
            404, f"Cannot find the movie by name like {movies_name}")

    # Serialize the data for the response
    movies_schema = MoviesSchema(many=True)
    data = movies_schema.dump(movies)
    return data


def get_expensive_movie():
    """
    This function responds to a request for /api/movies
    with the complete list of movies, sorted by release_date 

    :return:                json list of all movies for all director
    """
    # Query the database for all the movies
    movies = Movies.query.order_by(desc(Movies.budget)).all()

    # Serialize the list of movies from our data
    Movies_schema = MoviesSchema(many=True)
    data = Movies_schema.dump(movies)
    return data[0]


def get_more_revenue_movie():
    """
    This function responds to a request for /api/movies
    with the complete list of movies, sorted by release_date 

    :return:                json list of all movies for all director
    """
    # Query the database for all the movies
    movies = Movies.query.order_by(desc(Movies.revenue)).all()

    # Serialize the list of movies from our data
    Movies_schema = MoviesSchema(many=True)
    data = Movies_schema.dump(movies)
    return data[0]


def get_best_of_the_best_movie():
    """
    This function responds to a request for /api/movies
    with the complete list of movies, sorted by release_date 

    :return:                json list of all movies for all director
    """
    # Query the database for all the movies
    movies = Movies.query.order_by(desc(Movies.vote_average)).all()

    # Serialize the list of movies from our data
    Movies_schema = MoviesSchema(many=True)
    data = Movies_schema.dump(movies)
    best = data[0]['vote_average']

    best_movies = (
        Movies.query.filter(Movies.vote_average == best)
        .all()
    )

    Movies_schema2 = MoviesSchema(many=True)
    data = Movies_schema2.dump(best_movies)

    return data
