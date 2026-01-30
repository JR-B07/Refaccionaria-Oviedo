# Implementación genérica de CRUDBase para SQLAlchemy
from typing import Generic, TypeVar, Type, Any, Optional, List
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
	def __init__(self, model: Type[ModelType]):
		self.model = model

	def get(self, db: Session, id: Any) -> Optional[ModelType]:
		return db.query(self.model).get(id)

	def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
		return db.query(self.model).offset(skip).limit(limit).all()

	def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
		obj_in_data = obj_in.dict() if hasattr(obj_in, 'dict') else dict(obj_in)
		db_obj = self.model(**obj_in_data)
		db.add(db_obj)
		db.commit()
		db.refresh(db_obj)
		return db_obj

	def update(self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
		obj_data = db_obj.__dict__
		update_data = obj_in.dict(exclude_unset=True) if hasattr(obj_in, 'dict') else dict(obj_in)
		for field in obj_data:
			if field in update_data:
				setattr(db_obj, field, update_data[field])
		db.add(db_obj)
		db.commit()
		db.refresh(db_obj)
		return db_obj

	def remove(self, db: Session, id: Any) -> ModelType:
		obj = db.query(self.model).get(id)
		db.delete(obj)
		db.commit()
		return obj
