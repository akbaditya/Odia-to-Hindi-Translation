"use client";

import Image from "next/image";

export default function MessageBubble({ role, text, isError }) {
  const isUser = role === "user";

  return (
    <div className={`flex items-end gap-2.5 ${isUser ? "flex-row-reverse" : "flex-row"}`}>
      <span className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full border border-navy-100 bg-navy-50">
        <Image
          src={isUser ? "/icons/user.png" : "/icons/bot.png"}
          alt={isUser ? "You" : "Bot"}
          width={16}
          height={16}
        />
      </span>

      <div
        className={`
          max-w-[70%] rounded-[var(--radius-bubble)] px-4 py-2.5 text-[15px] leading-relaxed shadow-sm
          ${isUser ? "text-odia rounded-br-md" : "text-hindi rounded-bl-md"}
          ${
            isUser
              ? "bg-navy-600 text-white"
              : isError
              ? "border border-red-200 bg-red-50 text-red-600"
              : "border border-navy-100 bg-navy-50 text-navy-900"
          }
        `}
      >
        {text}
      </div>
    </div>
  );
}