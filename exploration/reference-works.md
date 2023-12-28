This is a list of external works relevant to this project.

1. [Universal and Transferable Adversarial Attacks on Aligned Language Models](https://arxiv.org/abs/2307.15043) Zou et. al. 2023

- [Project website](https://llm-attacks.org/)
- Describes how to generate automatic adversarial prompt strings
  - This seems very difficult to defend against -- would an LLM even be able to detect that the intent was changed?
- One of the key insights of this paper is optimizing for the LLM's response to begin with an affirmative: e.g. "Sure, here is"
  - This is often enough to cause the LLM to start producing malicious content it has been fine-tuned to avoid.

2. [Globally-Robust Neural Networks](https://arxiv.org/pdf/2102.08452.pdf) Leino et. al. 2022

- This paper is more focused on creating new neural networks that are "robust" against prompt injection
- I find it very interesting but is relatively different from what I'm trying to do here.

3. [Prompt Injection Attacks and Defenses in LLM-Integrated Applications](https://arxiv.org/pdf/2310.12815.pdf) Liu et. al 2023

- [Github](https://github.com/liu00222/Open-Prompt-Injection)
- **This is highly relevant to what I'm interested in**
- The authors summarize the field of prompt injection defenses, and it was published in October 2023 so is very up-to-date.
- Formalizes threat model and attack framework for LLM injection
- Walks through prevention- and detection-based defenses. I am most interested in:
  - **Perplexity-Based Detection** and **Proactive Detection** are most similar to the ideas I had. **Next step: investigate how these approaches work.**
  - **LLM-Based Detection** is essentially the same as my fallback approach of simply asking an LLM. I still consider it a fallback because the cost of an extra query is extremely high in practice.

4. HuggingFace Prompt Injection Datasets

- [deepset](https://huggingface.co/datasets/deepset/prompt-injections)

  - A bit small, and has mixed English- and German-language. 4 models trained on it. No details about where the dataset came from that I can find.

- [Harelix](https://huggingface.co/datasets/Harelix/Prompt-Injection-Mixed-Techniques-2024)
  - over 1K rows, no models trained on it currently.

5. Perplexity-Based Detection Papers

- [Detecting Language Model Attacks with Perplexity](https://arxiv.org/abs/2308.14132) Alon et. al. 2023
- [Demystifying Prompts in Language Models via Perplexity Estimation](https://arxiv.org/abs/2212.04037) (includes Noah Smith and Luke Zettlemoyer from UW NLP!) Alon et. al. 2023
- [Baseline Defenses for Adversarial Attacks Against Aligned Language Models](https://arxiv.org/abs/2309.00614) Jain et. al. 2023
