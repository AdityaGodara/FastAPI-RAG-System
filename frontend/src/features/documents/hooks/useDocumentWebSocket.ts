import { useEffect, useRef } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { useAuthStore } from '@/store/auth';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const WS_URL = API_URL.replace(/^http/, 'ws');

export const useDocumentWebSocket = () => {
  const queryClient = useQueryClient();
  const token = useAuthStore((state) => state.accessToken);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!token) return;

    // Connect to WebSocket with token
    ws.current = new WebSocket(`${WS_URL}/documents/ws?token=${token}`);

    ws.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'document_status_update') {
          // Update the specific document status in the React Query cache
          queryClient.setQueryData(['documents'], (oldData: any[]) => {
            if (!oldData) return oldData;
            return oldData.map((doc) =>
              doc.id === data.document_id
                ? { ...doc, status: data.status }
                : doc
            );
          });
        }
      } catch (err) {
        console.error('Failed to parse WebSocket message', err);
      }
    };

    ws.current.onclose = () => {
      console.log('WebSocket disconnected');
    };

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [token, queryClient]);
};
