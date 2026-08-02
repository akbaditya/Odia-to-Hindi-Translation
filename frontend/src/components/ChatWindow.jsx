"use client";

import { useEffect, useRef } from "react";
import Image from "next/image";
import MessageBubble from "./MessageBubble";

export default function ChatWindow({ messages, loading }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  return (
    <div className="flex-1 overflow-y-auto px-5 py-5 sm:px-8 sm:py-6">
      <div className="mx-auto flex max-w-3xl flex-col gap-3.5">
        {messages.length === 0 && (
          <div className="mt-12 flex flex-col items-center gap-3 text-center">
            <span className="flex h-12 w-12 items-center justify-center rounded-full border border-navy-100 bg-navy-50">
              <Image src="/icons/chat.png" alt="" width={22} height={22} />
            </span>
            <p className="max-w-xs text-sm text-navy-400">
              Type an Odia sentence below, or pick a demo from the sidebar to get started.
            </p>
          </div>
        )}

        {messages.map((msg) => (
          <MessageBubble key={msg.id} role={msg.role} text={msg.text} isError={msg.isError} />
        ))}

        {loading && (
          <div className="flex items-end gap-2.5">
            <span className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full border border-navy-100 bg-navy-50">
              <Image src="/icons/bot.png" alt="Bot" width={16} height={16} />
            </span>
            <div className="flex items-center gap-1 rounded-[var(--radius-bubble)] rounded-bl-md border border-navy-100 bg-navy-50 px-4 py-3 shadow-sm">
              <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-navy-300 [animation-delay:-0.3s]"></span>
              <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-navy-300 [animation-delay:-0.15s]"></span>
              <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-navy-300"></span>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>
    </div>
  );
}