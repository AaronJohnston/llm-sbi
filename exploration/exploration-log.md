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

12/28/2023 11:00pm

- I'm finding that models which can run in a reasonable amount of time on my Intel MacBook Pro are not producing a perplexity reliable enough to do what I want.
- I may need to rethink this tool with an inference API in mind, or restrict its use to more powerful hardware. Regardless, it's worth running the experiment with a more powerful model to see if something like this is even possible.
- I can run 7B models in reasonable time if quantized, but I'm having difficulty getting quantized models in a framework that still allows me to extract model loss (Cross-Entropy; so I can calculate perplexity). This might be the next path to explore.

12/29/2023 12:00pm

- Currently my task is getting LLM inference working locally. My requirements are:
  - Able to expose the logits from inference so I can calculate perplexity
  - Does not require running beam search or doing any sampling, which is unnecessary for my use case and would slow things down
  - Able to run a quantized model on the CPU, which is the best I can realistically expect on my current MacBook. GPU tests indicate it is not fast enough to speed up inference, and is unsupported by the vast majority of tooling since it doesn't have CUDA (as an AMD GPU) or ROCM (apparently PyTorch does not support ROCM on MacOS).
- Because of the third requirement, my best option will be a GGUF format model with the quantization of a high-parameter-count model.
- I've evaluated a bunch of libraries for this. The current options are:
  - HuggingFace Transformers - Exposes logits and can calculate loss easily, but does not do well loading quantized CPU models. It seems quantization is largely optimized for GPU use cases only. For example, HF Transformers supports AutoGPTQ natively, but this is for GPU only. HF Transformers can also quantize a model upon download, but (a) this requires downloading the unquantized model which is inefficient (though not a blocker), and (b) it breaks for me because it's implemented assuming CUDA is available (again, GPU only. This is a blocker).
  - llama.cpp - Much more friendly to the GGUF format, and exposes logits. Has an implementation of Perplexity built-in. I could run it in a subprocess and sample Perplexity.
  - llama-cpp-python - Python bindings for llama.cpp. There is an eval_logits function that will expose the logits themselves, and I can write my own Perplexity function using those logits with PyTorch's CrossEntropyLoss. There is an example in [this wrapper class from text-generation-webui](https://github.com/oobabooga/text-generation-webui/blob/main/modules/llamacpp_hf.py) I can base off of.

12/29/2023 11:30pm

- I was able to get Mistral 7B (Quantized) running locally, compute perplexity scores from it, and run a small initial experiment.
  - The initial experiment was too small to be conclusive, although perplexity calculation runs slower than I was hoping, which will make future experimentation hard.
- I went back to the first Perplexity defense paper and it's as I remembered: adversarial prompts can be detected with perplexity, manual jailbreak prompts cannot. That's why they also had to use length. I suspect the classifier approach they use would not be robust.
- I played with many examples of Perplexity and after going back through its calculation I am still convinced it can serve as a good measure of "fluency" in text, provided the model is trained well enough.
- **Next Step**: Re-run this experiment on the full dataset, using the full perplexity calculation (which is normalized via geometric mean). See if there are any trends in perplexity between manual jailbreak prompts and manual benign prompts. Perhaps I can use the perplexity scores on the range of "test" output completions as features, and use a t-SNE algorithm to see if they can be clustered in any way.
  - If that doesn't yield results, can try on a SageMaker GPU with a larger LLM to see if it yields any improvements.
  - And if that doesn't yield results, may be time to move on from perplexity and focus on attention.
