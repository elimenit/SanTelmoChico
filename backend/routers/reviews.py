"""Endpoints de las reseñas.
"""
from fastapi import APIRouter, Query, Path, Body, status
from schemas.review import (
    Review, ReviewCreate, ReviewUpdate, ReviewDelete, ReviewPublic, ReviewUpsert,
    ReviewFilters
)
from dependencies.database import DBReviewsDep
from dependencies.dbsession import SessionDep
router = APIRouter()

@router.get("/", response_model=list[ReviewPublic], status_code=status.HTTP_200_OK)
def get_all(
    db: DBReviewsDep, session: SessionDep, 
    filters: ReviewFilters = Query()):
    return db.get_all(session, filters)

@router.get("/{id}", response_model=ReviewPublic, status_code=status.HTTP_200_OK)
async def get(
    db: DBReviewsDep, session: SessionDep, id: int):
    return db.get(session, ReviewUpsert(id))

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    db: DBReviewsDep, session: SessionDep,
    new_review: ReviewCreate):
    db.add(session, new_review)

@router.put("/", status_code=status.HTTP_202_ACCEPTED)
async def update( 
    db: DBReviewsDep, session: SessionDep,
    update_review: ReviewUpdate
    ):
    return db.update(session, update_review)

@router.delete("/", response_model=ReviewPublic, status_code=status.HTTP_200_OK)
async def delete(
    db: DBReviewsDep, session: SessionDep,
    review: ReviewDelete = Body()
):
    return db.remove(session, review)