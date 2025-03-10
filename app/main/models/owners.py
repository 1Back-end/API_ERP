from dataclasses import dataclass   
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Table, Boolean, types, event, Enum
from datetime import datetime, date
from sqlalchemy.orm import relationship
from .db.base_class import Base
from sqlalchemy.dialects.postgresql import ENUM

# Définition d'un énumérateur pour représenter les différents statuts possibles d'un propriétaire
class Ownerstatus(str, Enum):
    ACTIVED = "ACTIVED"  # Actif
    UNACTIVED = "UNACTIVED"  # Inactif
    DELETED = "DELETED"  # Supprimé
    BLOCKED = "BLOCKED"  # Bloqué

# Définition de la classe Owner qui représente un propriétaire dans la base de données
class Owner(Base):
    """
    Modèle de base de données pour stocker les détails liés aux propriétaires
    """
    __tablename__ = 'owners'  # Nom de la table SQL

    # Identifiant unique du propriétaire (UUID)
    uuid: str = Column(String, primary_key=True, unique=True, index=True)

    # Informations personnelles
    email: str = Column(String, nullable=False, default="", index=True)  # Adresse email du propriétaire
    first_name: str = Column(String, nullable=False, default="")  # Prénom
    last_name: str = Column(String, nullable=False, default="")  # Nom de famille
    country_code: str = Column(String(5), nullable=False, default="", index=True)  # Code du pays (ex: +33)
    phone_number: str = Column(String(20), nullable=False, default="", index=True)  # Numéro de téléphone
    full_phone_number: str = Column(String(25), nullable=False, default="", index=True)  # Numéro complet

    # # Clé étrangère qui relie l'utilisateur ayant ajouté ce propriétaire
    # added_by_uuid: str = Column(String, ForeignKey('users.uuid'), nullable=True)
    # added_by = relationship("User", foreign_keys=[added_by_uuid], uselist=False)

    # Clé étrangère pour stocker l'avatar du propriétaire
    avatar_uuid: str = Column(String, ForeignKey('storages.uuid'), nullable=True)
    avatar = relationship("Storage", foreign_keys=[avatar_uuid], uselist=False)

    # Hash du mot de passe du propriétaire
    password_hash: str = Column(String(100), nullable=True, default="")

    # Statut du propriétaire (actif, inactif, supprimé, bloqué)
    status = Column(String, nullable=False, default=Ownerstatus.ACTIVED)

    # Indique si l'utilisateur est un nouvel utilisateur
    is_new_user: bool = Column(Boolean, nullable=True, default=False)

    # Champs pour la gestion des OTP (One-Time Password)
    otp: str = Column(String(5), nullable=True, default="")  # Code OTP
    otp_expired_at: datetime = Column(DateTime, nullable=True, default=None)  # Expiration du code OTP
    otp_password: str = Column(String(5), nullable=True, default="")  # Mot de passe OTP
    otp_password_expired_at: datetime = Column(DateTime, nullable=True, default=None)  # Expiration du mot de passe OTP

    # Dates d'ajout et de modification du propriétaire
    date_added: datetime = Column(DateTime, nullable=False, default=datetime.now())  # Date d'ajout
    date_modified: datetime = Column(DateTime, nullable=False, default=datetime.now())  # Date de modification

    # Représentation sous forme de chaîne de caractères de l'objet Owner
    def __repr__(self):
        return '<Owner: uuid: {} email: {}>'.format(self.uuid, self.email)

# Événement qui met à jour les champs de date avant l'insertion d'un nouvel enregistrement
@event.listens_for(Owner, 'before_insert')
def update_created_modified_on_create_listener(mapper, connection, target):
    """ 
    Écouteur d'événements qui s'exécute avant l'insertion d'un nouvel enregistrement
    et met à jour les champs de création et de modification.
    """
    target.date_added = datetime.now()
    target.date_modified = datetime.now()

# Événement qui met à jour le champ de date_modified avant toute mise à jour d'un enregistrement existant
@event.listens_for(Owner, 'before_update')
def update_modified_on_update_listener(mapper, connection, target):
    """ 
    Écouteur d'événements qui s'exécute avant une mise à jour et 
    met à jour le champ de modification.
    """
    target.date_modified = datetime.now()

# Ancienne classe commentée qui pourrait être utilisée pour valider certaines actions des propriétaires
# class OwnerActionValidation(Base):
#     __tablename__ = 'owner_action_validations'
#
#     uuid: str = Column(String, primary_key=True)
#
#     user_uuid: str = Column(String, ForeignKey('owners.uuid'), nullable=True)
#     code: str = Column(String, unique=False, nullable=True)
#     expired_date: any = Column(DateTime, default=datetime.now())
#     value: str = Column(String, default="", nullable=True)
#
#     date_added: any = Column(DateTime, nullable=False, default=datetime.now())
#
# @event.listens_for(OwnerActionValidation, 'before_insert')
# def update_created_modified_on_create_listener(mapper, connection, target):
#     """ 
#     Écouteur d'événements qui s'exécute avant l'insertion d'un nouvel enregistrement
#     et met à jour le champ de création.
#     """
#     target.date_added = datetime.now()
