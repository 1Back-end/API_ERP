import math
import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_
import re
from typing import List, Optional, Union
import uuid
from app.main.core.i18n import __
from sqlalchemy.orm import Session
from app.main.crud.base import CRUDBase
from app.main import models,schemas,crud



class CRUDFeature(CRUDBase[models.Feature,schemas.FeatureCreate,schemas.FeatureUpdate]):

    @classmethod
    def get_by_uuid(cls,db:Session,uuid:str):
        return db.query(models.Feature).filter(models.Feature.uuid == uuid,models.Feature.is_deleted==False).first()
    
    @classmethod
    def get_by_name(cls, db: Session,*, name: str):
        return db.query(models.Feature).filter(models.Feature.name == name, models.Feature.is_deleted==False).first()
    
    @classmethod
    def create(cls, db: Session, *, features_data: schemas.FeatureCreateResquest, added_by_uuid: str):
        # Vérifier si le type d’abonnement existe et n'est pas supprimé
        type_abonnement = crud.type_abonnement.get_by_uuid(db=db,uuid=features_data.type_abonnement_uuid)

        if not type_abonnement:
            raise HTTPException(status_code=404, detail=__("type-abonnement-not-found"))

        created_features = []

        for feature_data in features_data.features:
            exist_feature = db.query(models.Feature).filter(
                models.Feature.name == feature_data.name,
                models.Feature.type_abonnement_uuid == features_data.type_abonnement_uuid,
                models.Feature.is_deleted == False
            ).first()

            if exist_feature:
                raise HTTPException(status_code=409, detail=__("feature-already-exists") + ": " + feature_data.name)

            new_feature = models.Feature(
                uuid=str(uuid.uuid4()),
                name=feature_data.name,
                type_abonnement_uuid=features_data.type_abonnement_uuid,
                added_by_uuid=added_by_uuid
            )

            db.add(new_feature)
            created_features.append(new_feature)

        db.commit()
        
        return created_features
    

    @classmethod
    def update(cls, db: Session, *, obj_in: schemas.FeatureUpdateResquest, added_by_uuid: str):
        # Vérifier si le type d’abonnement existe et n'est pas supprimé
        type_abonnement = crud.type_abonnement.get_by_uuid(db=db, uuid=obj_in.type_abonnement_uuid)

        if not type_abonnement:
            raise HTTPException(status_code=404, detail=__("type-abonnement-not-found"))

        update_feature = []

        # Mettre à jour chaque fonctionnalité
        for feature_data in obj_in.features:
            feature = cls.get_by_uuid(db=db, uuid=feature_data.uuid)
            
            if not feature:
                raise HTTPException(status_code=404, detail=__("feature-not-found"))
            
            # Mise à jour des attributs de la fonctionnalité
            if feature_data.name:
                feature.name = feature_data.name
            if feature_data.type_abonnement_uuid:
                feature.type_abonnement_uuid = feature_data.type_abonnement_uuid

            # Ajouter à la liste des fonctionnalités mises à jour
            db.add(feature)
            db.commit()  # Commit après chaque mise à jour
            db.refresh(feature)  # Rafraîchir l'objet feature pour les derniers changements
            update_feature.append(feature)  # Ajouter la fonctionnalité mise à jour à la liste

        return update_feature

        
    @classmethod
    def delete(cls,db:Session,*,uuid:str):
        features = cls.get_by_uuid(db=db,uuid=uuid)
        if not features:
            raise HTTPException(status_code=404, detail=__("feature-not-found"))
        features.is_deleted = True
        db.commit()

    @classmethod
    def get_features_by_type_abonnement(cls,db:Session,*,type_abonnement_uuid:str):
        return db.query(models.Feature).filter(models.Feature.type_abonnement_uuid==type_abonnement_uuid,models.Feature.is_deleted==False).all()


        
        
        

    

features = CRUDFeature(models.Feature)