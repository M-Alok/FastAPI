from fastapi import FastAPI, Depends, status, Response, HTTPException
from .import schemas, models, database
from sqlalchemy.orm import Session

app = FastAPI()

def get_db():
    db = database.sessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(database.engine)

@app.post('/create', status_code=status.HTTP_201_CREATED)
def creat_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blogs')
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}')
def get_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog of id {id} is not found')
    return blog

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog of id {id} is not found')

    blog.title = request.title
    blog.body = request.body

    db.commit()
    db.refresh(blog)
    return blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first().delete(synchronize_session=False)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog of id {id} is not found')
    db.commit()
    return {'detail': f'Blog of id {id} is deleted'}