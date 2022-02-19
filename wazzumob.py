from unittest import BaseTestSuite
from app import create_app, db
from app.Model.models import Post, Tag

app = create_app()

@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
    if Tag.query.count() == 0:
        tags = ['Official WSU Events','Greek Row Events', 'WSU Club Events', 'Open to All', 'friendship']
        for t in tags:
            db.session.add(Tag(name=t))
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)