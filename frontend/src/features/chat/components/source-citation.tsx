"use client";

import { useState } from "react";
import { ChevronDown, ChevronRight, FileText } from "lucide-react";
import { Source } from "../api";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";
import { Button } from "@/components/ui/button";

interface SourceCitationProps {
  source: Source;
}

export function SourceCitation({ source }: SourceCitationProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <Collapsible open={isOpen} onOpenChange={setIsOpen} className="w-full max-w-2xl mt-2">
      <div className="flex items-center gap-2 rounded-md border border-border bg-sidebar px-3 py-2 text-sm text-muted-foreground hover:bg-sidebar-accent transition-colors">
        <FileText className="h-4 w-4 shrink-0 text-primary" />
        <span className="truncate font-medium flex-1">{source.filename}</span>
        <span className="text-xs shrink-0 bg-secondary px-2 py-0.5 rounded">Chunk {source.chunk_number}</span>
        <CollapsibleTrigger
          render={
            <Button variant="ghost" size="icon" className="h-6 w-6 shrink-0 p-0">
              {isOpen ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
              <span className="sr-only">Toggle</span>
            </Button>
          }
        />
      </div>
      <CollapsibleContent className="mt-1 overflow-hidden">
        <div className="rounded-md border border-border bg-sidebar/50 p-3 text-xs leading-relaxed text-muted-foreground">
          {source.content || source.preview}
        </div>
      </CollapsibleContent>
    </Collapsible>
  );
}
