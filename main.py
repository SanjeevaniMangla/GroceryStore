from application import create_app
from application.celery_worker import make_celery


app = create_app()


app.config.update(
        CELERY_BROKER_URL='redis://localhost:6379/1',
         result_backend='redis://localhost:6379/2',
        enable_utc = False,
        timezone = "Asia/Kolkata"
    )
celery = make_celery(app)


if __name__ == '__main__':
    app.run(debug=True)