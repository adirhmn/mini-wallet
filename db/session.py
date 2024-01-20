from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import core.config as config

# Define database url
db_host = config.DB_HOST
db_user = config.DB_USER
db_password = config.DB_PASSWORD
db_port = config.DB_PORT
db_name = config.DB_NAME

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
# DATABASE_URL = "sqlite:///./walletdb.db"

# Initialize the machine database
engine = create_engine(DATABASE_URL, 
                        # connect_args={"check_same_thread": False} for sqlite
                        )

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the model
Base = declarative_base()

def get_db():
    # Get instance database session.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()