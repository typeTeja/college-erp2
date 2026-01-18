/**
 * Library Management Hooks
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import libraryApi from '@/services/library-api';
import { queryKeys } from '@/config/react-query';

export function useBooks(filters?: {
    search?: string;
    category?: string;
    available?: boolean;
}) {
    return useQuery({
        queryKey: queryKeys.library.books.list(filters),
        queryFn: () => libraryApi.listBooks(filters),
    });
}

export function useIssueBook() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: { book_id: number; member_id: number; due_date: string }) =>
            libraryApi.issueBook(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.library.books.all });
        },
    });
}

export function useReturnBook() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (issueId: number) => libraryApi.returnBook(issueId),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.library.books.all });
        },
    });
}

export function useLibraryMembers() {
    return useQuery({
        queryKey: queryKeys.library.members,
        queryFn: () => libraryApi.listMembers(),
    });
}
