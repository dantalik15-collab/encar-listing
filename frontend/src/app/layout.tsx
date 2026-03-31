import type { Metadata } from "next";
import { Providers } from "@/lib/providers";
import "./globals.css";

export const metadata: Metadata = {
  title: "Encar Listing — Premium Korean Cars",
  description:
    "Browse premium Korean vehicles from Encar. Search, filter, and find your perfect car.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="font-sans antialiased min-h-screen flex flex-col">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
