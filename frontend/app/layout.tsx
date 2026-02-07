import { Navbar } from '@/components/layout/Navbar';
import './globals.css';

export const metadata = {
  title: 'Pantry Oracle - Your AI Cooking Assistant',
  description: 'Gen Z-friendly pantry-aware cooking assistant with Indianization mode',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        <Navbar />
        <main className="container mx-auto">
          {children}
        </main>
      </body>
    </html>
  );
}
