from website import create_app
from flask import render_template

app = create_app()

# Define the route for the custom 404 error

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
