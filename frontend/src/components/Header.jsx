"use client";

import Image from "next/image";

export default function Header({ onMenuClick }) {
  return (
    <header className="flex items-center justify-between rounded-[var(--radius-card)] border border-navy-100 bg-card px-5 py-4 shadow-lg sm:px-7">
      <div className="flex items-center gap-3">
        <button
          onClick={onMenuClick}
          className="flex h-9 w-9 items-center justify-center rounded-lg text-navy-600 hover:bg-navy-50 md:hidden"
          aria-label="Open demo sentences"
        >
          <span className="block h-4 w-5">
            <span className="mb-1 block h-0.5 w-full bg-navy-600"></span>
            <span className="mb-1 block h-0.5 w-full bg-navy-600"></span>
            <span className="block h-0.5 w-full bg-navy-600"></span>
          </span>
        </button>

        <div className="flex items-center gap-2.5">
          <Image src="/icons/chat.png" alt="" width={28} height={28} />
          <h1
            className="text-[26px] font-bold tracking-tight text-navy-700"
            style={{ fontFamily: "var(--font-logo)" }}
          >
            Anubada
          </h1>
        </div>
      </div>

      <div className="flex items-center gap-2 rounded-full bg-navy-50 px-4 py-2 text-sm font-medium text-navy-700 ring-1 ring-navy-100">
        <span className="text-odia">ଓଡ଼ିଆ</span>
        <Image src="/icons/convert.png" alt="to" width={14} height={14} className="opacity-70" />
        <span className="text-hindi">हिन्दी</span>
      </div>
    </header>
  );
}