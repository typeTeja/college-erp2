from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlmodel import Session
from app.db.session import get_session
from app.api.deps import get_current_user
from app.models.user import User
from app.services.import_service import ImportService
from app.schemas.import_schema import ImportPreviewResponse, ImportExecuteRequest
import json
from typing import List
from app.schemas.import_schema import ImportPreviewRow

router = APIRouter()

def check_import_permissions(user: User):
    allowed_roles = {"SUPER_ADMIN", "ADMISSION_OFFICER", "ADMIN"}
    user_roles = {role.name for role in user.roles}
    print(f"DEBUG IMPORTS: User={user.email}, Roles={user_roles}, IsSuper={user.is_superuser}")
    if not allowed_roles.intersection(user_roles) and not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions for bulk import"
        )

@router.post("/preview", response_model=ImportPreviewResponse)
def preview_import(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Upload and preview student import file.
    Validates structure, types, and duplicates.
    """
    check_import_permissions(current_user)
    service = ImportService(session)
    return service.preview_import(file, current_user.id) # type: ignore

@router.post("/execute")
def execute_import(
    preview_data: ImportPreviewResponse,
    file_name: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Execute the import for confirmed valid rows.
    """
    check_import_permissions(current_user)
    service = ImportService(session)
    log = service.execute_import(preview_data.rows, current_user.id, file_name) # type: ignore
    return {"message": "Import completed", "log_id": log.id, "status": log.status}

from fastapi.responses import StreamingResponse
import io
import csv

@router.get("/template")
def download_template():
    """
    Download a sample CSV template for student import.
    """
    headers = [
        "admission_number", "full_name", "gender", "dob", "mobile", 
        "email", "aadhaar", "blood_group", 
        "course", "year", "semester", "section", "batch",
        "father_name", "father_mobile", "mother_name", "guardian_mobile",
        "hostel_required", "transport_required", "scholarship_category", "lateral_entry"
    ]
    
    sample_row = [
        "ADM2024001", "John Doe", "MALE", "2005-08-15", "9876543210", 
        "john.doe@example.com", "123456789012", "O+", 
        "BTECH-CS", "1", "1", "A", "2024-2028",
        "Robert Doe", "9876543211", "Mary Doe", "",
        "YES", "NO", "GENERAL", "NO"
    ]
    
    stream = io.StringIO()
    writer = csv.writer(stream)
    writer.writerow(headers)
    writer.writerow(sample_row)
    
    stream.seek(0)
    
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=student_import_template.csv"
    return response
