"use client";

import { useState } from "react";
import Image from "next/image";

export default function InputBar({ onSend, disabled }) {
  const [text, setText] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (!text.trim() || disabled) return;
    onSend(text);
    setText("");
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="border-t border-navy-100 bg-card px-4 py-3.5 sm:px-6"
    >
      <div className="mx-auto flex max-w-3xl items-center gap-2.5">
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Type an Odia sentence..."
          disabled={disabled}
          className="text-odia flex-1 rounded-[var(--radius-card)] border border-navy-100 bg-navy-50 px-4 py-2.5 text-[15px] text-navy-900 outline-none focus:border-navy-400 focus:ring-2 focus:ring-navy-100 disabled:opacity-60"
        />
        <button
          type="submit"
          disabled={disabled || !text.trim()}
          className="flex h-11 w-11 flex-shrink-0 items-center justify-center rounded-full bg-navy-600 shadow-md transition-colors hover:bg-navy-700 disabled:cursor-not-allowed disabled:bg-navy-200"
          aria-label="Send"
        >
          <Image src="/icons/send.png" alt="" width={18} height={18} />
        </button>
      </div>
    </form>
  );
}