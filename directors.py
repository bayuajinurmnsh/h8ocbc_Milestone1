from flask import make_response, abort

"""
import method from config.py and models.py
"""
from config import db
from models import Directors, DirectorsSchema, Movies


def read_all():
    """
    This function responds to a request for /api/director
    with the complete lists of director

    :return:        json string of list of director
    """
    # Create the list of director from our data
    directors = Directors.query.order_by(Directors.id).all()

    # Serialize the data for the response
    directors_schema = DirectorsSchema(many=True)
    data = directors_schema.dump(directors)
    return data


def create(directors):
    """
    This function creates a director in the director structure
    based on the passed in director data

    :param director:  director to create in director structure
    :return:        201 on success, 406 on director exists, 406 on invalid json data
                    409 on existing data
    """
    required = ['department', 'gender', 'name', 'uid']

    # user have to send department, gender, name, and uid
    if len(directors) != 4:
        abort(
            406, f"you have send invalid data! make sure you only send data with this key {required}.")

    valid_send_data = [x for x in directors if x not in required]
    if len(valid_send_data) != 0:
        abort(
            406, f"you have send invalid data! make sure you only send data with this key {required}")

    body_name = directors.get("name")
    body_uid = directors.get("uid")

    existing_directors = (
        Directors.query.filter(Directors.name == body_name)
        .one_or_none()
    )

    existing_uid = (
        Directors.query.filter(Directors.uid == body_uid)
        .one_or_none()
    )

    # Can we insert this director?
    if existing_directors is None:

        if existing_uid is not None:
            abort(409, f"UID {body_uid} already exists")

        # Create a director instance using the schema and the passed in director
        schema = DirectorsSchema()
        new_directors = schema.load(directors, session=db.session)

        # Add the director to the database
        db.session.add(new_directors)
        db.session.commit()

        # Serialize and return the newly created director in the response
        data = schema.dump(new_directors)

        return data, 201

    # Otherwise, nope, director exists already
    else:
        abort(409, f"Director with name {body_name} already exists")


def read_one(director_id):
    """
    This function responds to a request for /api/director/{director_id}
    with one matching director from director

    :param director_id:   Id of director to find
    :return:            director matching id
    """
    # Build the initial query
    directors = (
        Directors.query.filter(Directors.id == director_id)
        .outerjoin(Movies)
        .one_or_none()
    )

    # Did we find a director?
    if directors is not None:

        # Serialize the data for the response
        directors_schema = DirectorsSchema()
        data = directors_schema.dump(directors)
        return data

    # Otherwise, nope, didn't find that director
    else:
        abort(404, f"Director not found for Id: {director_id}")


def update(director_id, directors):
    """
    This function updates an existing director in the director structure

    :param director_id:   Id of the director to update in the director structure
    :param director:      director to update
    :return:            updated director structure
    """
    required = ['department', 'gender', 'name', 'uid']

    # user have to send department, gender, name, and uid
    if len(directors) != 4:
        abort(
            406, f"you have send invalid data! make sure you only send data with this key {required}.")

    valid_send_data = [x for x in directors if x not in required]
    if len(valid_send_data) != 0:
        abort(
            406, f"you have send invalid data! make sure you only send data with this key {required}")

    # Get the director requested from the db into session

    body_uid = directors.get("uid")
    body_name = directors.get("name")

    update_directors = Directors.query.filter(
        Directors.id == director_id
    ).one_or_none()

    update_uid = Directors.query.filter(
        Directors.uid == body_uid
    ).one_or_none()

    update_name = Directors.query.filter(
        Directors.name == body_name
    ).one_or_none()

    # Did we find an existing director?
    if update_directors is not None:
        if update_uid is not None and update_uid.id != update_directors.id:
            abort(409, f"Unique id {body_uid} already exists!")

        if update_name is not None and update_name.id != update_directors.id:
            abort(409, f"Directors {body_name} already exists!")

        # turn the passed in director into a db object
        schema = DirectorsSchema()
        update = schema.load(directors, session=db.session)

        # Set the id to the director we want to update
        update.id = update_directors.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated director in the response
        data = schema.dump(update_directors)

        return data, 200

    # Otherwise, nope, didn't find that director
    else:
        abort(404, f"Director not found for Id: {director_id}")


def delete(director_id):
    """
    This function deletes a director from the director structure

    :param director_id:   Id of the director to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the director requested
    directors = Directors.query.filter(
        Directors.id == director_id).one_or_none()

    # Did we find a director?
    if directors is not None:
        db.session.delete(directors)
        db.session.commit()
        return make_response(f"Director with Id: {director_id} has been deleted", 200)

    # Otherwise, nope, didn't find that director
    else:
        abort(404, f"Director not found for Id: {director_id}")


# get data director with method LIKE%director_name%
def get_director_by_name(director_name):
    """
    This function responds to a request for api/directors/get_by_name/{director_name}
    with one matching director from director

    :param director_name:   name of director to find
    :return:            director matching name

    use LIKE%name% method
    """
    search = f"%{director_name}%"
    # posts = Post.query.filter(Post.tags.like(search)).all()

    directors = Directors.query.filter(Directors.name.like(search)).all()

    if directors is None:
        abort(
            404, f"Cannot find the director by name like {director_name}")

    # Serialize the data for the response
    directors_schema = DirectorsSchema(many=True)
    data = directors_schema.dump(directors)
    return data


# get total revenue each director from all the movies,
def get_each_revenue_from_movie(director_id):
    """
    This function responds to a request for api/directors/get_total_networth/{director_id}
    with one matching director from director

    :param director_id:   id of director to find
    :return:            director matching id

    this function give us information total networth from each director
    """

    # Build the initial query
    directors = (
        Directors.query.filter(Directors.id == director_id)
        .outerjoin(Movies)
        .one_or_none()
    )

    # Did we find a director?
    if directors is not None:

        # Serialize the data for the response
        directors_schema = DirectorsSchema()
        data = directors_schema.dump(directors)

        total_networth = []
        for x in data['movies']:
            def temp_networth(revenue, budget): return revenue - budget
            d = temp_networth(x['revenue'], x['budget'])
            total_networth.append(d)

        response_data = {
            'uid': data['uid'],
            'id': data['id'],
            'gender': data['gender'],
            'name': data['name'],
            'total_movies': len(data['movies']),
            'total_networth': sum(total_networth)}

        return response_data

    # Otherwise, nope, didn't find that director
    else:
        abort(404, f"Director not found for Id: {director_id}")
