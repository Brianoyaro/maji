from flask import render_template
from app.error import bp
from app import db


@bp.app_errorhandler(404)
def not_found_error(error):
    """404 error"""
    return render_template("error/404.html"), 404


@bp.app_errorhandler(500)
def internal_error(error):
    """500 error"""
    db.session.rollback()
    return render_template("error/500.html"), 500
