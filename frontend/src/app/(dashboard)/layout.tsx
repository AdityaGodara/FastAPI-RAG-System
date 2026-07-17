"use client";

import { useAppStore } from "@/store/app";
import { Sidebar } from "@/features/conversations/components/sidebar";
import { Menu } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger, SheetTitle } from "@/components/ui/sheet";
import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const isSidebarOpen = useAppStore((state) => state.isSidebarOpen);
  const setSidebarOpen = useAppStore((state) => state.setSidebarOpen);
  const [isMobile, setIsMobile] = useState(false);
  const pathname = usePathname();

  // Handle responsive sidebar behavior
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 1024) {
        setIsMobile(true);
        setSidebarOpen(false);
      } else {
        setIsMobile(false);
        setSidebarOpen(true);
      }
    };

    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, [setSidebarOpen]);

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      {/* Desktop Sidebar */}
      {!isMobile && isSidebarOpen && (
        <div className="w-[280px] flex-shrink-0 border-r border-border bg-sidebar transition-all duration-300">
          <Sidebar />
        </div>
      )}

      {/* Main Content Area */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {/* Mobile Header */}
        {isMobile && (
          <header className="flex h-14 items-center gap-4 border-b border-border bg-background px-4 lg:hidden">
            <Sheet>
              <SheetTrigger
                render={
                  <Button variant="ghost" size="icon" className="md:hidden">
                    <Menu className="h-5 w-5" />
                    <span className="sr-only">Toggle sidebar</span>
                  </Button>
                }
              />
              <SheetContent side="left" className="w-[280px] p-0" aria-describedby="sidebar-description">
                <SheetTitle className="sr-only">Sidebar</SheetTitle>
                <Sidebar />
              </SheetContent>
            </Sheet>
            <div className="flex-1 font-semibold text-sm">
              {pathname === '/documents' ? 'Documents' : 'Chat'}
            </div>
          </header>
        )}
        
        <main className="flex-1 overflow-auto bg-background">
          {children}
        </main>
      </div>
    </div>
  );
}
