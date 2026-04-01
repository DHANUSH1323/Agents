---
title: GAIA Agent
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.25.2
app_file: app.py
pinned: false
hf_oauth: true
hf_oauth_expiration_minutes: 480
---

# GAIA Agent

A smolagents-based agent for the GAIA benchmark evaluation.

## Architecture

- **Model:** Qwen/Qwen2.5-72B-Instruct via HuggingFace Inference API
- **Framework:** smolagents CodeAgent
- **Tools:**
  - DuckDuckGo web search
  - GAIA file reader (text, Excel, PDF)
  - Calculator
  - String reverse
