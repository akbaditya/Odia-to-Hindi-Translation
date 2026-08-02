"use client";

export default function DemoSidebar({ sentences, onSelect, isOpen, onClose }) {
  return (
    <>
      {isOpen && (
        <div
          className="fixed inset-0 z-30 bg-navy-900/50 md:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={`
          fixed inset-y-3 left-3 z-40 w-72 overflow-hidden rounded-[var(--radius-card)] border border-navy-100 bg-card shadow-lg
          transition-transform duration-200 ease-out
          md:static md:inset-auto md:z-0 md:h-full md:w-full md:translate-x-0
          ${isOpen ? "translate-x-0" : "-translate-x-[120%]"}
        `}
      >
        <div className="flex h-full flex-col">
          <div className="flex items-center justify-between border-b border-navy-100 px-5 py-4">
            <h2 className="text-xs font-semibold uppercase tracking-wider text-navy-400">
              Demo
            </h2>
            <button
              onClick={onClose}
              className="text-navy-400 hover:text-navy-700 md:hidden"
              aria-label="Close"
            >
              ✕
            </button>
          </div>

          <div className="flex flex-1 flex-col gap-1 overflow-y-auto p-3">
            {sentences.map((sentence, i) => (
              <button
                key={i}
                onClick={() => onSelect(sentence)}
                className="rounded-xl border border-transparent px-3.5 py-3 text-left text-odia text-[15px] text-navy-800 transition-colors hover:border-navy-100 hover:bg-navy-50 active:bg-navy-100"
              >
                {sentence}
              </button>
            ))}
          </div>
        </div>
      </aside>
    </>
  );
}