"use client";

import { useEffect, useRef } from "react";
import { useAppStore } from "@/store/app";
import { useChatHistory } from "@/features/chat/api";
import { useChatStream } from "@/features/chat/hooks/useChatStream";
import { ChatMessage } from "@/features/chat/components/chat-message";
import { ChatInput } from "@/features/chat/components/chat-input";
import { Hexagon } from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";

export default function ChatPage() {
  const selectedConversationId = useAppStore((state) => state.selectedConversationId);
  const { data: history = [], isLoading } = useChatHistory(selectedConversationId);
  const { sendMessage, isStreaming, streamingMessage, streamingSources } = useChatStream(selectedConversationId);
  
  const scrollRef = useRef<HTMLDivElement>(null);
  
  // Auto-scroll
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [history, streamingMessage]);

  if (!selectedConversationId) {
    return (
      <div className="flex h-full flex-col items-center justify-center p-8 text-center text-muted-foreground">
        <div className="flex h-20 w-20 items-center justify-center rounded-full bg-primary/10 mb-6">
          <Hexagon className="h-10 w-10 text-primary" />
        </div>
        <h2 className="text-2xl font-semibold text-foreground mb-2">Welcome to AI Workspace</h2>
        <p className="max-w-md">
          Select an existing conversation from the sidebar or start a new one to begin.
        </p>
      </div>
    );
  }

  return (
    <div className="flex h-full flex-col">
      <ScrollArea className="flex-1">
        <div className="mx-auto flex max-w-3xl flex-col gap-2 p-4 pt-8 pb-32">
          {isLoading ? (
            <div className="flex items-center justify-center h-40 text-muted-foreground text-sm">
              Loading conversation...
            </div>
          ) : history.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-40 mt-20 text-center space-y-4">
              <div className="bg-sidebar-accent p-3 rounded-full">
                <Hexagon className="h-6 w-6 text-primary" />
              </div>
              <div>
                <p className="font-medium text-foreground">How can I help you today?</p>
                <p className="text-sm text-muted-foreground">Ask any question about your uploaded documents.</p>
              </div>
            </div>
          ) : (
            history.map((msg) => (
              <ChatMessage key={msg.id} message={msg} />
            ))
          )}

          {/* Render streaming response */}
          {isStreaming && (
            <ChatMessage 
              message={{
                role: 'assistant',
                content: streamingMessage || 'Thinking...',
                sources: streamingSources
              }} 
            />
          )}
          
          {/* Scroll anchor */}
          <div ref={scrollRef} className="h-1" />
        </div>
      </ScrollArea>
      
      {/* Input Area Overlay */}
      <div className="bg-background/80 backdrop-blur-sm border-t border-transparent p-4 pb-0 mt-auto">
        <ChatInput onSend={sendMessage} disabled={isStreaming} />
      </div>
    </div>
  );
}
