const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Sends an Odia sentence to the backend and returns the Hindi translation.
 * Assumes your FastAPI/Flask backend exposes POST /translate
 * with body { text: "odia sentence" } and returns { translation: "hindi sentence" }
 *
 * Adjust the endpoint path and response key to match your main.py route.
 */
export async function translateText(text) {
  const res = await fetch(`${API_BASE_URL}/translate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });

  if (!res.ok) {
    const errText = await res.text().catch(() => "");
    throw new Error(`Translation failed (${res.status}): ${errText}`);
  }

  const data = await res.json();
  return data.translated_text;
}