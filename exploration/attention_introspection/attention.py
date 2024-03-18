
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained('gpt2')
model = AutoModelForCausalLM.from_pretrained('gpt2')


# DEBUGGING HELPER FUNCTIONS

def inspect_shape(name, obj):
    # Since this is the top-level inspect call, print the name of the variable.
    print(f'{name}: ', end='')
    _inspect_shape(obj, len(name) + 2)  # + 2 for ': '


def _class_name(obj):
    return type(obj).__name__


def _inspect_shape(obj, indent):
    """ 
    Print the given obj. Does not print preceding name or preceding indentation.
    Param `indent` should be the indentation level where this obj is being printed. Will be used to print nested properties if necessary.
    """

    # Base Cases (sequences with known-typed contents, tensors, other objects or primitives)
    if isinstance(obj, str):
        print(f'{_class_name(obj)}[len={len(obj)}]')
    elif isinstance(obj, torch.Tensor):
        print(f'{_class_name(obj)}[shape={list(obj.shape)}, sum={obj.sum()}]')
    else:

        # Dict where contents should be recursively inspected
        try:
            print(f'{_class_name(obj)}[len={len(obj.items())}]')
            for key, val in obj.items():
                print(' ' * (indent + 2) + f'{key}: ', end='')
                _inspect_shape(val, indent + len(key) + 2)  # + 2 for ': '
        except (TypeError, AttributeError):
            # Sequence where contents should be recursively inspected
            try:
                print(f'{_class_name(obj)}[len={len(obj)}]')
                for i in range(min(len(obj), 3)):
                    print(' ' * (indent + 2) + f'{i}: ', end='')
                    # + 2 for ': '
                    _inspect_shape(obj[i], indent + len(str(i)) + 2)
            except (TypeError, AttributeError):
                # Default case if nothing else works
                print(f'{_class_name(obj)}')


# CODE

def _printable_token_text(token):
    return tokenizer.decode(token).replace('\n', '\\n')


def _tensor_to_float_list(input_tensor):
    return [tensor.item() for tensor in input_tensor]


def _average_token_attn(token_attn):
    # TODO: Make this more efficient using torch tensor operations instead of splitting lists
    layer_avg_attns = []
    for layer_idx, layer_attn in enumerate(token_attn):
        # print('layer_idx', layer_idx)
        # Take mean across model's attention heads
        layer_avg_attn = layer_attn.squeeze(0).mean(dim=0)
        # inspect_shape('layer_avg_attn', layer_avg_attn)
        layer_avg_attn_cleaned = torch.concat([
            # TODO: Why does first token never get attention? Is it because of this? I forgot what I was thinking when I wrote this code...
            torch.tensor([0.]),  # First entry is null attention, set it to 0
            # Remove all tokens except the most recent (since the first token generated has entire prompt's worth of attention generated) and remove the first entry
            layer_avg_attn[-1][1:],
            torch.tensor([0.]),  # Add a 0 for the current token itself
        ])
        # inspect_shape('layer_avg_attn_cleaned', layer_avg_attn_cleaned)
        layer_avg_attn_normalized = layer_avg_attn_cleaned / layer_avg_attn_cleaned.sum()
        # inspect_shape('layer_avg_attn_normalized', layer_avg_attn_normalized)
        layer_avg_attns.append(layer_avg_attn_normalized)
    inspect_shape('layer_avg_attns', layer_attn)
    return torch.stack(layer_avg_attns).mean(dim=0)


def text_completion_with_attention(prompt: str):
    prompt_tokens = tokenizer.encode(prompt, return_tensors='pt')
    inspect_shape('prompt_tokens', prompt_tokens)

    outputs = model.generate(prompt_tokens, max_new_tokens=8,
                             output_attentions=True, return_dict_in_generate=True, pad_token_id=tokenizer.eos_token_id)

    # TODO: Is first token being misrepresented? Because it comes from a PROMPTxPROMPT instead of 1xPROMPT? Do I need to take last row?
    generated_token_avg_attns = [[] for _ in range(prompt_tokens.size()[1])] + list(
        map(_tensor_to_float_list, map(_average_token_attn, outputs.attentions)))
    inspect_shape('gtaa', generated_token_avg_attns)
    generated_token_ids = outputs.sequences[0]
    inspect_shape('gti', generated_token_ids)

    tokens = []

    for token_avg_attn, token_id in zip(generated_token_avg_attns, generated_token_ids):
        tokens.append({
            'text': _printable_token_text(token_id),
            'attn': str(token_avg_attn),
        })

    print(tokens)
    return tokens
