from typing import List


def build_context(matches: List[dict], max_tokens: int = 2000) -> str:
    context_parts = []
    total_chars = 0
    char_limit = max_tokens * 4

    for i, match in enumerate(matches):
        text = match.get("text", "").strip()
        if not text:
            continue
        chunk = f"[Source {i+1}]\n{text}"
        if total_chars + len(chunk) > char_limit:
            break
        context_parts.append(chunk)
        total_chars += len(chunk)

    context = "\n\n".join(context_parts)
    print(f"✅ Built context: {len(context_parts)} chunks, ~{total_chars // 4} tokens")
    return context
