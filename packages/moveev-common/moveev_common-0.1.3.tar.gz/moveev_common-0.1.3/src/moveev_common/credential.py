from sqlalchemy import Column, Integer, String, UniqueConstraint, Text, ForeignKey
from sqlalchemy.orm import validates, relationship
from jose import jwt
from typing import TYPE_CHECKING

import os
from . import Base


class Credential(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True)
    provider = Column(String)
    encrypted_token = Column(Text)
    username = Column(String)
    password = Column(String)
    database = Column(String)

    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    client = relationship("Client", back_populates="credentials")

    __table_args__ = (
        UniqueConstraint("encrypted_token", name="credential_unique_key"),
    )

    @staticmethod
    def encrypt_token(token):
        secret_key = os.environ.get("JWT_SECRET")
        if not secret_key:
            raise ValueError("JWT_SECRET not found in environment variables")
        encrypted = jwt.encode({"token": token}, secret_key, algorithm="HS256")
        return encrypted

    @staticmethod
    def decrypt_token(encrypted_token):
        secret_key = os.environ.get("JWT_SECRET")
        if not secret_key:
            raise ValueError("JWT_SECRET not found in environment variables")
        decrypted = jwt.decode(encrypted_token, secret_key, algorithms=["HS256"])
        return decrypted["token"]

    @validates("encrypted_token")
    def validate_encrypted_token(self, key, token):
        return self.encrypt_token(token)

    def get_token(self):
        if self.encrypted_token:
            return self.decrypt_token(self.encrypted_token)
        return None

    @classmethod
    def create_credential(cls, session, client_id, provider, token):
        credential = cls(
            client_id=client_id,
            provider=provider,
            encrypted_token=token,
        )
        session.add(credential)
        session.commit()
        return credential

    @staticmethod
    def get_token_from_credential_id(db, credential_id):
        credential = db.query(Credential).filter_by(id=credential_id).first()
        if credential:
            return credential.get_token()
        return None

    # hide token from terminal output
    def __repr__(self):
        return f"<Credential(id={self.id}, provider='{self.provider}')>"


from .client import Client
