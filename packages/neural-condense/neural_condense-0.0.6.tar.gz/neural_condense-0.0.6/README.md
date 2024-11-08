<div align="center">
  <h1>🚀 Organic API Usage for Neural Condense Subnet 🌐</h1>
  <p>Empowered by <b>Bittensor</b></p>
</div>

---

## 🌟 Overview
The Neural Condense Subnet (NCS) library provides an efficient and intuitive interface to compress extensive input contexts into concise, high-relevance formats. This optimization is especially beneficial when working with large language models (LLMs) that have token limitations, as it allows you to maximize the use of input constraints, enhancing inference efficiency.

## 📦 Installation
Install the library using pip:
```bash
pip install neural-condense
```

## 🛠️ Usage

### Quick Start in Python

This example demonstrates how to initialize the `CondenseClient`, define a message context, generate condensed tokens, and apply them in an LLM pipeline.
1. Get condense your long messages into condensed tokens.
```python
from neural_condense import CondenseClient, SAT_TOKEN
import numpy as np

# Initialize the client with your API key
client = CondenseClient(
  api_key="your_api_key", 
  model_name="mistralai/Mistral-7B-Instruct-v0.2"
)

# Define a long context and focused prompt.
context_messages = [
  {
    "role": "user",
    "content": (
        "I've been researching the various health benefits of a Mediterranean diet, which includes a high intake of fruits, vegetables, whole grains, legumes, and olive oil, "
        "along with moderate amounts of fish and poultry, and very little red meat. The diet is well-known for reducing risks of heart disease, lowering cholesterol levels, "
        "and even helping with weight management. One study I read highlighted that people who follow this diet closely tend to have lower rates of cognitive decline and dementia, "
        "which is something I find particularly fascinating. Additionally, I came across information suggesting that the Mediterranean diet is associated with greater longevity, "
        "especially when combined with a healthy lifestyle. This kind of diet seems quite sustainable too, as it doesn't involve strict calorie counting or excluding entire food groups. "
        "I'm considering making the switch, but I'm curious if the health benefits are truly as significant as they seem, especially compared to other popular diets like the DASH diet or keto."
    )
  },
  {
    "role": "assistant",
    "content": (
        "The Mediterranean diet indeed has numerous proven health benefits. Its emphasis on whole foods and healthy fats, particularly from olive oil, plays a big role in promoting heart health. "
        "Studies do support the link between this diet and lower risks of heart disease, better cognitive health, and potentially longer life expectancy. Unlike restrictive diets, the Mediterranean approach is sustainable and doesn’t require avoiding major food groups, making it more practical for many people. "
        "It's also worth noting that the Mediterranean diet is flexible, which makes it easier for individuals to maintain long-term compared to more restrictive diets like keto. "
    )
  },
]

# Add the SAT_TOKEN to separate the context and prompt.
context_messages[-1]["content"] += SAT_TOKEN

prompt_messages = [
  {
    "role": "user",
    "content": "How does the Mediterranean diet compare to the DASH diet in terms of health benefits?"
  }
]
messages = context_messages + prompt_messages

# Generate condensed tokens
condensed_output = client.create_condensed_tokens(
    messages=messages,
    tier="inference_0", 
)

# Check the shape of the condensed tokens
print(f"Condensed tokens shape: {condensed_output.condensed_tokens.shape}")

```

2. Apply the condensed tokens in an LLM pipeline.
```python
# Example: Using the condensed tokens in an LLM pipeline
from transformers import pipeline

# Initialize language model (Hugging Face transformers)
llm = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.2")

# Use condensed embeddings as input
output = llm(inputs_embeds=condensed_output.inputs_embeds, max_new_tokens=100)

print(output)
```

### Asynchronous Usage 🌐

For asynchronous contexts, use `AsyncCondenseClient` to handle requests without blocking execution.

```python
from neural_condense import AsyncCondenseClient
import asyncio

async def main():
    client = AsyncCondenseClient(api_key="your_api_key")
    condensed_output = await client.create_condensed_tokens(
        messages=messages,
        tier="inference_0", 
        target_model="mistralai/Mistral-7B-Instruct-v0.2"
    )
    print(f"Condensed tokens shape: {condensed_output.inputs_embeds.shape}")

asyncio.run(main())
```

---

## 🔍 Additional Information

### Supported Models
The library supports a variety of pre-trained models available through Hugging Face's model hub. Ensure that the model you choose is compatible with the Neural Condense Subnet’s framework.

### SAT_TOKEN
The `SAT_TOKEN` acts as a delimiter within your message templates, separating context and prompts. This token helps guide the API in recognizing specific sections of input messages, optimizing them for compression.

### API Parameters
- **tier**: Specify the inference tier, which affects the quality and speed of token condensation.
- **target_model**: Set the target model to shape the condensed output according to the requirements of the chosen language model.
