"""Interaccion con la BD, acerca de las reseñas.
"""
from fastapi import HTTPException, status
from sqlmodel import Session, select
from schemas.review import (
    ReviewCreate, 
    ReviewUpsert, 
    ReviewDelete, 
    ReviewPublic, 
    ReviewFilters, 
    ReviewUpdate, 
    Review
)

class DBReviews:
    def add(self, session: Session, new_review: ReviewCreate, user_id: int) -> ReviewPublic:
        db_review = Review.model_validate(new_review, update={"user_id": user_id})
        
        session.add(db_review)
        session.commit()
        session.refresh(db_review)
        
        return db_review

    def get(self, session: Session, review: ReviewUpsert) -> ReviewPublic:
        db_review = session.get(Review, review.id)
        
        if not db_review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Reseña no encontrada"
            )
            
        return db_review

    def get_all(self, session: Session, filters: ReviewFilters) -> list[ReviewPublic]:
        statement = select(Review)
        
        if filters.stars is not None:
            statement = statement.where(Review.stars == filters.stars)
            
        results = session.exec(statement).all()
        return results
    
    def update(self, session: Session, update_review: ReviewUpdate) -> ReviewPublic:
        db_review = session.get(Review, update_review.id)
        if not db_review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Reseña no encontrada"
            )
        
        update_data = update_review.model_dump(exclude_unset=True)
        
        db_review.sqlmodel_update(update_data)
        
        session.add(db_review)
        session.commit()
        session.refresh(db_review)
        
        return db_review

    def remove(self, session: Session, review: ReviewDelete) -> ReviewPublic:
        db_review = session.get(Review, review.id)
        if not db_review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Reseña no encontrada"
            )
            
        session.delete(db_review)
        session.commit()
        
        return db_review