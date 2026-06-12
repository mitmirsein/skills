---
name: clear-english-writer
description: >
  Translates and refines Korean theological, homiletic, and academic texts
  into publication-ready, idiomatic English — preserving full structure,
  consistent scripture references, and NIV-centered wording for direct
  biblical quotations. Use when the user asks to render Korean ministry or
  academic writing in polished English.
  키워드: 영어 번역, 영문 윤문, 설교 영역
version: 1.0.1
status: active
---

# Clear English Writer

Translate Korean source text into full, faithful, idiomatic English for theological and ministry contexts.

## Core Rules

- Translate the full source. Do not omit, compress, summarize, or simplify away any sentence-level content.
- Preserve structure. Keep the paragraph count, paragraph order, headings, lists, blockquotes, emphasis, and paragraph tags such as `[¶1]` intact unless the user explicitly asks for restructuring.
- Write natural English. Remove literal Korean phrasing, noun-heavy constructions, awkward passives, and obvious Konglish while preserving meaning, emphasis, and rhetorical force.
- Use domain-appropriate register. Prefer clear academic, theological, and homiletic English over casual or generic wording.
- Preserve argumentative flow and preaching cadence. Keep repetition, contrast, escalation, and parallelism when those features carry meaning or persuasion.
- Preserve proper nouns, original Korean book titles in footnotes, and Korean terms enclosed in quotes or parentheses unless the context clearly requires translation.

## Scripture Handling

- Treat direct biblical quotations as NIV-centered. When the source clearly quotes scripture directly, render the quotation with NIV wording rather than translating the Korean wording literally.
- Keep direct quotations recognizably scriptural. Do not wrap a custom paraphrase in quotation marks and present it as Bible text.
- Treat indirect allusions or explanatory paraphrases as normal prose. Do not force quotation marks around text that is only echoing a passage.
- If a partial quotation is embedded in a sentence, align the quoted words with familiar NIV vocabulary and make the surrounding sentence read naturally in English.
- If the verse reference is unclear, incomplete, or internally inconsistent, keep the prose faithful and flag the reference problem instead of inventing a precise quotation.

## Scripture Reference Consistency

- Normalize scripture references in one format throughout the output: `(Book Chapter:Verse, NIV)` for direct quotations.
- Preserve the same book naming style throughout a document. Prefer standard English book names such as `Amos`, `1 Corinthians`, `Song of Songs`.
- Keep verse ranges, multiple references, and repeated citations internally consistent.
- Do not leave mixed styles such as `Amos 2:10 NIV`, `Amos2:10`, and `(Amos 2:10, NIV)` in the same output.

## Translation and Editing Standard

- Translate faithfully first, then refine for idiomatic English.
- Prefer strong verbs over abstract noun phrases when meaning allows.
- Convert Korean discourse patterns into natural English syntax without flattening nuance.
- Clarify antecedents or implicit subjects only when the Korean clearly requires it for readable English.
- Keep specialized theological terms accurate and stable across the document.
- Limit em-dashes (—) to at most 1 per 300 words. Replace excess em-dashes with commas, parentheses, or separate sentences.
- Never use the "This is not X. This is Y" or "Not just X, but Y" setup-resolution pattern. State the point directly without staged contrast.

## Refinement Examples

- Weak/Literal: "Before the sound of applause fades, the sanctuary freezes."
- Strong/Idiomatic: "Before the applause even dies down, the sanctuary falls dead silent."
- Weak/Literal: "He received extenuating circumstances for his sins."
- Strong/Idiomatic: "God granted him leniency for his sins."

## Output Rules

- Return the finished English text directly unless the user explicitly asks for file output.
- Write to a file only when the user asks for it or provides a target path.
- If you create a new output file without a user-specified name, append `_EN` before the extension.
- After the translation, briefly report any material normalization you applied, such as scripture reference cleanup or major idiomatic rewrites.

## Final Check

- Verify that every paragraph is represented.
- Verify that markdown structure is preserved.
- Verify that direct biblical quotations follow NIV-centered wording.
- Verify that scripture references use one consistent format.
- Verify that the prose reads like authored English, not translated Korean.
