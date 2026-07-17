import { api } from '@/lib/axios';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export interface Document {
  id: string;
  filename: string;
  status: 'processing' | 'completed' | 'failed';
  uploaded_at: string;
  size_bytes: number;
}

export const useDocuments = () => {
  return useQuery<Document[]>({
    queryKey: ['documents'],
    queryFn: async () => {
      const { data } = await api.get('/documents');
      return data;
    },
  });
};

export const useUploadDocument = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append('file', file);
      const { data } = await api.post('/documents/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] });
    },
  });
};

export const useDeleteDocument = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      await api.delete(`/documents/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] });
    },
  });
};
