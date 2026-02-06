import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "apps", "api", ".env"))
success = load_dotenv(env_path)

# Add the apps/api directory to sys.path so we can import 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "apps", "api")))

from sqlmodel import Session, select
from app.db.session import engine
from app.domains.admission.models import Application
from app.domains.admission.schemas import ApplicationRead
import json
from pydantic import ValidationError

def test_serialization():
    print("Testing serialization of Application object to ApplicationRead schema...")
    with Session(engine) as session:
        # Get the latest application
        statement = select(Application).order_by(Application.id.desc()).limit(1)
        application = session.exec(statement).first()
        
        if not application:
            print("No application found in database.")
            return

        print(f"Found Application ID: {application.id}, Number: {application.application_number}")
        
        try:
            # Attempt to serialize
            print("Attempting to parse into ApplicationRead...")
            try:
                read_schema = ApplicationRead.model_validate(application)
            except AttributeError:
                read_schema = ApplicationRead.from_orm(application)
                
            print("Serialization successful!")
            print("Model is valid for schema.")
        except ValidationError as ve:
            print(f"Pydantic Validation Error: {ve}")
        except Exception as e:
            print(f"Unexpected Error during serialization: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_serialization()
