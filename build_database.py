import os
from datetime import datetime
from config import db
from models import Movies, Directors

# movies
# Data to initialize database with
DIRECTORS = [
    {
        "name": "Christopher Nolan",
        "gender": 2,
        "uid": 101,
        "department": "Directing",
        "movies": [

            ("The Dark Knight Rises",  # original_title Text
             250000000,  # budget int
             112,  # popularity int
             "2012-07-16",  # release_date text yyyy-MM-dd(2009-12-10)
             1084939099,  # revenue int
             "The Dark Knight Rises",  # title Text
             7.6,  # vote_average real
             9106,  # vote_count int
             # overview Text
             "Following the death of District Attorney Harvey Dent, Batman assumes responsibility for Dent's crimes to protect the late attorney's reputation and is subsequently hunted by the Gotham City Police Department. Eight years later, Batman encounters the mysterious Selina Kyle and the villainous Bane, a new terrorist leader who overwhelms Gotham's finest. The Dark Knight resurfaces to protect a city that has branded him an enemy.",
             # tagline Text
             "The Legend Ends",
             49026),  # uid int

            ("The Dark Knight",
             185000000,
             187,
             "2008-07-16",
             1004558444,
             "The Dark Knight",
             8.2,
             12002,
             "Batman raises the stakes in his war on crime. With the help of Lt. Jim Gordon and District Attorney Harvey Dent, Batman sets out to dismantle the remaining criminal organizations that plague the streets. The partnership proves to be effective, but they soon find themselves prey to a reign of chaos unleashed by a rising criminal mastermind known to the terrified citizens of Gotham as the Joker.",
             "Why So Serious?",
             155)
        ]
    },

    {
        "name": "George Lucas",
        "gender": 2,
        "uid": 102,
        "department": "Directing",
        "movies": [

            ("Star Wars",  # original_title Text
             11000000,  # budget int
             126,  # popularity int
             "1977-05-25",  # release_date text yyyy-MM-dd(2009-12-10)
             775398007,  # revenue int
             "Star Wars",  # title Text
             8.1,  # vote_average real
             6624,  # vote_count int
             # overview Text
             "Princess Leia is captured and held hostage by the evil Imperial forces in their effort to take over the galactic Empire. Venturesome Luke Skywalker and dashing captain Han Solo team together with the loveable robot duo R2-D2 and C-3PO to rescue the beautiful princess and restore peace and justice in the Empire.",
             # tagline Text
             "A long time ago in a galaxy far, far away...",
             11),  # uid int

            ("Star Wars: Episode I - The Phantom Menace",
             115000000,
             54,
             "1999-05-19",
             924317558,
             "Star Wars: Episode I - The Phantom Menace",
             6.3,
             4432,
             "Anakin Skywalker, a young slave strong with the Force, is discovered on Tatooine. Meanwhile, the evil Sith have returned, enacting their plot for revenge against the Jedi.",
             "Every generation has a legend. Every journey has a first step. Every saga has a beginning.",
             32)
        ]

    },

    {
        "name": "Peter Jackson",
        "gender": 2,
        "uid": 103,
        "department": "Directing",
        "movies": [

            ("The Lord of the Rings: The Return of the King",  # original_title Text
             94000000,  # budget int
             123,  # popularity int
             "2003-12-01",  # release_date text yyyy-MM-dd(2009-12-10)
             1118888979,  # revenue int
             "The Lord of the Rings: The Return of the King",  # title Text
             8.1,  # vote_average real
             8064,  # vote_count int
             # overview Text
             "Aragorn is revealed as the heir to the ancient kings as he, Gandalf and the other members of the broken fellowship struggle to save Gondor from Sauron's forces. Meanwhile, Frodo and Sam bring the ring closer to the heart of Mordor, the dark lord's realm.",
             # tagline Text
             "The eye of the enemy is moving.",
             122)  # uid int
        ]

    },

    {
        "name": "Louis Leterrier",
        "gender": 2,
        "uid": 104,
        "department": "Directing",
        "movies": [

            ("Now You See Me",  # original_title Text
             75000000,  # budget int
             71,  # popularity int
             "2013-05-29",  # release_date text yyyy-MM-dd(2009-12-10)
             117698894,  # revenue int
             "Now You See Me",  # title Text
             7.3,  # vote_average real
             5487,  # vote_count int
             # overview Text
             "An FBI agent and an Interpol detective track a team of illusionists who pull off bank heists during their performances and reward their audiences with the money.",
             # tagline Text
             "4 amazing magicians. 3 impossible heists. 1 billion dollars. This is no illusion.",
             75656)  # uid int

        ]

    },
]

# Delete database file if it exists currently
if os.path.exists('final_project.db'):
    os.remove('final_project.db')

# Create the database
db.create_all()

# Iterate over the DIRECTORS structure and populate the database
for directors in DIRECTORS:
    d = Directors(name=directors.get("name"), gender=directors.get("gender"),
                  uid=directors.get("uid"), department=directors.get("department"))

    # Add the movies for the person
    for movies in directors.get("movies"):
        original_title, budget, popularity, release_date, revenue, title, vote_average, vote_count, overview, tagline, uid = movies
        d.movies.append(
            Movies(
                original_title=original_title,
                budget=budget,
                popularity=popularity,
                release_date=datetime.strptime(
                    release_date, "%Y-%m-%d").date(),
                revenue=revenue,
                title=title,
                vote_average=vote_average,
                vote_count=vote_count,
                overview=overview,
                tagline=tagline,
                uid=uid
            )
        )
    db.session.add(d)

db.session.commit()
