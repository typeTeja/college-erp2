/**
 * Student Assignment API Service
 */
import { api } from './api';
import type {
    AutoAssignRequest,
    AutoAssignResponse,
    StudentSectionAssignmentCreate,
    StudentSectionAssignment,
    ReassignRequest,
    SectionRosterResponse,
    UnassignedStudentsResponse
} from '@/types/student-assignment';

export const studentAssignmentService = {
    /**
     * Auto-assign students to sections
     */
    autoAssignToSections: async (data: AutoAssignRequest): Promise<AutoAssignResponse> => {
        const response = await api.post<AutoAssignResponse>(
            '/assignments/sections/auto-assign',
            data
        );
        return response.data;
    },

    /**
     * Manually assign a student to a section
     */
    manualAssignToSection: async (data: StudentSectionAssignmentCreate): Promise<StudentSectionAssignment> => {
        const response = await api.post<StudentSectionAssignment>(
            '/assignments/sections/manual-assign',
            data
        );
        return response.data;
    },

    /**
     * Reassign a student to a different section
     */
    reassignStudent: async (assignmentId: number, data: ReassignRequest): Promise<StudentSectionAssignment> => {
        const response = await api.patch<StudentSectionAssignment>(
            `/assignments/sections/${assignmentId}/reassign`,
            data
        );
        return response.data;
    },

    /**
     * Delete a section assignment
     */
    deleteAssignment: async (assignmentId: number): Promise<void> => {
        await api.delete(`/assignments/sections/${assignmentId}`);
    },

    /**
     * Get section roster (list of students)
     */
    getSectionRoster: async (sectionId: number): Promise<SectionRosterResponse> => {
        const response = await api.get<SectionRosterResponse>(
            `/assignments/sections/${sectionId}/roster`
        );
        return response.data;
    },

    /**
     * Get unassigned students for a batch/semester
     */
    getUnassignedStudents: async (batchId: number, semesterNo: number): Promise<UnassignedStudentsResponse> => {
        const response = await api.get<UnassignedStudentsResponse>(
            `/assignments/batches/${batchId}/unassigned`,
            { params: { semester_no: semesterNo } }
        );
        return response.data;
    }
};
