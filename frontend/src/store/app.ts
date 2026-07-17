import { create } from 'zustand';

interface AppState {
  isSidebarOpen: boolean;
  selectedConversationId: string | null;
  toggleSidebar: () => void;
  setSidebarOpen: (isOpen: boolean) => void;
  setSelectedConversationId: (id: string | null) => void;
}

export const useAppStore = create<AppState>((set) => ({
  isSidebarOpen: true,
  selectedConversationId: null,
  toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
  setSidebarOpen: (isOpen) => set({ isSidebarOpen: isOpen }),
  setSelectedConversationId: (id) => set({ selectedConversationId: id }),
}));
