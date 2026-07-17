"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { UploadCloud, File, X } from "lucide-react";
import { useUploadDocument } from "../api";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

export function UploadZone() {
  const uploadMutation = useUploadDocument();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      if (file.type !== "application/pdf") {
        toast.error("Only PDF files are supported");
        return;
      }
      setSelectedFile(file);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "application/pdf": [".pdf"] },
    maxFiles: 1,
  });

  const handleUpload = () => {
    if (!selectedFile) return;
    uploadMutation.mutate(selectedFile, {
      onSuccess: () => {
        toast.success("Document uploaded successfully");
        setSelectedFile(null);
      },
      onError: (err: any) => {
        toast.error(err.response?.data?.detail || "Upload failed");
      },
    });
  };

  return (
    <div className="w-full">
      {!selectedFile ? (
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-10 flex flex-col items-center justify-center cursor-pointer transition-colors ${
            isDragActive ? "border-primary bg-primary/5" : "border-border hover:bg-sidebar-accent"
          }`}
        >
          <input {...getInputProps()} />
          <UploadCloud className="h-10 w-10 text-muted-foreground mb-4" />
          <p className="text-sm font-medium">Click or drag PDF to upload</p>
          <p className="text-xs text-muted-foreground mt-1">
            Max file size: 50MB
          </p>
        </div>
      ) : (
        <div className="border border-border rounded-lg p-6 flex flex-col items-center justify-center">
          <File className="h-10 w-10 text-primary mb-4" />
          <p className="text-sm font-medium truncate max-w-[250px]">{selectedFile.name}</p>
          <p className="text-xs text-muted-foreground mt-1">
            {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
          </p>
          <div className="flex gap-2 mt-6 w-full max-w-[200px]">
            <Button
              variant="outline"
              className="flex-1"
              onClick={() => setSelectedFile(null)}
              disabled={uploadMutation.isPending}
            >
              Cancel
            </Button>
            <Button
              className="flex-1"
              onClick={handleUpload}
              disabled={uploadMutation.isPending}
            >
              {uploadMutation.isPending ? "Uploading..." : "Upload"}
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
