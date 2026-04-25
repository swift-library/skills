---
name: natural-language-patterns
description: Use this skill for Natural Language and Translation framework implementation and review across NLTokenizer, NLLanguageRecognizer, NLTagger, NLEmbedding, NLContextualEmbedding, NLModel, gazetteers, language constraints, token options, asset requests, translationPresentation, translationTask, TranslationSession, LanguageAvailability, batch translation, replacement actions, and deterministic text-analysis pipelines. Do not use for Foundation Models generation, Speech transcription, Core ML internals, server translation APIs, or interface copywriting.
---

# Natural Language Patterns

## Purpose

Guide implementation, review, and troubleshooting for Apple's Natural Language
and Translation frameworks, including deterministic text analysis, language
metadata, embeddings, custom natural-language models, and in-app translation.

## When To Use

- Tokenizing text with `NLTokenizer` or tagging text with `NLTagger`.
- Detecting language with `NLLanguageRecognizer`, constraints, hints, or
  hypotheses.
- Using `NLEmbedding`, `NLContextualEmbedding`, `NLModel`, gazetteers, or
  custom text classifiers/taggers.
- Adding Translation framework UI or programmatic translation with
  `TranslationSession`, `translationTask`, or `LanguageAvailability`.
- Reviewing asset downloads, locale/language availability, deterministic text
  fixtures, threading, and pipeline boundaries.

## When Not To Use

- Do not use for Foundation Models generation or prompt/session behavior; use
  `foundation-models-patterns`.
- Do not use for Speech framework transcription; use `speech-patterns`.
- Do not use for Core ML model internals unless `NLModel` is only a thin
  wrapper around a model artifact that needs Core ML review.
- Do not use for server translation APIs, copywriting, or interface text
  editing; use `interface-writing` for UI text.
- Do not invent language coverage, translation availability, asset behavior, or
  thread-safety details. Verify current Apple documentation and the local SDK.

## Inputs To Inspect

- Natural Language imports, tokenizer, recognizer, tagger, embedding, model,
  gazetteer, and text pipeline code.
- Locale, language hints, constraints, token options, tag schemes, asset
  requests, and fallback behavior.
- Translation framework modifiers, sessions, configuration, batch requests,
  replacement actions, and language-availability checks.
- Test fixtures, user-entered text boundaries, privacy/logging behavior, and UI
  state reached from analysis or translation.

## Workflow

1. Separate deterministic text analysis from generative language tasks.
2. Choose the narrowest Natural Language API for the job: tokenizer, language
   recognizer, tagger, embedding, contextual embedding, or model.
3. Make language, locale, and script assumptions explicit. Use constraints or
   hints only when the product has reliable context.
4. Keep `NLTagger` and mutable analyzer instances confined to one thread or
   actor when documentation requires it.
5. For embeddings and custom models, verify asset availability, language
   support, input normalization, and fallback behavior.
6. For Translation, check language availability before offering the feature and
   use `prepareTranslation()` when the product needs a deliberate asset prompt.
7. Validate with deterministic fixtures that cover expected languages, mixed
   script input, short text, empty text, and unsupported cases.

## Review Rules

- Do not use language detection confidence as identity, region, or compliance
  evidence.
- Do not hide unsupported language behavior behind generic errors.
- Do not run Translation tasks without user-visible state for unavailable
  languages, asset download, cancellation, and failure.
- Do not store or log sensitive analyzed text unless the feature explicitly
  needs it.
- Treat language coverage, Translation API behavior, and newer embedding/model
  APIs as current-source gated.

## Validation

- Build the affected app/package against the local SDK.
- Run text fixtures for each supported language, mixed-language input, short
  input, empty input, and unsupported input.
- Test asset-missing, asset-downloading, unavailable-language, cancellation,
  and failed-translation states when in scope.
- Verify tokenizer/tagger/model instance ownership under concurrent use.
- Inspect logs, analytics, and snapshots for accidental raw-text leakage.

## Output

For implementation or review work, return:

1. Natural Language or Translation surface and language assumptions
2. Tokenization, tagging, embedding, model, or translation findings
3. Asset, availability, privacy, and threading boundaries
4. Validation run or still needed
5. Current-source assumptions for version-specific behavior
