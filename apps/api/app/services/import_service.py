from typing import List, Dict, Any
import pandas as pd
from io import BytesIO
from datetime import datetime
from sqlmodel import Session, select
from fastapi import UploadFile, HTTPException

from app.models.student import Student, Gender, BloodGroup, ScholarshipCategory, StudentStatus
from app.models.program import Program
from app.models.parent import Parent
from app.models.user import User
from app.models.import_log import ImportLog
from app.schemas.import_schema import (
    StudentImportRow, ImportPreviewResponse, ImportPreviewRow, 
    ImportRowStatus, ImportErrorDetail
)
from app.core.security import get_password_hash

class ImportService:
    def __init__(self, session: Session):
        self.session = session

    def parse_file(self, file: UploadFile) -> List[Dict[str, Any]]:
        try:
            contents = file.file.read()
            if file.filename.endswith('.csv'):
                df = pd.read_csv(BytesIO(contents))
            elif file.filename.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(BytesIO(contents))
            else:
                raise HTTPException(status_code=400, detail="Invalid file format")
            
            # Normalize columns
            df.columns = [c.lower().replace(' ', '_').strip() for c in df.columns]
            return df.to_dict('records')
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing file: {str(e)}")

    def validate_row(self, row: Dict[str, Any], programs_map: Dict[str, int], existing_admissions: set, default_program_code: str = None) -> ImportPreviewRow:
        errors = []
        valid_data = None
        status = ImportRowStatus.VALID

        # check duplicate in DB
        if str(row.get('admission_number')) in existing_admissions:
            status = ImportRowStatus.DUPLICATE
            errors.append(ImportErrorDetail(field="admission_number", message="Student already exists"))

        # Pydantic validation
        try:
            # Handle DOB dynamically
            raw_dob = row.get('dob')
            dob_obj = None
            if raw_dob and str(raw_dob) != 'nan':
                try:
                    dob_obj = pd.to_datetime(raw_dob).date()
                except:
                    pass # Leave as None

            # Map excel values to schema
            mapped_data = {
                "admission_number": str(row.get('admission_number', '')).upper().replace('ADM', '').split('.')[0].strip(),
                "name": str(row.get('full_name')) if row.get('full_name') and str(row.get('full_name')) != 'nan' else "Unknown Student",
                "gender": row.get('gender', 'MALE').upper() if row.get('gender') and str(row.get('gender')) != 'nan' else "MALE",
                "dob": dob_obj,
                "mobile": str(row.get('mobile', '')).split('.')[0] if row.get('mobile') and str(row.get('mobile')) != 'nan' else None, 
                "email": row.get('email'),
                "aadhaar": str(row.get('aadhaar', '')).split('.')[0] if row.get('aadhaar') and str(row.get('aadhaar')) != 'nan' else None,
                "blood_group": row.get('blood_group'),
                "course_code": row.get('course', '') or default_program_code or "BTECH-CS",
                "academic_year": int(row.get('year', 1)) if str(row.get('year', '')).isdigit() else 1,
                "semester": int(row.get('semester', 1)) if str(row.get('semester', '')).isdigit() else 1,
                "section": str(row.get('section', 'A')),
                "batch": str(row.get('batch', '2024-2028')),
                "father_name": str(row.get('father_name', 'Unknown')),
                "father_mobile": str(row.get('father_mobile', '9999999999')).split('.')[0],
                "mother_name": row.get('mother_name'),
                "guardian_mobile": str(row.get('guardian_mobile', '')).split('.')[0] if row.get('guardian_mobile') else None,
                "hostel_required": str(row.get('hostel_required', 'NO')),
                "transport_required": str(row.get('transport_required', 'NO')),
                "scholarship_category": row.get('scholarship_category'),
                "lateral_entry": str(row.get('lateral_entry', 'NO'))
            }
            
            # Remove None/NaN values to let optional Pydantic fields handle it
            cleaned_data = {}
            for k, v in mapped_data.items():
                if v is not None and str(v) != 'nan':
                     cleaned_data[k] = v
            
            valid_data = StudentImportRow(**cleaned_data)
            
            # Master Data Logic Validation
            # Relaxed: if course not found, warn or use default? 
            # We used default_program_code above. If still fails:
            if valid_data.course_code not in programs_map:
                # Fallback to ANY program?
                if default_program_code:
                     valid_data.course_code = default_program_code
                else:
                    errors.append(ImportErrorDetail(field="course", message=f"Course '{valid_data.course_code}' not found"))
                    status = ImportRowStatus.INVALID

        except Exception as e:
            status = ImportRowStatus.INVALID
            # Rough parsing of validation errors
            if hasattr(e, 'errors'):
                for err in e.errors(): # type: ignore
                    errors.append(ImportErrorDetail(field=str(err['loc'][0]), message=err['msg']))
            else:
                errors.append(ImportErrorDetail(field="row", message=str(e)))

        return ImportPreviewRow(
            row_number=0, # Set later
            data=valid_data or {}, # type: ignore
            status=status,
            errors=errors
        )

    def preview_import(self, file: UploadFile, user_id: int) -> ImportPreviewResponse:
        rows = self.parse_file(file)
        
        # Prefetch Master Data
        programs = self.session.exec(select(Program)).all()
        programs_map = {p.code: p.id for p in programs}
        # Pick a default program for fallback
        default_program_code = programs[0].code if programs else None
        
        existing_students = self.session.exec(select(Student.admission_number)).all()
        existing_admissions = set(existing_students)
        
        preview_rows = []
        valid_count = 0
        invalid_count = 0
        duplicate_count = 0
        
        for i, row in enumerate(rows):
            preview_row = self.validate_row(row, programs_map, existing_admissions, default_program_code)
            preview_row.row_number = i + 1
            
            if preview_row.status == ImportRowStatus.VALID:
                valid_count += 1
            elif preview_row.status == ImportRowStatus.DUPLICATE:
                duplicate_count += 1
            else:
                invalid_count += 1
                
            preview_rows.append(preview_row)
            
        # Log basic attempt
        log = ImportLog(
            file_name=file.filename or "unknown",
            uploaded_by_id=user_id,
            total_rows=len(rows),
            status="PREVIEW"
        )
        self.session.add(log)
        self.session.commit()
        
        return ImportPreviewResponse(
            total_rows=len(rows),
            valid_count=valid_count,
            invalid_count=invalid_count,
            duplicate_count=duplicate_count,
            rows=preview_rows
        )

    def execute_import(self, preview_rows: List[ImportPreviewRow], user_id: int, file_name: str) -> ImportLog:
        # Pre-fetch maps again just to be safe in context
        programs = self.session.exec(select(Program)).all()
        programs_map = {p.code: p.id for p in programs}
        
        imported_count = 0
        failed_count = 0
        
        for row in preview_rows:
            if row.status != ImportRowStatus.VALID:
                continue
                
            try:
                # Row-level transaction
                # Row-level transaction
                with self.session.begin_nested():
                    data = row.data
                    # Defaults for missing data
                    username = data.admission_number
                    # If DOB missing, use default 01012000 for password and 2000-01-01 for DB
                    dob_str = str(data.dob) if data.dob else "2000-01-01"
                    password = data.dob.strftime('%d%m%Y') if data.dob else "01012000"
                    
                    # Auto-generate email if missing, using admission number and rchmct.org domain
                    if not data.email:
                        email = f"{data.admission_number}@rchmct.org"
                    else:
                        email = data.email

                    user = User(
                        username=username,
                        email=email, 
                        full_name=data.name or "Unknown",
                        hashed_password=get_password_hash(password),
                        is_active=True, 
                        is_superuser=False
                    )
                    self.session.add(user)
                    self.session.flush() # get ID
                    
                    # Create Student
                    student = Student(
                        admission_number=data.admission_number,
                        name=data.name or "Unknown",
                        dob=dob_str,
                        phone=data.mobile or "0000000000",
                        email=email,
                        user_id=user.id,
                        program_id=programs_map[data.course_code],
                        current_year=data.academic_year or 1,
                        current_semester=data.semester or 1,
                        section=data.section or "A",
                        batch=data.batch or "2024-2028",
                        gender=data.gender or Gender.MALE,
                        aadhaar_number=data.aadhaar,
                        blood_group=data.blood_group,
                        hostel_required=(data.hostel_required == "YES"),
                        transport_required=(data.transport_required == "YES"),
                        scholarship_category=data.scholarship_category or ScholarshipCategory.GENERAL,
                        lateral_entry=(data.lateral_entry == "YES"),
                        status=StudentStatus.IMPORTED_PENDING_VERIFICATION
                    )
                    self.session.add(student)
                    self.session.flush()
                    
                    # Create Parent
                    parent = Parent(
                        linked_student_id=student.id, # type: ignore
                        father_name=data.father_name or "Unknown",
                        father_mobile=data.father_mobile or "9999999999",
                        mother_name=data.mother_name,
                        guardian_mobile=data.guardian_mobile
                    )
                    self.session.add(parent)
                    
                    imported_count += 1
            
            except Exception as e:
                print(f"Failed to import row {row.row_number}: {e}")
                failed_count += 1
                # Transaction rolls back automatically for this nested block
        
        self.session.commit()
        
        # Create final log
        log = ImportLog(
            file_name=file_name,
            uploaded_by_id=user_id,
            timestamp=datetime.utcnow(),
            total_rows=len(preview_rows),
            imported_count=imported_count,
            failed_count=failed_count,
            duplicate_count=len([r for r in preview_rows if r.status == ImportRowStatus.DUPLICATE]),
            status="SUCCESS" if failed_count == 0 else "PARTIAL"
        )
        self.session.add(log)
        self.session.commit()
        
        return log
