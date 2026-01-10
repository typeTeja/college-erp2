"""
Academic Setup Module - Integration Tests
Tests for bulk setup, dashboard, inline editing, validation, and audit logging
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.main import app
from app.models.academic.batch import AcademicBatch, ProgramYear, BatchSemester
from app.models.master_data import Section, PracticalBatch
from app.models.audit_log import AuditLog

client = TestClient(app)


@pytest.fixture
def auth_headers(test_db):
    """Get authentication headers for admin user"""
    # Login as admin
    response = client.post("/api/v1/auth/login", json={
        "email": "admin@test.com",
        "password": "admin123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestBulkSetup:
    """Test bulk batch setup functionality"""
    
    def test_bulk_setup_creates_complete_structure(self, test_db, auth_headers):
        """Test that bulk setup creates all expected records"""
        response = client.post(
            "/api/v1/batches/bulk-setup",
            headers=auth_headers,
            json={
                "program_id": 1,
                "joining_year": 2024,
                "regulation_id": 1,
                "sections_per_semester": 2,
                "section_capacity": 60,
                "labs_per_section": 3,
                "lab_capacity": 20
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify statistics
        assert data["years_created"] == 4
        assert data["semesters_created"] == 8
        assert data["sections_created"] == 16
        assert data["labs_created"] == 48
        assert data["total_section_capacity"] == 960
        assert data["total_lab_capacity"] == 960
        
        # Verify database records
        batch = test_db.get(AcademicBatch, data["batch_id"])
        assert batch is not None
        assert batch.batch_code == "2024-2028"
        
        # Verify years
        years = test_db.exec(
            select(ProgramYear).where(ProgramYear.batch_id == batch.id)
        ).all()
        assert len(years) == 4
        
        # Verify sections
        sections = test_db.exec(
            select(Section).where(Section.batch_id == batch.id)
        ).all()
        assert len(sections) == 16
        assert all(s.max_strength == 60 for s in sections)
        
        # Verify labs
        labs = test_db.exec(select(PracticalBatch)).all()
        assert len(labs) == 48
        assert all(lab.max_strength == 20 for lab in labs)
    
    def test_bulk_setup_prevents_duplicate_batch(self, test_db, auth_headers):
        """Test that duplicate batches are prevented"""
        # Create first batch
        client.post(
            "/api/v1/batches/bulk-setup",
            headers=auth_headers,
            json={
                "program_id": 1,
                "joining_year": 2024,
                "regulation_id": 1,
                "sections_per_semester": 2,
                "section_capacity": 60,
                "labs_per_section": 3,
                "lab_capacity": 20
            }
        )
        
        # Try to create duplicate
        response = client.post(
            "/api/v1/batches/bulk-setup",
            headers=auth_headers,
            json={
                "program_id": 1,
                "joining_year": 2024,
                "regulation_id": 1,
                "sections_per_semester": 2,
                "section_capacity": 60,
                "labs_per_section": 3,
                "lab_capacity": 20
            }
        )
        
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]
    
    def test_bulk_setup_logs_audit_entry(self, test_db, auth_headers):
        """Test that bulk setup creates audit log"""
        response = client.post(
            "/api/v1/batches/bulk-setup",
            headers=auth_headers,
            json={
                "program_id": 1,
                "joining_year": 2024,
                "regulation_id": 1,
                "sections_per_semester": 2,
                "section_capacity": 60,
                "labs_per_section": 3,
                "lab_capacity": 20
            }
        )
        
        batch_id = response.json()["batch_id"]
        
        # Check audit log
        audit = test_db.exec(
            select(AuditLog)
            .where(AuditLog.table_name == "academic_batch")
            .where(AuditLog.record_id == batch_id)
            .where(AuditLog.action == "CREATE")
        ).first()
        
        assert audit is not None
        assert audit.new_values["batch_code"] == "2024-2028"


class TestDashboard:
    """Test academic dashboard functionality"""
    
    def test_dashboard_returns_structure(self, test_db, auth_headers):
        """Test that dashboard returns hierarchical structure"""
        # Create test data first
        client.post(
            "/api/v1/batches/bulk-setup",
            headers=auth_headers,
            json={
                "program_id": 1,
                "joining_year": 2024,
                "regulation_id": 1,
                "sections_per_semester": 2,
                "section_capacity": 60,
                "labs_per_section": 3,
                "lab_capacity": 20
            }
        )
        
        # Get dashboard
        response = client.get(
            "/api/v1/academic-setup/dashboard/",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify structure
        assert "batches" in data
        assert "summary" in data
        assert len(data["batches"]) > 0
        
        batch = data["batches"][0]
        assert "years" in batch
        assert len(batch["years"]) == 4
        
        year = batch["years"][0]
        assert "semesters" in year
        assert len(year["semesters"]) == 2
        
        semester = year["semesters"][0]
        assert "sections" in semester
        assert len(semester["sections"]) == 2
        
        section = semester["sections"][0]
        assert "lab_groups" in section
        assert len(section["lab_groups"]) == 3
    
    def test_dashboard_calculates_utilization(self, test_db, auth_headers):
        """Test that dashboard calculates utilization correctly"""
        response = client.get(
            "/api/v1/academic-setup/dashboard/",
            headers=auth_headers
        )
        
        data = response.json()
        summary = data["summary"]
        
        assert "total_students" in summary
        assert "total_capacity" in summary
        assert "overall_utilization" in summary
        
        # Verify calculation
        if summary["total_capacity"] > 0:
            expected = (summary["total_students"] / summary["total_capacity"]) * 100
            assert abs(summary["overall_utilization"] - expected) < 0.01


class TestInlineEditing:
    """Test inline editing functionality"""
    
    def test_section_capacity_update(self, test_db, auth_headers):
        """Test updating section capacity"""
        # Create section first
        section = Section(
            name="Section A",
            code="A",
            batch_semester_id=1,
            max_strength=60,
            current_strength=30
        )
        test_db.add(section)
        test_db.commit()
        test_db.refresh(section)
        
        # Update capacity
        response = client.patch(
            f"/api/v1/sections/{section.id}",
            headers=auth_headers,
            json={"max_strength": 70}
        )
        
        assert response.status_code == 200
        assert response.json()["max_strength"] == 70
        
        # Verify in database
        test_db.refresh(section)
        assert section.max_strength == 70
    
    def test_section_capacity_validation(self, test_db, auth_headers):
        """Test that capacity cannot be reduced below enrollment"""
        # Create section with students
        section = Section(
            name="Section A",
            code="A",
            batch_semester_id=1,
            max_strength=60,
            current_strength=50
        )
        test_db.add(section)
        test_db.commit()
        test_db.refresh(section)
        
        # Try to reduce below enrollment
        response = client.patch(
            f"/api/v1/sections/{section.id}",
            headers=auth_headers,
            json={"max_strength": 40}
        )
        
        assert response.status_code == 400
        assert "Cannot reduce capacity" in response.json()["detail"]
    
    def test_section_update_logs_audit(self, test_db, auth_headers):
        """Test that section updates are logged"""
        section = Section(
            name="Section A",
            code="A",
            batch_semester_id=1,
            max_strength=60,
            current_strength=30
        )
        test_db.add(section)
        test_db.commit()
        test_db.refresh(section)
        
        # Update
        client.patch(
            f"/api/v1/sections/{section.id}",
            headers=auth_headers,
            json={"max_strength": 70}
        )
        
        # Check audit log
        audit = test_db.exec(
            select(AuditLog)
            .where(AuditLog.table_name == "section")
            .where(AuditLog.record_id == section.id)
            .where(AuditLog.action == "UPDATE")
        ).first()
        
        assert audit is not None
        assert audit.old_values["max_strength"] == 60
        assert audit.new_values["max_strength"] == 70


class TestValidation:
    """Test validation rules"""
    
    def test_cannot_delete_batch_with_students(self, test_db, auth_headers):
        """Test that batches with students cannot be deleted"""
        # Create batch with students
        batch = AcademicBatch(
            batch_code="2024-2028",
            batch_name="Test Batch",
            program_id=1,
            regulation_id=1,
            joining_year=2024,
            start_year=2024,
            end_year=2028,
            total_students=100
        )
        test_db.add(batch)
        test_db.commit()
        test_db.refresh(batch)
        
        # Try to delete
        response = client.delete(
            f"/api/v1/batches/{batch.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 400
        assert "Cannot delete batch with" in response.json()["detail"]
    
    def test_cannot_delete_lab_with_students(self, test_db, auth_headers):
        """Test that labs with students cannot be deleted"""
        # Create lab with students
        lab = PracticalBatch(
            name="P1",
            code="P1",
            section_id=1,
            max_strength=20,
            current_strength=15
        )
        test_db.add(lab)
        test_db.commit()
        test_db.refresh(lab)
        
        # Try to delete
        response = client.delete(
            f"/api/v1/master/practical-batches/{lab.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 400
        assert "Cannot delete" in response.json()["detail"]


class TestAuditLogs:
    """Test audit logging functionality"""
    
    def test_audit_logs_query(self, test_db, auth_headers):
        """Test querying audit logs"""
        response = client.get(
            "/api/v1/audit-logs/",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_audit_logs_filter_by_table(self, test_db, auth_headers):
        """Test filtering audit logs by table"""
        response = client.get(
            "/api/v1/audit-logs/?table_name=section",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        logs = response.json()
        
        if len(logs) > 0:
            assert all(log["table_name"] == "section" for log in logs)
    
    def test_audit_logs_filter_by_action(self, test_db, auth_headers):
        """Test filtering audit logs by action"""
        response = client.get(
            "/api/v1/audit-logs/?action=UPDATE",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        logs = response.json()
        
        if len(logs) > 0:
            assert all(log["action"] == "UPDATE" for log in logs)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
