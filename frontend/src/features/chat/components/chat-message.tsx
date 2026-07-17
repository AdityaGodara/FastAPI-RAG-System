"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";
import { Check, Copy } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Message } from "../api";
import { SourceCitation } from "./source-citation";

export function ChatMessage({ message }: { message: Message | { role: 'assistant', content: string, sources?: any[] } }) {
  const isUser = message.role === "user";

  return (
    <div className={`flex w-full py-6 ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`flex max-w-[85%] flex-col gap-2 rounded-2xl px-5 py-4 text-sm ${
          isUser
            ? "bg-primary text-primary-foreground"
            : "bg-sidebar text-sidebar-foreground border border-border shadow-sm"
        }`}
      >
        <div className="prose prose-sm dark:prose-invert max-w-none break-words">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              code({ node, inline, className, children, ...props }: any) {
                const match = /language-(\w+)/.exec(className || "");
                const codeString = String(children).replace(/\n$/, "");
                
                // eslint-disable-next-line react-hooks/rules-of-hooks
                const [isCopied, setIsCopied] = useState(false);

                const handleCopy = () => {
                  navigator.clipboard.writeText(codeString);
                  setIsCopied(true);
                  setTimeout(() => setIsCopied(false), 2000);
                };

                if (!inline && match) {
                  return (
                    <div className="relative group my-4 rounded-md overflow-hidden bg-[#1E1E1E]">
                      <div className="flex items-center justify-between px-4 py-1.5 bg-[#2D2D2D] text-[#D4D4D4] text-xs font-mono">
                        <span>{match[1]}</span>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-6 w-6 hover:bg-[#3D3D3D] text-[#D4D4D4]"
                          onClick={handleCopy}
                        >
                          {isCopied ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
                        </Button>
                      </div>
                      <SyntaxHighlighter
                        {...props}
                        style={vscDarkPlus}
                        language={match[1]}
                        PreTag="div"
                        className="!m-0 !bg-transparent text-[13px]"
                      >
                        {codeString}
                      </SyntaxHighlighter>
                    </div>
                  );
                }
                return (
                  <code className={`${className} bg-primary/10 text-primary rounded px-1.5 py-0.5`} {...props}>
                    {children}
                  </code>
                );
              },
              p: ({ children }) => <p className="mb-4 last:mb-0 leading-7">{children}</p>,
              a: ({ href, children }) => (
                <a href={href} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline underline-offset-4">
                  {children}
                </a>
              ),
              ul: ({ children }) => <ul className="list-disc pl-6 mb-4">{children}</ul>,
              ol: ({ children }) => <ol className="list-decimal pl-6 mb-4">{children}</ol>,
              li: ({ children }) => <li className="mb-1">{children}</li>,
              table: ({ children }) => (
                <div className="overflow-x-auto mb-4 border rounded-md">
                  <table className="w-full text-left border-collapse min-w-[400px]">
                    {children}
                  </table>
                </div>
              ),
              th: ({ children }) => <th className="border-b bg-sidebar-accent px-4 py-2 font-medium">{children}</th>,
              td: ({ children }) => <td className="border-b px-4 py-2">{children}</td>,
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>
        
        {/* Render Source Citations if present */}
        {message.sources && message.sources.length > 0 && (
          <div className="mt-4 pt-4 border-t border-border flex flex-col gap-2">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Sources</span>
            <div className="flex flex-col gap-2">
              {message.sources.map((source, idx) => (
                <SourceCitation key={`${source.document_id}-${idx}`} source={source} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
