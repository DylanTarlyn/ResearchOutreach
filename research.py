from app import create_app, db
from app.Model.models import Post, Research, Language

app = create_app()


@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
    if Research.query.count() == 0:
        research_field = ['Topic1','Topic2','Topic3','Topic4','Topic5']
        for t in research_field:
            db.session.add(Research(field=t))
        db.session.commit()
    if Language.query.count()==0:
        language_field=['Lang1','Lang2','Lang3','Lang4','Lang5']
        for l in language_field:
            db.session.add(Language(field=l))
            db.session.commit()
   

if __name__ == "__main__":
    app.run(debug=True)