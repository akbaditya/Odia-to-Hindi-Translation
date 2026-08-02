import "./globals.css";

export const metadata = {
  title: "Odia–Hindi Translator",
  description: "Fast, accurate Odia to Hindi translation.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="h-full">{children}</body>
    </html>
  );
}