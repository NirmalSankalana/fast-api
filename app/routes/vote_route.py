from fastapi import APIRouter, Depends, status, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session

from ..schemas import vote_schema
from .. import oauth2, models, database

router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: vote_schema.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id ==
                                              vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=f"user has already voted on post {found_vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote!"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully removed vote"}
