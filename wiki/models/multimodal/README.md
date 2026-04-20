# Multimodal Models

Documentation of AI models that process and generate multiple modalities (vision, language, audio, video).

---

## Quick Navigation

| Section | Description |
|---------|-------------|
| [Overview](#overview) | Multimodal AI landscape |
| [Vision-Language](#vision-language-models) | Image understanding models |
| [Video Models](#video-understanding) | Video processing models |
| [Audio Models](#audio-speech-models) | Speech and audio models |
| [Unified Models](#unified-multimodal) | Omni-modal models |
| [By Lab](#by-lab) | Models organized by lab |

---

## Overview

Multimodal models integrate multiple data types (text, images, audio, video) enabling:
- **Image Understanding:** Captioning, visual QA, object detection
- **Video Analysis:** Temporal understanding, action recognition
- **Audio Processing:** Speech recognition, audio generation
- **Cross-Modal Generation:** Text-to-image, image-to-text

### Current Trends (2025-2026)
- Native multimodal training (vs. bolted-on vision)
- Longer video context windows
- Improved video generation quality
- Audio-language integration

---

## Vision-Language Models

### Leading Models

| Model | Lab | Release | Image | Video | Context |
|-------|-----|---------|-------|-------|---------|
| GPT-4o | OpenAI | May 2024 | Yes | Limited | 128K |
| Claude 3.7 Sonnet | Anthropic | Feb 2025 | Yes | No | 200K |
| Gemini 2.0 Pro | Google | Feb 2025 | Yes | Yes | 2M |
| Llama 3.2 Vision | Meta | Sep 2024 | Yes | No | 128K |
| Pixtral 12B | Mistral | Sep 2024 | Yes | No | 128K |

### Capabilities
- **Visual Question Answering:** Answer questions about images
- **Image Captioning:** Generate descriptive captions
- **Document Understanding:** OCR, chart/table analysis
- **Visual Reasoning:** Multi-step visual reasoning

### Benchmarks
- **MMMU:** College-level multimodal problems
- **MMBench:** Comprehensive VLM evaluation
- **ChartQA:** Chart understanding
- **DocVQA:** Document visual QA

---

## Video Understanding

### Leading Models

| Model | Lab | Release | Input Length | Key Feature |
|-------|-----|---------|--------------|-------------|
| Gemini 2.0 Pro | Google | Feb 2025 | 2M tokens | Native video |
| Sora | OpenAI | Dec 2024 | 60s | Video generation |
| VideoPoet | Google | 2024 | Various | Video generation |
| VILA | NVIDIA | 2024 | 1 hour+ | Efficient training |

### Capabilities
- **Video Captioning:** Describe video content
- **Temporal Reasoning:** Understand events over time
- **Action Recognition:** Identify actions in video
- **Video QA:** Answer questions about video content

---

## Audio & Speech Models

### Speech Recognition & Synthesis

| Model | Lab | Type | Key Feature |
|-------|-----|------|-------------|
| Whisper v3 | OpenAI | ASR | Multilingual, robust |
| Gemini 2.0 | Google | ASR/TTS | Native audio |
| GPT-4o Audio | OpenAI | Audio | Native audio I/O |
| SoundStream | Google | Audio Codec | Neural compression |

### Capabilities
- **Speech-to-Text:** Transcription with timestamps
- **Text-to-Speech:** Natural voice synthesis
- **Audio Understanding:** Music, environmental sounds
- **Voice Cloning:** Speaker adaptation

---

## Unified Multimodal

Models designed from the ground up for multiple modalities:

### Gemini 2.0 Series (Google)
- Native multimodal architecture
- Text, image, audio, video in single model
- Up to 2M token context

### GPT-4o (OpenAI)
- Omni-modal capabilities
- Real-time audio interaction
- Unified token space

### Llama 3.2 Vision (Meta)
- Open vision-language model
- 11B and 90B variants
- Tool use with vision

---

## By Lab

### [OpenAI](../../labs/openai.md)
- GPT-4o (Vision + Audio)
- Sora (Video generation)
- DALL-E 3 (Image generation)
- Whisper v3 (Speech)

### [Google DeepMind](../../labs/google.md)
- Gemini 2.0 Pro/Flash (Omni-modal)
- Imagen 3 (Image generation)
- VideoPoet (Video)

### [Meta AI](../../labs/meta.md)
- Llama 3.2 Vision (Vision-Language)
- Audiobox (Audio)
- Movie Gen (Video generation)

### [Mistral AI](../../labs/mistral.md)
- Pixtral (Vision-Language)

---

## Benchmark Performance

### MMMU (Massive Multi-discipline Multimodal Understanding)
| Model | Score | Date |
|-------|-------|------|
| Gemini 2.0 Pro | 82.4% | 2025-02 |
| GPT-4o | 69.1% | 2024-05 |
| Claude 3.7 Sonnet | 68.3% | 2025-02 |
| Llama 3.2 90B Vision | 68.0% | 2024-09 |

### MMBench
| Model | Score | Date |
|-------|-------|------|
| Gemini 2.0 Pro | 89.2% | 2025-02 |
| GPT-4o | 83.4% | 2024-05 |
| Claude 3.7 Sonnet | 81.5% | 2025-02 |

---

## Tracked Models

*Individual model pages will be created here*

### Vision-Language
- [ ] GPT-4o Vision
- [ ] Claude 3.7 Vision
- [ ] Gemini 2.0 Vision
- [ ] Llama 3.2 Vision 90B
- [ ] Pixtral 12B

### Video Models
- [ ] Gemini 2.0 Video
- [ ] Sora
- [ ] VideoPoet

### Audio Models
- [ ] Whisper v3
- [ ] GPT-4o Audio
- [ ] Gemini 2.0 Audio

---

## Related Categories

- [LLMs](../llms/) - Text-only language models
- [Reasoning Models](../reasoning/) - Multimodal reasoning
- [Benchmarks](../../benchmarks/) - Multimodal evaluation
- [Architectures](../../architectures/) - Multimodal architectures

---

## Template

To add a new multimodal model entry, use the [model template](../../templates/model-template.md).

---

*Last updated: 2026-04-19 by AI Model Research Team*