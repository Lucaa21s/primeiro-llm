import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Primeiro LLM — AI Platform",
  description: "Plataforma de IA local com Ollama, RAG, Agentes e Multi-Agentes. Powered by Llama3 e Mistral rodando em GPU local.",
  keywords: ["IA", "LLM", "Ollama", "RAG", "FastAPI", "Agentes"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR" className="h-full dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </head>
      <body className="h-full overflow-hidden antialiased">
        {children}
      </body>
    </html>
  );
}
