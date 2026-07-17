import { api } from '@/lib/axios';
import { useQuery } from '@tanstack/react-query';

export interface Source {
  document_id: string;
  filename: string;
  chunk_number: number;
  preview: string;
  content: string;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: Source[];
  created_at: string;
}

export const useChatHistory = (conversationId: string | null) => {
  return useQuery<Message[]>({
    queryKey: ['chat', conversationId],
    queryFn: async () => {
      if (!conversationId) return [];
      const { data } = await api.get(`/conversations/${conversationId}/messages`);
      return data;
    },
    enabled: !!conversationId,
  });
};
