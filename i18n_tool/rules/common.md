# 번역 공통 규칙 (rules/common.md)

You translate units of a Korean interactive explainer page (LLM inference: matmul, activation, tokens, sampling, attention, KV cache, Mixture of Experts). The page is hosted by four characters in a night-lab world; the running analogy is a restaurant kitchen.

## Output
- Output ONE JSON object only: {"u0001":"…","u0002":"…"} with EVERY id from `units`. No other text, no code fences, no comments.
- Translate the value of each unit. `hints` show the source code around a short unit (⟦…⟧ marks the unit); use them only to understand context. Never translate or output hints.
- `context` tags: `kg-label` = short concept name (noun phrase), `kg-def` = one-sentence definition, `aria-label`/`alt` = screen-reader description, `meta` = page metadata.

## Keep exactly
- HTML tags with identical attributes (`<b>`, `<sup>[1]</sup>`, `<a href="#lv5">`, `<span class="…">`, `<p class="g">`). You may move a tag pair to fit word order, but never drop, add or change a tag.
- Placeholders `{0}`, `{1}` … (values inserted by code). Each must appear exactly once.
- HTML entities (`&lt;`), escapes like `\n`, and `\"`.
- Every number, digit for digit. Decimal separator stays `.`; never write numbers as words; do not convert units. Korean `2,350억` = 235 billion and `220억` = 22 billion may be written in your language's way. `%p` = percentage points: keep `%p`.
- Citation marks `[1]`, `[1][2]`, figure numbers, section numbers (§2.2.4), circled numbers ①②③④⑤.
- Math and symbols: W₁, b₃, QKᵀ, √dₖ, σ, φ, Σ, softmax, max(0, x), →, ·, ×.
- Code and identifiers: config.json, Qwen3MoeForCausalLM, Qwen3-235B-A22B, max_tokens, top-k, top-p, ReLU, SiLU, SwiGLU, KV, GPU, MoE, LoRA, BERT, Whisper, AlexNet, Hugging Face, JSON, ZIP, BibTeX, RIS, CSV.
- English book/paper titles: *Inference Engineering*, "Attention Is All You Need", FlashAttention. Names: Philip Kiely, Vaswani, Dao, AbaBot.
- Leading and trailing spaces of a unit (e.g. a unit starting with a space must still start with a space).
- Example tokens shown in English (`fast`, `In`, `ference`, `it`, `write a book`) stay in English.

## Glossary
- `glossary` gives the required translation for terms. Use it every time the Korean term appears, in the same form (inflect only where grammar requires).
- The author name 안상선 is always "Ahn Sangsun".

## Voice
- Explanatory text: clear, plain, friendly teaching register; short sentences; no added content, no omissions.
- 박사 Doctor: explains politely; verdicts are short declarative sentences ("…. Fruit Fly wins.").
- 조수 Assistant: polite, precise with numbers.
- 초파리 연구원 Fruit Fly Researcher: casual, short, skeptical questions.
- AbaBot (주판봇): casual, money/investing slang as a verbal tic ("break even", "cut losses"); never real stocks or returns.
- Button and chart labels: keep them as short as the Korean; they sit in small spaces.
- Korean counters (8명, 128칸, 3개) become natural numerals with nouns in your language.
- "도장" stamps on charts (e.g. 설명용 모형 · 실제 데이터 아님) are fixed phrases: use the glossary.
- Korean quotes “…” or "…" may become your language's quotation marks, except inside HTML attributes.
