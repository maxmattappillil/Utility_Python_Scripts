import os


def create_fastapi_project(project_name):
    # Check if the project directory already exists
    if os.path.exists(project_name):
        print(
            f"The project directory '{project_name}' already exists. Please choose a different name.")
        return

    # Define the project structure
    directories = [
        project_name,
        os.path.join(project_name, 'app'),
        os.path.join(project_name, 'app', 'routers'),
    ]

    files = [
        os.path.join(project_name, 'app', '__init__.py'),
        os.path.join(project_name, 'app', 'main.py'),
        os.path.join(project_name, 'app', 'models.py'),
        os.path.join(project_name, 'app', 'database.py'),
        os.path.join(project_name, 'app', 'schemas.py'),
        os.path.join(project_name, 'app', 'config.py'),
        os.path.join(project_name, 'app', 'oauth2.py'),
        os.path.join(project_name, 'app', 'utils.py'),
        os.path.join(project_name, 'app', 'routers', '__init__.py'),
        os.path.join(project_name, '.dockerignore'),
        os.path.join(project_name, 'DockerFile'),
        os.path.join(project_name, 'docker-compose.yml'),
        os.path.join(project_name, '.env'),
    ]

    # Create directories
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    # Create files
    for file in files:
        open(file, 'w').close()

    print(f"\nProject structure for '{project_name}' has been created.")
    

#Create project structure
project_name = input("Enter the project name: ")
create_fastapi_project(project_name)

def write_out_to_file(filename, code_content):
    
    with open(filename, "w") as file:
        file.write(code_content)


def fill_in_main_file():
    code_content = """from fastapi import FastAPI
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
    """
    
    # Specify the filename for the new Python file
    filename = os.path.join(project_name, 'app', 'main.py')
    
    write_out_to_file(filename, code_content)


def fill_in_models_file():
    code_content = """from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base
    """
    
    # Specify the filename for the new Python file
    filename = os.path.join(project_name, 'app', 'models.py')
    
    write_out_to_file(filename, code_content)


def fill_in_database_file():
    code_content = """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


#Establishes the connection to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()
    """
    
    # Specify the filename for the new Python file
    filename = os.path.join(project_name, 'app', 'database.py')
    
    write_out_to_file(filename, code_content)
    

def fill_in_config_file():
    code_content = """from pydantic_settings import BaseSettings

# Performs validation to make sure environment variables are set up and of the right type

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    # secret_key: str
    # algorithm: str
    # access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
    """
    
    # Specify the filename for the new Python file
    filename = os.path.join(project_name, 'app', 'config.py')
    
    write_out_to_file(filename, code_content)


def fill_in_ouath2_file():
    code_content = """from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

# Specifies which endpoint FastAPI should search the Authorization Header for in order to find a Token

# =============================================================================
# Uncomment below if you want to change the endpoint / perform any authentication in general
# =============================================================================

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Can generate this using the cmd command "openssl rand -hex 32"
# SECRET_KEY = settings.secret_key

# ALGORITHM = settings.algorithm
# ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    # expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add in the expiration key
    to_encode.update({'exp': expire})

    # Create the token --> Data, secret key, algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get('user_id')

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=str(id))

    except JWTError:
        raise credentials_exception

    return token_data

# =============================================================================
# Uncomment below to get the current user
# =============================================================================

# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
#     credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                           detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

#     token = verify_access_token(token, credentials_exception)

#     user = db.query(models.User).filter(models.User.id == token.id).first()

#     return user
    """
    
    #Write out to file
    filename = os.path.join(project_name, 'app', 'oauth2.py')
    
    write_out_to_file(filename, code_content)

def fill_in_utils_file():
    code_content = """from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
    """
    
    #Write out to file
    filename = os.path.join(project_name, 'app', 'utils.py')
    
    write_out_to_file(filename, code_content)
    
    
def fill_in_env_file():
    code_content = """DATABASE_HOSTNAME=""
DATABASE_PORT=""
DATABASE_PASSWORD=""
DATABASE_NAME=""
DATABASE_USERNAME=""
# SECRET_KEY = ""
# ALGORITHM = ""
# ACCESS_TOKEN_EXPIRE_MINUTES = 0
    """
    
    #Write out to file
    filename = os.path.join(project_name, '.env')
    
    write_out_to_file(filename, code_content)


fill_in_main_file()
fill_in_models_file()
fill_in_database_file()
fill_in_config_file()
fill_in_ouath2_file()
fill_in_utils_file()
fill_in_env_file()

print("Files have been pre-populated with standard content")
