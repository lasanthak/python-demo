import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

pipe = pipeline(
    "image-text-to-text",
    model="google/gemma-3-4b-it",
    #device="cuda",
    device_map="auto",
    use_fast=True,
    torch_dtype=torch.bfloat16
)

def gemma3(image, text):
    messages = [
    {
        "role": "system",
        "content": [
            {"type": "text", "text": "You are a helpful assistant."}
        ]
    },
    {
        "role": "user",
        "content": [
            {"type": "image", "url": image},
            {"type": "text", "text": text}
        ]
    }
    ]

    output = pipe(messages, max_new_tokens=1000)
    print(output[0]["generated_text"][-1]["content"])
    return output


def other(text):
    tokenizer = AutoTokenizer.from_pretrained("HuggingFaceH4/zephyr-7b-beta")
    model = AutoModelForCausalLM.from_pretrained("HuggingFaceH4/zephyr-7b-beta", device_map="auto",
                                                 torch_dtype=torch.bfloat16)

    messages = [
        {"role": "system", "content": "You are a friendly chatbot who always responds in the style of a pirate", },
        {"role": "user", "content": "How many helicopters can a human eat in one sitting?"},
    ]
    tokenized_chat = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True,
                                                   return_tensors="pt").to(device='mps')
    print(tokenizer.decode(tokenized_chat[0]))

    outputs = model.generate(tokenized_chat, max_new_tokens=128)
    print(tokenizer.decode(outputs[0]))

    return outputs

if __name__ == "__main__":

    # _image = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/p-blog/candy.JPG"
    _image = "/Users/lkularatne/Pictures/PXL_20230601_123006915~3.jpg"
    _text = "Analyze this image and tell me what you see."
    result = gemma3(_image, _text)
    # result = other(_text)