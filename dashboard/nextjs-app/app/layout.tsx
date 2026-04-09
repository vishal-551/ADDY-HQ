import type { Metadata } from "next";
import "./globals.css";
import { Footer, TopNav } from "@/components/ui";

export const metadata: Metadata = {
  title: "Addy Bot Platform Preview",
  description: "Visual preview for Addy website and dashboards",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <TopNav />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
