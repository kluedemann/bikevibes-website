import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from bikemonitor.db import get_db

bp = Blueprint('map', __name__)

@bp.route("/")
def index():
    return render_template("index.html")

