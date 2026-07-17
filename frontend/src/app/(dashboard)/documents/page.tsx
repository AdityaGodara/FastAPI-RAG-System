"use client";

import { UploadZone } from "@/features/documents/components/upload-zone";
import { DocumentList } from "@/features/documents/components/document-list";

export default function DocumentsPage() {
  return (
    <div className="flex-1 space-y-6 p-8 max-w-5xl mx-auto">
      <div>
        <h1 className="text-3xl font-semibold tracking-tight">Documents</h1>
        <p className="text-muted-foreground mt-2">
          Upload and manage your knowledge base. Documents are processed automatically.
        </p>
      </div>

      <div className="grid gap-8">
        <section>
          <UploadZone />
        </section>
        
        <section>
          <h2 className="text-xl font-semibold tracking-tight mb-4">Your Files</h2>
          <DocumentList />
        </section>
      </div>
    </div>
  );
}
