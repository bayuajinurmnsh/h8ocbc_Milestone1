from datetime import datetime
from config import db, ma
from marshmallow import fields
from flask import abort
from sqlalchemy.orm import validates


class Directors(db.Model):
    """
    This Class have a function to control and create table of directors.
    In this class i have create realtion one(director) to many(movies) so 1 director can have many movies.

    in this class i have create a few validates like:
        - validates a name , name minimum length is 3 , and only accept input alphabet and a space
        - validates a gender, to control if user only can input gender with value 0,1,2

    """
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    gender = db.Column(db.Integer)
    uid = db.Column(db.Integer)
    department = db.Column(db.Text)

    movies = db.relationship(
        'Movies',
        backref='directors',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Movies.release_date)'
    )

    # validate name
    @validates('name')
    def validate_name(self, key, value):
        if all(x.isalpha() or x.isspace() for x in value):
            return value

        if len(value) < 3:
            abort(
                400, f"Please insert name with minimum length is 3 alphabet")

        abort(
            400, f"Name only contains alphabet and space, numbers and other characters are restricted")

    # validate gender
    @validates('gender')
    def validate_gender(self, key, value):
        valid_gender = [0, 1, 2]
        if value not in valid_gender:
            abort(
                400, f"Please insert gender with val:0  -> i prefer not to say , 1 -> for female, 2 -> for male ")
        return value


class Movies(db.Model):
    """
    This Class have a function to control and create table of movies.
    In this class i have create realtion one(movies) to one(director) so 1 movies only can have 1 directors.

    in this class i have create a few validates like:
        - validates an original title , original title minimum length is 1 
        - validates a budget, minimum value is 10000 (ten thousand)
        - validates a title , title minimum length is 1 
        - validates a date, the valid date format is (Year-Month-Day) , example: 2010-12-30

    """
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    original_title = db.Column(db.Text)
    budget = db.Column(db.Integer)
    popularity = db.Column(db.Integer)
    release_date = db.Column(db.Text, default=datetime.now().date(),
                             onupdate=datetime.now().date())  # Y-M-D
    revenue = db.Column(db.Integer)
    title = db.Column(db.Text)
    vote_average = db.Column(db.REAL)
    vote_count = db.Column(db.Integer)
    overview = db.Column(db.Text)
    tagline = db.Column(db.Text)
    uid = db.Column(db.Integer)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))

    # validate original_title
    @validates('original_title')
    def validate_original_title(self, key, value):
        if len(value) < 1:
            abort(
                400, f"Original tittle cannot be empty, minimum length is 1 characters")
        return value

    # validate budget
    @validates('budget')
    def validate_budget(self, key, value):
        if value < 10000:
            abort(
                400, f"Minimum budget is 10000")
        return value

    # validate title
    @validates('title')
    def validate_title(self, key, value):
        if len(value) < 1:
            abort(
                400, f"Tittle cannot be empty, minimum length is 1 characters")
        return value

    # validate release_date
    @validates('release_date')
    def set_release_date(self, key, value):
        if value != "":
            try:
                datetime.strptime(str(value), "%Y-%m-%d").date()
                return value
            except ValueError:
                abort(
                    400, f"Please insert a valid date format(YYYY-MM-DD), example:2010-12-31")
        else:
            default_date = datetime.today().strftime('%Y-%m-%d')
            return default_date


class DirectorsSchema(ma.SQLAlchemyAutoSchema):
    """
    This Class have a function to control all method that connected to Director
    , and control the relation from director to movies.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Directors
        sqla_session = db.session
        load_instance = True

    movies = fields.Nested('DirectorsMoviesSchema', default=[], many=True)


class DirectorsMoviesSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # print only id(movies), original_title, vote_average, budget, and revenue
    id = fields.Int()
    director_id = fields.Int()
    original_title = fields.Str()
    vote_average = fields.Str()
    budget = fields.Int()
    revenue = fields.Int()


class MoviesSchema(ma.SQLAlchemyAutoSchema):
    """
    This Class have a function to control all method that connected to Movies
    , and control the relation from movies to director.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Movies
        sqla_session = db.session
        load_instance = True

    directors = fields.Nested("MoviesDirectorsSchema", default=None)


class MoviesDirectorsSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()
    name = fields.Str()
    gender = fields.Int()
