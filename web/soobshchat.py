from flask import Flask
from flask import render_template
from web.tasks import make_celery

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='sqla+sqlite:///celerydb.sqlite',
    CELERY_RESULT_BACKEND='sqla+sqlite:///celerydb.sqlite'
)
celery = make_celery(app)

@celery.task()
def add_together(a, b):
    return a + b

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('basic.html', name=name)

    result = add_together

result = add_together.delay(23, 42)


if __name__ == "__main__":
    app.run()