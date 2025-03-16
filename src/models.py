from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    apellido: Mapped[str] = mapped_column(String(50), nullable=False)
    fecha_suscripcion: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    favoritos = relationship("Favorito", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_suscripcion": self.fecha_suscripcion,
            "favoritos": [fav.serialize() for fav in self.favoritos],
        }

class Personaje(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    altura: Mapped[int] = mapped_column(Integer, nullable=True)
    peso: Mapped[int] = mapped_column(Integer, nullable=True)
    genero: Mapped[str] = mapped_column(String(20), nullable=True)
    planeta_origen: Mapped[int] = mapped_column(ForeignKey("planeta.id"), nullable=True)

    planeta = relationship("Planeta", back_populates="personajes")
    favoritos = relationship("Favorito", back_populates="personaje")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "altura": self.altura,
            "peso": self.peso,
            "genero": self.genero,
            "planeta_origen": self.planeta_origen,
        }

class Planeta(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    clima: Mapped[str] = mapped_column(String(50), nullable=True)
    poblacion: Mapped[int] = mapped_column(Integer, nullable=True)

    personajes = relationship("Personaje", back_populates="planeta")
    favoritos = relationship("Favorito", back_populates="planeta")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "clima": self.clima,
            "poblacion": self.poblacion,
        }

class Favorito(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    personaje_id: Mapped[int] = mapped_column(ForeignKey("personaje.id"), nullable=True)
    planeta_id: Mapped[int] = mapped_column(ForeignKey("planeta.id"), nullable=True)

    user = relationship("User", back_populates="favoritos")
    personaje = relationship("Personaje", back_populates="favoritos")
    planeta = relationship("Planeta", back_populates="favoritos")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "personaje_id": self.personaje_id,
            "planeta_id": self.planeta_id,
        }
