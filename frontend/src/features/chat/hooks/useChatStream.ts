import { useState, useCallback } from 'react';
import { useAuthStore } from '@/store/auth';
import { useQueryClient } from '@tanstack/react-query';
import { Message, Source } from '../api';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const useChatStream = (conversationId: string | null) => {
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamingMessage, setStreamingMessage] = useState<string>('');
  const [streamingSources, setStreamingSources] = useState<Source[]>([]);
  const token = useAuthStore((state) => state.accessToken);
  const queryClient = useQueryClient();

  const sendMessage = useCallback(
    async (content: string) => {
      if (!conversationId || !token) return;

      setIsStreaming(true);
      setStreamingMessage('');
      setStreamingSources([]);

      // Optimistically add user message to cache
      const userMessage: Message = {
        id: Date.now().toString(),
        role: 'user',
        content,
        created_at: new Date().toISOString(),
      };

      queryClient.setQueryData(['chat', conversationId], (old: Message[] = []) => [
        ...old,
        userMessage,
      ]);

      try {
        // Fetch a document ID to use for the chat
        const docsResponse = await fetch(`${API_URL}/documents/`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        const docs = await docsResponse.json();
        const completedDocs = docs.filter((d: any) => d.status === 'completed');
        const documentId = completedDocs.length > 0 ? completedDocs[0].id : null;

        if (!documentId) {
          throw new Error('No completed documents found to chat with.');
        }

        const response = await fetch(`${API_URL}/chat/stream`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ 
            content: content,
            question: content,
            conversation_id: conversationId,
            document_id: documentId
          }),
        });

        if (!response.ok) {
          throw new Error('Failed to start stream');
        }

        const reader = response.body?.getReader();
        const decoder = new TextDecoder();

        if (!reader) return;

        let assistantContent = '';
        let sources: Source[] = [];

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value, { stream: true });
          const lines = chunk.split('\n');

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6);
              if (data === '[DONE]') {
                break;
              }
              try {
                const parsed = JSON.parse(data);
                if (parsed.type === 'token') {
                  assistantContent += parsed.content;
                  setStreamingMessage(assistantContent);
                } else if (parsed.type === 'sources') {
                  sources = parsed.sources;
                  setStreamingSources(sources);
                }
              } catch (e) {
                // Ignore parse errors for partial chunks
              }
            }
          }
        }

        // Add final assistant message to cache
        const finalMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: assistantContent,
          sources: sources,
          created_at: new Date().toISOString(),
        };

        queryClient.setQueryData(['chat', conversationId], (old: Message[] = []) => [
          ...old,
          finalMessage,
        ]);
      } catch (error) {
        console.error('Streaming error', error);
      } finally {
        setIsStreaming(false);
        setStreamingMessage('');
        setStreamingSources([]);
      }
    },
    [conversationId, token, queryClient]
  );

  return {
    sendMessage,
    isStreaming,
    streamingMessage,
    streamingSources,
  };
};
