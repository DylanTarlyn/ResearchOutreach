from app import create_app, db
from app.Model.models import Post, Research

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Post': Post}

@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
    if Research.query.count() == 0:
        research_field = ['Test1','Test2','Test3','Test4','Test5']
        for t in research_field:
            db.session.add(Research(field=t))
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)