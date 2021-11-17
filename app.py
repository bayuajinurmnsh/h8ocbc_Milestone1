"""
Main module from the server
"""

# import module render template untuk merender html
from flask import render_template

# import module buatan user dengna nama config.py
import config


# Get the application instance
connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")


# Create a URL route in our application for "/"


if __name__ == "__main__":
    connex_app.run(debug=True)
