from transformers import pipeline
import torch

pipe = pipeline(
    "image-text-to-text",
    model="google/gemma-3-4b-it",
    #device="cuda",
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

    output = pipe(text=messages, max_new_tokens=200)
    print(output[0]["generated_text"][-1]["content"])


if __name__ == "__main__":
    _image = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/p-blog/candy.JPG"
    _text = "What animal is on the candy?"
    result = pipe(_image, _text)
    print(result)