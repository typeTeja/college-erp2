import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { Book, BookIssue, LibraryFine } from '@/types/library';

export const libraryService = {
    useBooks: (search?: string, category?: string) => {
        return useQuery({
            queryKey: ['books', search, category],
            queryFn: async () => {
                const params = new URLSearchParams();
                if (search) params.append('search', search);
                if (category) params.append('category', category);
                const { data } = await api.get<Book[]>(`/library/books?${params.toString()}`);
                return data;
            }
        });
    },

    useCreateBook: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (book: Partial<Book>) => {
                const { data } = await api.post<Book>('/library/books', book);
                return data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['books'] });
            }
        });
    },

    useIssueBook: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (issue: { book_id: number; student_id: number; due_date: string }) => {
                const { data } = await api.post<BookIssue>('/library/issue', issue);
                return data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['books'] });
                queryClient.invalidateQueries({ queryKey: ['book-issues'] });
            }
        });
    },

    useReturnBook: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (issueId: number) => {
                const { data } = await api.post<BookIssue>(`/library/return/${issueId}`);
                return data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['books'] });
                queryClient.invalidateQueries({ queryKey: ['book-issues'] });
            }
        });
    }
};
