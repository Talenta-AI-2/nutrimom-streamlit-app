from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey,
    Text,
    Float, and_,
)
from datetime import datetime, timezone, date
import bcrypt
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, Session
from model.engine.Engine import Base,get_session,get_engine
import pandas as pd


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
def query_data_to_dataframe(user_id, start_date, end_date):
    # Create SQLAlchemy engine and session
    engine = get_engine()
    session = get_session()

    try:
        # Query data within the specified date range for the user
        query = session.query(GiziHarianIbuHamil).filter(
            and_(
                GiziHarianIbuHamil.user_id == user_id,
                GiziHarianIbuHamil.created_at.between(start_date, end_date)
            )
        ).all()

        # If there are records, convert to DataFrame
        if query:
            data = []
            for record in query:
                data.append({
                    'user_id': record.user_id,
                    'created_at': record.created_at,
                    'total_air': record.total_air,
                    'total_energi': record.total_energi,
                    'total_protein': record.total_protein,
                    'total_lemak': record.total_lemak,
                    'total_karbo': record.total_karbo,
                    'total_serat': record.total_serat,
                    'selisih_air': record.selisih_air,
                    'selisih_energi': record.selisih_energi,
                    'selisih_protein': record.selisih_protein,
                    'selisih_lemak': record.selisih_lemak,
                    'selisih_karbo': record.selisih_karbo,
                    'selisih_serat': record.selisih_serat,
                    'user_name': record.user.name  # Assuming 'User' model has a 'name' attribute
                })

            df = pd.DataFrame(data)
            return df

        else:
            print("No data found for the specified date range and user.")
            return pd.DataFrame()

    finally:
        # Close the session
        session.close()
def get_tinggi_badan_and_status_by_name(db: Session, name):
    query = db.query(PertumbuhanAnak.tinggi_badan, PertumbuhanAnak.status_nutrisi, PertumbuhanAnak.created_at).join(PertumbuhanAnak.anak).filter(
        Anak.name == name
    )
    results = query.all()
    return results

def create_gizi_harian_ibu_hamil(db: Session, total_gizi_data: dict, selisih_gizi: dict, user_id: int):
    new_gizi = GiziHarianIbuHamil(
        user_id=user_id,
        total_air=total_gizi_data['Air'],
        total_energi=total_gizi_data['Energi'],
        total_protein = total_gizi_data['Protein'],
        total_lemak = total_gizi_data['Lemak'],
        total_karbo= total_gizi_data['Karbohidrat'],
        total_serat = total_gizi_data['Serat'],

        selisih_air=selisih_gizi['Air'],
        selisih_energi=selisih_gizi['Energi'],
        selisih_protein=selisih_gizi['Protein'],
        selisih_lemak=selisih_gizi['Lemak'],
        selisih_karbo=selisih_gizi['Karbohidrat'],
        selisih_serat=selisih_gizi['Serat'],

    )
    db.add(new_gizi)
    db.commit()
    db.refresh(new_gizi)
    return new_gizi

def get_pertumbuhan_anak(db: Session, user_id):
    return  db.query(PertumbuhanAnak).filter_by()
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
