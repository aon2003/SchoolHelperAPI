from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from dependencies import get_db
import crud
import schemas

router = APIRouter(
    prefix='/subjects',
    tags=['Subjects'],
    dependencies=[Depends(get_db)]
)


@router.get(
    '',
    response_model=List[schemas.Subject],
    summary="Gets a list of all Subjects",
)
def get_subjects(database: Session = Depends(get_db)):
    """
    Description
    """
    subjects = crud.get_all_subjects(database)
    if subjects is None:
        raise HTTPException(
            status_code=404,
            detail='Няма зададени предмети!'
        )
    
    return subjects


@router.get(
    '/{name}',
    response_model=schemas.Subject,
    summary="Gets a Subject object from the DB.",
)
def get_subjects(name: str, database: Session = Depends(get_db)):
    """
    Description
    """
    subject = crud \
        .get_subject_by_name(database, name)
    if subject is None:
        raise HTTPException(
            status_code=404,
            detail=f"Предмет с име '{name}' не съществува!"
        )
    
    return subject


@router.post(
    '/create',
    response_model=schemas.Subject,
    summary='Create a Subject instance in the DB.'
)
def create_subject(subject: schemas.SubjectCreate,
                   database: Session = Depends(get_db)):
    if len(subject.name) < 3 or len(subject.name) > 50:
        raise HTTPException(
            status_code=400,
            detail="Името на Предмет трябва да бъде между 3 и 50 символа!"
        )
    
    db_subject = crud.get_subject_by_name(database, subject.name)
    if db_subject:
        raise HTTPException(
            status_code=400,
            detail=f"Предмет с име '{subject.name}' вече съществува!"
        )
    
    return crud.create_subject(database, subject)


@router.put(
    '/{name}/edit',
    response_model=schemas.Subject,
    summary='Edit the details of a Subject object from the DB.'
)
def edit_subject(name: str, subject: schemas.SubjectCreate,
                 database: Session = Depends(get_db)):
    db_subject = crud.get_subject_by_name(database, name)
    db_new_subject = crud.get_subject_by_name(database, subject.name)
    if db_subject is None:
        raise HTTPException(
            status_code=404,
            detail=f"Предмет с име '{name}' не съществува!"
        )
    if db_new_subject is not None:
        raise HTTPException(
            status_code=400,
            detail=f"Предмет с име '{subject.name}' вече съществува!"
        )
    if len(subject.name) < 3 or len(subject.name) > 50:
        raise HTTPException(
            status_code=400,
            detail="Името на Предмет трябва да бъде между 3 и 50 символа!"
        )
    return crud.edit_subject(database, db_subject, subject)


@router.delete(
    '/{name}/delete',
    response_model=schemas.Subject,
    summary='Delete a Subject instance from the DB.'
)
def delete_subject(name: str, database: Session = Depends(get_db)):
    db_subject = crud.get_subject_by_name(database, name)
    if db_subject is None:
        raise HTTPException(
            status_code=404,
            detail=f"Предмет с име '{name}' не съществува!"
        )
    return crud.delete_subject(database, db_subject)


@router.get(
    '/{name}/classes',
    response_model=List[schemas.Class],
    summary='Get a list of the Classes that are assigned to this Subject.'
)
def get_subject_classes(name: str, database: Session = Depends(get_db)):
    subject = crud.get_subject_by_name(database, name)
    if subject is None:
        raise HTTPException(
            status_code=404,
            detail=f"Предмет с име '{name}' не съществува!"
        )
    if subject.classes is None:
        raise HTTPException(
            status_code=404,
            detail=f'Предметът не е зададен на никой Клас!'
        )
    return subject.classes