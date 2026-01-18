import { renderHook, waitFor } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { useStudent, useStudents } from '../../hooks/use-students'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

// Mock API interactions
vi.mock('@/services/student-service', () => ({
    studentService: {
        getStudent: vi.fn(),
        getStudents: vi.fn(),
    }
}))

const createWrapper = () => {
    const queryClient = new QueryClient({
        defaultOptions: {
            queries: {
                retry: false,
            },
        },
    })
    return ({ children }: { children: React.ReactNode }) => (
        <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    )
}

describe('useStudent Hook', () => {
    it('should be defined', () => {
        expect(useStudent).toBeDefined()
    })
})
