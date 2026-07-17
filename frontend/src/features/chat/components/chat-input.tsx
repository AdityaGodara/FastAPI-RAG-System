"use client";

import { useRef, useEffect } from "react";
import { Send, Paperclip } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSend, disabled }: ChatInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const adjustHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "auto";
      textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
    }
  };

  useEffect(() => {
    adjustHeight();
  }, []);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleSubmit = () => {
    const content = textareaRef.current?.value.trim();
    if (!content || disabled) return;
    
    onSend(content);
    
    if (textareaRef.current) {
      textareaRef.current.value = "";
      adjustHeight();
    }
  };

  return (
    <div className="relative mx-auto w-full max-w-3xl">
      <div className="relative flex items-end gap-2 rounded-2xl border border-input bg-background p-2 shadow-sm focus-within:ring-1 focus-within:ring-ring">
        <Button variant="ghost" size="icon" className="h-9 w-9 shrink-0 text-muted-foreground mb-1" disabled={disabled}>
          <Paperclip className="h-5 w-5" />
          <span className="sr-only">Attach file</span>
        </Button>
        <Textarea
          ref={textareaRef}
          placeholder="Message AI Workspace..."
          className="min-h-[44px] w-full resize-none border-0 bg-transparent py-3 text-sm shadow-none focus-visible:ring-0 px-0"
          rows={1}
          onInput={adjustHeight}
          onKeyDown={handleKeyDown}
          disabled={disabled}
        />
        <Button 
          size="icon" 
          onClick={handleSubmit} 
          disabled={disabled}
          className="h-9 w-9 shrink-0 rounded-xl mb-1 bg-primary text-primary-foreground hover:bg-primary/90"
        >
          <Send className="h-4 w-4" />
          <span className="sr-only">Send message</span>
        </Button>
      </div>
      <div className="text-center mt-2 pb-2">
        <p className="text-xs text-muted-foreground">
          AI can make mistakes. Consider verifying important information.
        </p>
      </div>
    </div>
  );
}
