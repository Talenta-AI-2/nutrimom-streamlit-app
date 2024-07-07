from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey,
    Text,
    Float,
)
from datetime import datetime, timezone, date
import bcrypt
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, Session
from model.engine.Engine import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    _password = Column(String(255), nullable=False)
    last_signin = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext_password):
        self._password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, plaintext_password):
        return bcrypt.checkpw(plaintext_password.encode('utf-8'), self._password.encode('utf-8'))


class Anak(Base):
    __tablename__ = "anak"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    tanggal_lahir = Column(Date, nullable=False)

    user = relationship("User", backref="anak")
    pertumbuhan = relationship("PertumbuhanAnak", back_populates="anak")

class PertumbuhanAnak(Base):
    __tablename__ = "pertumbuhan_anak"

    id = Column(Integer, primary_key=True, autoincrement=True)
    anak_id = Column(Integer, ForeignKey("anak.id"), nullable=False)
    umur = Column(Float, nullable=False)
    tinggi_badan = Column(Float, nullable=False)
    status_nutrisi = Column(String(255), nullable=False)  # note: 'stunting/tidak'
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    # Define relationship to Anak
    anak = relationship("Anak", back_populates="pertumbuhan")

class GiziHarianIbuHamil(Base):
    __tablename__ = "gizi_harian_ibu_hamil"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_air = Column(Float, nullable=False)
    total_energi = Column(Float, nullable=False)
    total_protein = Column(Float, nullable=False)
    total_lemak = Column(Float, nullable=False)
    total_karbo = Column(Float, nullable=False)
    total_serat = Column(Float, nullable=False)
    selisih_air = Column(Float, nullable=False)
    selisih_energi = Column(Float, nullable=False)
    selisih_protein = Column(Float, nullable=False)
    selisih_lemak = Column(Float, nullable=False)
    selisih_karbo = Column(Float, nullable=False)
    selisih_serat = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    user = relationship(User)

def create_gizi_harian_ibu_hamil(db: Session, gizi_data: dict):
    new_gizi = GiziHarianIbuHamil(**gizi_data)
    db.add(new_gizi)
    db.commit()
    db.refresh(new_gizi)
    return new_gizi

def get_anak_by_user_id(db: Session, user_id):
    return db.query(Anak).filter_by(user_id=user_id).order_by(Anak.tanggal_lahir).all()
def get_tanggal_lahir_by_name(db: Session, name):
    anak = db.query(Anak).filter_by(name=name).first()
    return anak.tanggal_lahir if anak else None
def get_anak_id_by_name(db: Session, name: str):
    anak = db.query(Anak).filter_by(name=name).first()
    return anak.id if anak else None
def create_pertumbuhan_anak(db: Session, anak_id: int, umur: int, tinggi_badan: str, status_nutrisi: str):
    new_pertumbuhan = PertumbuhanAnak(
        anak_id=anak_id,
        umur=umur,
        tinggi_badan=tinggi_badan,
        status_nutrisi=status_nutrisi
    )
    db.add(new_pertumbuhan)
    db.commit()
    db.refresh(new_pertumbuhan)
    return new_pertumbuhan


def create_anak(db: Session, user_id: int, name: str, tanggal_lahir: date):
    new_anak = Anak(user_id=user_id, name=name, tanggal_lahir=tanggal_lahir)
    db.add(new_anak)
    db.commit()
    db.refresh(new_anak)
    return new_anak


def get_user_id_by_username(session, username):
    user = session.query(User).filter(User.username == username).first()
    if user:
        return user.id
    return None


def check_username_exists(session, username: str):
    return session.query(User).filter_by(username=username).first()


def create_user(session, username: str, password: str):
    if check_username_exists(session, username):
        raise ValueError("Username already exists")
    new_user = User(username=username, password=password)
    session.add(new_user)
    session.commit()
    return new_user


def get_user_by_username(session, username: str):
    return session.query(User).filter(User.username == username).first()


def verify_user_password(session, username: str, password: str):
    user = get_user_by_username(session, username)
    if user and user.verify_password(password):
        return True
    return False
