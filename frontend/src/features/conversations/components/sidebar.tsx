"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { Plus, MessageSquare, FileText, Settings, LogOut, MoreVertical, Trash2, Edit2, Hexagon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useAuthStore } from "@/store/auth";
import { useAppStore } from "@/store/app";
import { useConversations, useCreateConversation, useDeleteConversation } from "../api";
import { ThemeToggle } from "@/components/theme-toggle";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const { user, logout } = useAuthStore();
  const { selectedConversationId, setSelectedConversationId } = useAppStore();
  
  const { data: conversations = [], isLoading } = useConversations();
  const createMutation = useCreateConversation();
  const deleteMutation = useDeleteConversation();

  const handleNewChat = () => {
    createMutation.mutate("New Conversation", {
      onSuccess: (data) => {
        setSelectedConversationId(data.id);
        router.push('/chat');
      }
    });
  };

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  return (
    <div className="flex h-full flex-col bg-sidebar text-sidebar-foreground">
      {/* Header */}
      <div className="flex h-14 items-center px-4 border-b border-sidebar-border">
        <Link href="/chat" className="flex items-center gap-2 font-semibold">
          <Hexagon className="h-5 w-5 text-sidebar-primary" />
          <span>AI Workspace</span>
        </Link>
      </div>

      {/* Primary Actions */}
      <div className="p-4">
        <Button onClick={handleNewChat} className="w-full justify-start gap-2" variant="default">
          <Plus className="h-4 w-4" />
          New Conversation
        </Button>
      </div>

      {/* Navigation */}
      <div className="px-3 pb-2">
        <Link href="/documents">
          <Button
            variant={pathname === "/documents" ? "secondary" : "ghost"}
            className="w-full justify-start gap-2 font-normal"
          >
            <FileText className="h-4 w-4" />
            Documents
          </Button>
        </Link>
      </div>

      <div className="px-4 py-2 text-xs font-medium text-muted-foreground uppercase tracking-wider">
        Recent Chats
      </div>

      {/* Conversations List */}
      <ScrollArea className="flex-1 px-3">
        <div className="space-y-1">
          {isLoading ? (
            <div className="p-4 text-sm text-center text-muted-foreground">Loading...</div>
          ) : conversations.length === 0 ? (
            <div className="p-4 text-sm text-center text-muted-foreground">No conversations yet.</div>
          ) : (
            conversations.map((chat) => (
              <div
                key={chat.id}
                className={`group flex items-center justify-between rounded-md px-3 py-2 text-sm transition-colors hover:bg-sidebar-accent hover:text-sidebar-accent-foreground cursor-pointer ${
                  selectedConversationId === chat.id ? "bg-sidebar-accent text-sidebar-accent-foreground font-medium" : ""
                }`}
                onClick={() => {
                  setSelectedConversationId(chat.id);
                  if (pathname !== '/chat') router.push('/chat');
                }}
              >
                <div className="flex items-center gap-2 truncate">
                  <MessageSquare className="h-4 w-4 shrink-0 opacity-70" />
                  <span className="truncate">{chat.title}</span>
                </div>
                
                <DropdownMenu>
                  <DropdownMenuTrigger
                    onClick={(e: React.MouseEvent) => e.stopPropagation()}
                    render={
                      <Button variant="ghost" size="icon" className="h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity">
                        <MoreVertical className="h-4 w-4" />
                      </Button>
                    }
                  />
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem onClick={(e) => { e.stopPropagation(); /* handle rename */ }}>
                      <Edit2 className="mr-2 h-4 w-4" />
                      Rename
                    </DropdownMenuItem>
                    <DropdownMenuItem 
                      className="text-destructive focus:bg-destructive focus:text-destructive-foreground"
                      onClick={(e) => { 
                        e.stopPropagation(); 
                        deleteMutation.mutate(chat.id);
                        if (selectedConversationId === chat.id) setSelectedConversationId(null);
                      }}
                    >
                      <Trash2 className="mr-2 h-4 w-4" />
                      Delete
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            ))
          )}
        </div>
      </ScrollArea>

      {/* User Footer */}
      <div className="mt-auto border-t border-sidebar-border p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3 truncate">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/10 text-primary font-medium uppercase">
              {user?.username?.charAt(0) || user?.email?.charAt(0) || 'U'}
            </div>
            <div className="flex flex-col truncate">
              <span className="truncate text-sm font-medium">{user?.username || 'User'}</span>
              <span className="truncate text-xs text-muted-foreground">{user?.email}</span>
            </div>
          </div>
          <div className="flex items-center gap-1">
            <ThemeToggle />
            <Button variant="ghost" size="icon" onClick={handleLogout} className="h-8 w-8 px-0">
              <LogOut className="h-4 w-4 text-muted-foreground" />
              <span className="sr-only">Log out</span>
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
