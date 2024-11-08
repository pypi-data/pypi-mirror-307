# Copyright 2024 Agnostiq Inc.
"""Source file for testing purposes only.

This script implements a chatbot backend service.
"""
import covalent_cloud as cc

# cc.save_api_key("you-api-key")

ENV_NAME = "llm-peft-lite"

cc.create_env(
    name=ENV_NAME,
    pip=["accelerate", "sentencepiece", "transformers", "covalent-blueprints"],
    wait=True,
)

gpu_executor = cc.CloudExecutor(
    env=ENV_NAME,
    num_cpus=24,
    memory="54 GB",
    time_limit="15 days",
    num_gpus=1,
    gpu_type=cc.cloud_executor.GPU_TYPE.A100,
)


@cc.service(executor=gpu_executor, name="LLM Chatbot Server")
def chatbot_backend(model_path: str, device_map="auto"):
    """Create a Llama2 chatbot server."""

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map=device_map,
        torch_dtype=torch.float16,
        do_sample=True,
    )
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer)
    return {"pipe": pipe}


@chatbot_backend.endpoint("/generate", name="Generate Response")
def generate(pipe, prompt, max_new_tokens=50):
    """Generate a response to a prompt."""
    output = pipe(
        prompt,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        truncation=True,
        temperature=0.9,
    )
    gen_text = output[0]["generated_text"]
    return gen_text


@chatbot_backend.endpoint("/stream", name="Stream Response", streaming=True)
def generate_stream(pipe, prompt, max_new_tokens=200):
    """Generate a response to a prompt, streaming tokens."""

    import torch

    def _starts_with_space(tokenizer, token_id):
        token = tokenizer.convert_ids_to_tokens(token_id)
        return token.startswith("▁")

    model = pipe.model
    tokenizer = pipe.tokenizer
    _input = tokenizer(prompt, return_tensors="pt").to("cuda")

    for output_length in range(max_new_tokens):
        # Generate next token
        output = model.generate(
            **_input,
            max_new_tokens=1,
            do_sample=True,
            temperature=0.9,
            pad_token_id=tokenizer.eos_token_id,
        )
        # Check for stopping condition
        current_token_id = output[0][-1]
        if current_token_id == tokenizer.eos_token_id:
            break
        # Decode token
        current_token = tokenizer.decode(current_token_id, skip_special_tokens=True)
        if _starts_with_space(tokenizer, current_token_id.item()) and output_length > 1:
            current_token = " " + current_token

        yield current_token

        # Update input for next iteration.
        # Output grows in size with each iteration.
        _input = {
            "input_ids": output.to("cuda"),
            "attention_mask": torch.ones(1, len(output[0])).to("cuda"),
        }


info = cc.deploy(chatbot_backend)(model_path="NousResearch/Llama-2-7b-chat-hf")
info = cc.get_deployment(info.function_id, wait=True)
print(info)
print(info.address)
