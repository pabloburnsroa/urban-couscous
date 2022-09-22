import os

from flask import Flask, render_template, send_from_directory


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    print(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'portfolio.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def my_home():
        # print(url_for('static', filename='favicon.ico'))
        return render_template('home/index.html')

    @app.route('/about')
    def about_me():
        return render_template('home/about.html')   \


    @app.route('/contact')
    def contact_me():
        return render_template('home/contact.html')

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import projects
    app.register_blueprint(projects.bp)

    return app
