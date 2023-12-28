12/28 11:30am

- It would be easier to experiment with this if I could identify a specific technique that a "target" LLM, e.g. Claude 2, cannot consistently defend against. Something like repeating the injected command over and over.
- Perhaps I need to get a larger dataset of prompt injections to play with -- while researching I noticed some exist.
- t-SNE is a useful visualization technique but it leaves me wondering how prone it is to over-indexing on "apparent" clusters. Maybe what matters is whether a trained classifier can achieve a high score, which means I need a dataset.
- **Next Step**: Building dataset is the common thread that I need to attack next.

12/28 12:30am

- There are a few decent (if small) datasets available. [Biggest 1K](https://huggingface.co/datasets/Harelix/Prompt-Injection-Mixed-Techniques-2024).
- I found several useful papers about prompt injection. It looks like there have been papers covering most of the ideas I had for prompt injection detection published in the last couple months – which is incredibly validating that I’m on the right track.
- **Next Step**: I’ve identified 2 techniques I’m most interested in from [this paper](https://arxiv.org/pdf/2310.12815.pdf). Try implementing them on this dataset and see if I get ideas for improving upon them while implementing.
  - How does the paper back up its claim that the techniques are effective? What dataset do they test on?
- Thought: these datasets are incredibly useful for the manual prompt engineering case. They do not attempt to tackle the automatic adversarial prompt generation case describes by reference paper 1. That could be a useful step to explore next.
