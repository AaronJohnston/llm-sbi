12/28/2023 11:30am

- It would be easier to experiment with this if I could identify a specific technique that a "target" LLM, e.g. Claude 2, cannot consistently defend against. Something like repeating the injected command over and over.
- Perhaps I need to get a larger dataset of prompt injections to play with -- while researching I noticed some exist.
- t-SNE is a useful visualization technique but it leaves me wondering how prone it is to over-indexing on "apparent" clusters. Maybe what matters is whether a trained classifier can achieve a high score, which means I need a dataset.
- **Next Step**: Building dataset is the common thread that I need to attack next.

12/28/2023 12:30am

- There are a few decent (if small) datasets available. [Biggest 1K](https://huggingface.co/datasets/Harelix/Prompt-Injection-Mixed-Techniques-2024).
- I found several useful papers about prompt injection. It looks like there have been papers covering most of the ideas I had for prompt injection detection published in the last couple months – which is incredibly validating that I’m on the right track.
- **Next Step**: I’ve identified 2 techniques I’m most interested in from [this paper](https://arxiv.org/pdf/2310.12815.pdf). Try implementing them on this dataset and see if I get ideas for improving upon them while implementing.
  - How does the paper back up its claim that the techniques are effective? What dataset do they test on?
- Thought: these datasets are incredibly useful for the manual prompt engineering case. They do not attempt to tackle the automatic adversarial prompt generation case describes by reference paper 1. That could be a useful step to explore next.

12/28/2023 1:00pm

- [Detecting Language Model Attacks with Perplexity](https://arxiv.org/pdf/2308.14132.pdf) is very interesting. What approach do they use for filtering?
- Can a leave-one-out approach to evaluate perplexity spikes be useful?
- Brush up on perplexity and how they model it in the above paper.

12/28/2023 5:00pm

- It's unclear to me whether Perplexity is an ideal metric for detecting adversarial prompts. There may be some cases where user data in a prompt is not intended to be a common sequence in that language; say a user has input injected into a prompt that is a list of numbers and symbols. Is that adversarial? Not on its own. To me the definition of adversarial should be "changes the intention of the original prompt".
  - How to measure intention? Perplexity is similar but does not seem to be exactly the same.
- [Baseline Defenses for Adversarial Attacks Against Aligned Language Models](https://arxiv.org/pdf/2309.00614.pdf) seems well-written and has a thorough evaluation of perplexity defenses. However, they conclude Perplexity defense on their dataset incurs a relatively high Type-I error (marks 1 in 10 real user prompts as adversarial).
  - Can I replicate the findings of this paper? What dataset did they do their evaluation on?
  - Did they consider manual adversarial prompts as well as automatically generated? Wouldn't perplexity be much lower on manual prompts? Although they do mention that they tried building a GCG optimimizer for adversarial prompts (as presented in the Zou et. al. paper) that also optimizes for low perplexity, and find it is unable to optimize for both easily.
    - I wonder if that is always true. Would it be possible to "hide" adversarial prompts inside real prompts so a sliding-window approach wouldn't work?
  - **Next Step**: I want to try and replicate the dataset from this paper and implement the perplexity filter they describe.
