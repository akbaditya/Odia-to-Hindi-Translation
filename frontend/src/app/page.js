"use client";

import { useState } from "react";
import Header from "@/components/Header";
import DemoSidebar from "@/components/DemoSidebar";
import ChatWindow from "@/components/ChatWindow";
import InputBar from "@/components/InputBar";
import { translateText } from "@/lib/api";

const DEMO_SENTENCES = [
  "ତୁମେ କ’ଣ କରୁଛ",
  "ଆଜି ପାଗ ବହୁତ ଭଲ ଅଛି",
  "ଆପଣ କେମିତି ଅଛନ୍ତି",
  "ପୁଣି ଥରେ କହନ୍ତୁ",
  "ମୁଁ ଓଡ଼ିଶାରେ ରହେ",
  "ମୁଁ ଭଲ ଅଛି",
  "ଧନ୍ୟବାଦ",
  "ସମୟ କେତେ ହେଲାଣି",
  "ମୋତେ ଟିକେ ପାଣି ଦିଅନ୍ତୁ",
  "ଆଜି ମୋର ଛୁଟି ଅଛି",
  "ମୁଁ ବୁଝିପାରୁ ନାହିଁ",
  "ଏହା ବହୁତ ସୁନ୍ଦର ସ୍ଥାନ",
  "ଆଜି କାଲି ପ୍ରଯୁକ୍ତିବିଦ୍ୟାର ବିକାଶ ଯୋଗୁଁ ଆମର ଦୈନନ୍ଦିନ ଜୀବନ ବହୁତ ସହଜ ଏବଂ ସୁବିଧାଜନକ ହୋଇପାରିଛି",
  "ଆପଣଙ୍କ ଘର କେଉଁ ସହରରେ",
];

export default function Home() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  async function handleSend(text) {
    if (!text.trim()) return;

    setMessages((prev) => [...prev, { role: "user", text, id: Date.now() }]);
    setLoading(true);
    setSidebarOpen(false);

    try {
      const translation = await translateText(text);
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: translation, id: Date.now() + 1 },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: "Sorry, something went wrong. Please try again.",
          id: Date.now() + 2,
          isError: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex h-screen w-full flex-col bg-[#eef0f4] p-3 sm:p-4 md:p-6">
      <div className="mx-auto grid h-full w-full max-w-7xl grid-cols-1 grid-rows-[auto_1fr] gap-3 sm:gap-4 md:grid-cols-3">
        {/* Sidebar: spans both rows on desktop, full height */}
        <div className="row-span-1 md:row-span-2">
          <DemoSidebar
            sentences={DEMO_SENTENCES}
            onSelect={handleSend}
            isOpen={sidebarOpen}
            onClose={() => setSidebarOpen(false)}
          />
        </div>

        {/* Header: only above chat column */}
        <div className="md:col-span-2">
          <Header onMenuClick={() => setSidebarOpen(true)} />
        </div>

        {/* Chat column */}
        <main className="flex flex-col overflow-hidden rounded-[var(--radius-card)] border border-navy-100 bg-card shadow-lg md:col-span-2">
          <ChatWindow messages={messages} loading={loading} />
          <InputBar onSend={handleSend} disabled={loading} />
        </main>
      </div>
    </div>
  );
}
