import os
from tokenizers.implementations import ByteLevelBPETokenizer
from transformers import GPT2Tokenizer

TRAIN_BASE = False
paths = ["python_code.txt"]
save_directory = "tokenizer"
tokenizer = ByteLevelBPETokenizer()

if TRAIN_BASE:
    tokenizer.train(files=paths, vocab_size=52_000, min_frequency=2, special_tokens=[
        "<s>",
        "<pad>",
        "</s>",
        "<unk>",
        "<mask>",
    ])
    os.makedirs(save_directory, exist_ok=True)
    tokenizer.save_model(save_directory)
else:
    # Load the pre-trained tokenizer
    tokenizer = ByteLevelBPETokenizer(
        os.path.join(save_directory, "vocab.json"),
        os.path.join(save_directory, "merges.txt")
    )


inp = "print('Hello world!')"

t = tokenizer.encode(inp)
print(t.tokens)  # Corresponding sub-word tokens
print(t.ids)     # Token IDs

gpt2_tokenizer = GPT2Tokenizer.from_pretrained("tokenizer")
gpt2_tokenizer.add_special_tokens({
    "eos_token": "</s>",
    "bos_token": "<s>",
    "unk_token": "<unk>",
    "pad_token": "<pad>",
    "mask_token": "<mask>",
})

encoded_input = gpt2_tokenizer.encode(inp)
print("GPT-2 Encoded IDs:", encoded_input)
print("GPT-2 Decoded Text:", gpt2_tokenizer.decode(encoded_input))
