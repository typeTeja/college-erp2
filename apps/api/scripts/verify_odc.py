
import sys
import os
from datetime import date, datetime, timedelta
from sqlmodel import Session, select

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import engine
from app.models.user import User
from app.models.student import Student
from app.models.odc import ODCHotel, ODCRequest, StudentODCApplication, ODCStatus, ApplicationStatus
from app.services.odc_service import ODCService
from app.schemas.odc import ODCHotelCreate, ODCRequestCreate, SelectionUpdate

def verify_odc_workflow():
    print("\n🚀 Starting ODC Workflow Verification...")
    
    with Session(engine) as session:
        # 1. Setup Data: Get Admin User and a Dummy Student
        print("1. Setting up test data...")
        admin = session.exec(select(User).where(User.username == "admin")).first()
        if not admin:
            print("❌ Admin user not found!")
            return

        # 1a. Get a valid Department
        from app.models.department import Department
        department = session.exec(select(Department)).first()
        if not department:
            print("   Creating dummy department...")
            department = Department(code="CSE", name="Computer Science Dept")
            session.add(department)
            session.commit()
            session.refresh(department)

        # 1b. Get a valid Program
        from app.models.program import Program
        program = session.exec(select(Program)).first()
        if not program:
            print("   Creating dummy program...")
            program = Program(code="CSE", name="Computer Science", department_id=department.id, duration_years=4)
            session.add(program)
            session.commit()
            session.refresh(program)

        # Create/Get dummy student linked to admin for testing (or create new user/student)
        student = session.exec(select(Student).where(Student.user_id == admin.id)).first()
        if not student:
            print("   Creating dummy student profile for admin...")
            student = Student(
                admission_number="TEST-001",
                name="Test Student",
                email="test@student.com",
                user_id=admin.id,
                program_id=program.id
            )
            session.add(student)
            session.commit()
            session.refresh(student)
        print(f"   Using Student: {student.name} (ID: {student.id})")

        service = ODCService(session)

        # 2. Create Hotel
        print("\n2. Creating Hotel...")
        hotel_data = ODCHotelCreate(
            name=f"Test Hotel {datetime.now().strftime('%H%M%S')}",
            address="Hyderabad",
            contact_person="Manager",
            phone="9999999999",
            default_pay_rate=500.0
        )
        hotel = service.create_hotel(hotel_data)
        print(f"   ✅ Created Hotel: {hotel.name} (ID: {hotel.id})")

        # 3. Create ODC Request
        print("\n3. Creating ODC Request...")
        request_data = ODCRequestCreate(
            hotel_id=hotel.id,
            event_name="Wedding Reception",
            event_date=date.today() + timedelta(days=2),
            report_time=datetime.now() + timedelta(days=2),
            duration_hours=5,
            vacancies=10,
            pay_amount=600.0,
            transport_provided=True
        )
        # Note: In service we pass user_id manually
        request = service.create_request(request_data, admin.id)
        print(f"   ✅ Created Request: {request.event_name} (ID: {request.id})")

        # 4. Student Applies
        print("\n4. Student Applying...")
        try:
            application = service.apply_for_odc(student.id, request.id)
            print(f"   ✅ Application successful (Status: {application.status})")
        except ValueError as e:
            print(f"   ⚠️ Application failed (Expected if re-running): {e}")
            application = session.exec(
                select(StudentODCApplication).where(
                    StudentODCApplication.student_id == student.id,
                    StudentODCApplication.request_id == request.id
                )
            ).first()

        # 5. Admin Selects Student
        print("\n5. Admin Selecting Student...")
        selection_update = SelectionUpdate(
            application_ids=[application.id],
            status=ApplicationStatus.SELECTED,
            remarks="Good academic record"
        )
        updated = service.update_selections(selection_update)
        print(f"   ✅ Updated {len(updated)} applications to SELECTED")

        # Verify final state
        session.refresh(application)
        if application.status == ApplicationStatus.SELECTED:
            print("\n✅ WORKFLOW VERIFIED SUCCESSFULLY!")
        else:
            print(f"\n❌ Workflow Verification Failed. Status is {application.status}")

if __name__ == "__main__":
    verify_odc_workflow()
