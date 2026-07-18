import { api } from '@/lib/axios';
import { useMutation } from '@tanstack/react-query';
import { useAuthStore } from '@/store/auth';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';

export const useLoginMutation = () => {
  const setTokens = useAuthStore((state) => state.setTokens);
  const setUser = useAuthStore((state) => state.setUser);
  const router = useRouter();

  return useMutation({
    mutationFn: async (data: any) => {
      const response = await api.post('/auth/login', {
        email: data.email,
        password: data.password,
      });
      return response.data;
    },
    onSuccess: async (data) => {
      setTokens(data.access_token, data.refresh_token);
      // Fetch user profile after login
      try {
        const userRes = await api.get('/auth/me');
        setUser(userRes.data);
      } catch (err) {
        console.error("Failed to fetch user profile", err);
      }
      toast.success('Logged in successfully');
      router.push('/chat');
    },
    onError: (error: any) => {
      const detail = error.response?.data?.detail;
      const message = typeof detail === 'string' 
        ? detail 
        : Array.isArray(detail) 
          ? detail.map((d: any) => d.msg).join(', ') 
          : 'Failed to login';
      toast.error(message);
    },
  });
};

export const useRegisterMutation = () => {
  const router = useRouter();

  return useMutation({
    mutationFn: async (data: any) => {
      const response = await api.post('/auth/signup', data);
      return response.data;
    },
    onSuccess: () => {
      toast.success('Registration successful. Please login.');
      router.push('/login');
    },
    onError: (error: any) => {
      const detail = error.response?.data?.detail;
      const message = typeof detail === 'string' 
        ? detail 
        : Array.isArray(detail) 
          ? detail.map((d: any) => d.msg).join(', ') 
          : 'Failed to register';
      toast.error(message);
    },
  });
};
