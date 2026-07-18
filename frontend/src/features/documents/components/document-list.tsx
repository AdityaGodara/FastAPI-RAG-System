"use client";

import { useDocuments, useDeleteDocument } from "../api";
import { useDocumentWebSocket } from "../hooks/useDocumentWebSocket";
import { FileText, Trash2, Loader2, CheckCircle2, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export function DocumentList() {
  const { data: documents = [], isLoading } = useDocuments();
  const deleteMutation = useDeleteDocument();
  
  // Connect to WebSocket for live status updates
  useDocumentWebSocket();

  if (isLoading) {
    return <div className="text-sm text-muted-foreground">Loading documents...</div>;
  }

  if (documents.length === 0) {
    return (
      <div className="border border-border border-dashed rounded-lg p-12 text-center flex flex-col items-center">
        <FileText className="h-8 w-8 text-muted-foreground mb-4 opacity-50" />
        <p className="text-sm font-medium">No documents yet</p>
        <p className="text-xs text-muted-foreground mt-1">Upload a PDF to get started</p>
      </div>
    );
  }

  return (
    <div className="border border-border rounded-lg overflow-hidden">
      <div className="grid grid-cols-[1fr_120px_150px_60px] gap-4 p-4 border-b border-border bg-sidebar/50 text-xs font-medium text-muted-foreground uppercase tracking-wider">
        <div>Name</div>
        <div>Status</div>
        <div>Date</div>
        <div className="text-right">Actions</div>
      </div>
      <div className="divide-y divide-border">
        {documents.map((doc) => (
          <div key={doc.id} className="grid grid-cols-[1fr_120px_150px_60px] gap-4 p-4 items-center hover:bg-sidebar-accent transition-colors">
            <div className="flex items-center gap-3 truncate pr-4">
              <FileText className="h-4 w-4 text-primary shrink-0" />
              <span className="text-sm font-medium truncate">{doc.filename}</span>
            </div>
            <div>
              {doc.status === 'processing' && (
                <Badge variant="secondary" className="bg-primary/10 text-primary border-primary/20 gap-1.5">
                  <Loader2 className="h-3 w-3 animate-spin" />
                  Processing
                </Badge>
              )}
              {doc.status === 'indexed' && (
                <Badge variant="secondary" className="bg-success/10 text-success border-success/20 gap-1.5">
                  <CheckCircle2 className="h-3 w-3" />
                  Indexed
                </Badge>
              )}
              {doc.status === 'failed' && (
                <Badge variant="secondary" className="bg-destructive/10 text-destructive border-destructive/20 gap-1.5">
                  <AlertCircle className="h-3 w-3" />
                  Failed
                </Badge>
              )}
            </div>
            <div className="text-sm text-muted-foreground">
              {new Date(doc.created_at).toLocaleDateString()}
            </div>
            <div className="text-right">
              <Button
                variant="ghost"
                size="icon"
                className="text-muted-foreground hover:text-destructive hover:bg-destructive/10"
                onClick={() => deleteMutation.mutate(doc.id)}
                disabled={deleteMutation.isPending && deleteMutation.variables === doc.id}
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
