<div align="center">
  <img src="./assets/covalent_blueprints_banner.png" alt="Covalent Blueprints Banner" width="100%">
</div>
</br>

<div align="center" text>
<b>Plug-and-play Covalent workflows and service deployments.</b>
</div>
</br>

Covalent Blueprints are pre-configured applications for [Covalent](https://www.covalent.xyz/). Each blueprint is runnable both on its own and as a component in another workflow. See the [catalogue](#blueprints-catalogue) below for a list of available blueprints.

### Example: Deploy a Llama 3 chatbot backend

Run a Llama3 chatbot on H100 GPUs in just a few lines.
```python
from covalent_blueprints import store_secret, save_api_key
from covalent_blueprints_ai import llama_chatbot

# Set credentials
save_api_key("<covalent-cloud-api-key>")
store_secret(name="HF_TOKEN", value="<huggingface-write-token>")

# Initialize a blueprint
bp = llama_chatbot(model_name="meta-llama/Meta-Llama-3-70B-Instruct")

# Customize compute resources (e.g. 2x H100 GPUs)
bp.executors.service_executor.gpu_type = "h100"
bp.executors.service_executor.num_gpus = 2
bp.executors.service_executor.memory = "240GB"

# Run the blueprint
llama_client = bp.run()
```

The [`llama_chatbot`](https://github.com/AgnostiqHQ/covalent-blueprints-ai/blob/main/covalent_blueprints_ai/llama_chatbot/llama_chatbot.py) blueprint returns a Python client for the deployed service.
```python
llama_client.generate(prompt="How are you feeling?", max_new_tokens=100)
```
```
How are you feeling? How are you doing?
I am feeling well, thank you for asking. I am a machine learning model, so I don't have emotions or feelings in the way that humans do.
```

```python
llama_client.generate_message(
    messages=[
        {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
        {"role": "user", "content": "Who are you?"},
    ]
)
```
```
{'role': 'assistant', 'content': "Arrrr, me hearty! Me be Captain Chatterbeard, the scurviest chatbot to ever sail the seven seas o' conversation! Me be here to swab yer decks with me witty banter, me treasure trove o' knowledge, and me trusty cutlass o' clever responses! So hoist the colors, me matey, and set course fer a swashbucklin' good time! What be bringin' ye to these fair waters?"}
```
Release compute resources with a single line.
```python
llama_client.teardown()
```

## Blueprints catalogue

👉 Each link below points to an example notebook.

```bash
pip install -U covalent-blueprints-ai
```

| Blueprint | Description |
|-|-|
| [Image Generator](https://github.com/AgnostiqHQ/covalent-blueprints-ai/blob/main/examples/sdxl_turbo.ipynb) | Deploy a text-to-image generator service.
| [Llama Chatbot](https://github.com/AgnostiqHQ/covalent-blueprints-ai/blob/main/examples/llama_chatbot.ipynb) | Deploy a chatbot backend using a Llama-like model.
| [LoRA fine tuning](https://github.com/AgnostiqHQ/covalent-blueprints-ai/blob/main/examples/lora_fine_tuning.ipynb) | Fine tune and deploy an LLM as a Covalent service.
| [vLLM](https://github.com/AgnostiqHQ/covalent-blueprints-ai/blob/main/examples/vllm_inference.ipynb) | Deploy an LLM using vLLM on Covalent Cloud.
| [NVIDIA Llama RAG](https://github.com/AgnostiqHQ/covalent-blueprints-ai/blob/main/examples/nvidia_llama_rag.ipynb) | Deploy a retrieval-augmented generation (RAG) pipeline using multiple NVIDIA NIMs.

**More coming soon...**

<!-- ### More coming soon...

Stay tuned for more blueprints in the near future! -->

## Contributing

Public contributions will soon be open! In the meantime, please reach out on [Slack](https://covalentworkflows.slack.com/ssb/redirect) to contribute a blueprint.
