from app import db, create_app
from app.models import Users, Order, Message

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """registers the function as a
    shell context function. When the flask shell command runs, it will
    invoke this function and register the items returned by it in the shell
    session. The reason the function returns a dictionary and not a list is
    that for each item you have to also provide a name under which it will
    be referenced in the shell, which is given by the dictionary keys."""
    return {'db': db, 'Users': Users, 'Order': Order, 'Message': Message}
