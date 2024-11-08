from .constants import BASE_URL, INPUT_EMBEDDINGS_METADATA, SAT_TOKEN
from .datatypes import CondensePayload, ClientResponse
import httpx
import os
import re
from transformers import AutoTokenizer
from huggingface_hub import HfApi
from safetensors.torch import load_model
import torch.nn as nn
import torch
import base64
import io
import numpy as np
import torch


def base64_to_tensor(base64_str: str) -> torch.Tensor:
    decoded = base64.b64decode(base64_str)
    buf = io.BytesIO(decoded)
    return torch.from_numpy(np.load(buf).astype(np.float32))


class CondenseClient:
    def __init__(self, model_name: str, api_key: str = "", base_url: str = ""):
        if model_name not in INPUT_EMBEDDINGS_METADATA:
            raise ValueError(f"Model {model_name} not supported")
        api_key = api_key or os.getenv("CONDENSE_API_KEY")
        if not api_key:
            raise ValueError("API key is required")
        self.model_name = model_name
        self.base_url = base_url or BASE_URL
        self.api_key = api_key
        self.headers = {"user-api-key": api_key}
        self.client = httpx.Client(base_url=self.base_url)
        self.tokenizer = AutoTokenizer.from_pretrained(
            INPUT_EMBEDDINGS_METADATA[model_name]["repo_id"]
        )
        self.hf_api = HfApi()
        self.embedding_file = self.hf_api.hf_hub_download(
            repo_id=INPUT_EMBEDDINGS_METADATA[model_name]["repo_id"],
            filename=INPUT_EMBEDDINGS_METADATA[model_name]["path_in_repo"],
        )
        self.embeddings = nn.Embedding(
            **INPUT_EMBEDDINGS_METADATA[model_name]["params"]
        )
        load_model(self.embeddings, self.embedding_file)
        print(f"Loaded embeddings from {self.embedding_file}")
        print(f"Initialized CondenseClient for {model_name}")

    @torch.no_grad()
    def create_condensed_tokens(
        self,
        messages: list[dict],
        tier: str,
        miner_uid: int = -1,
        top_incentive: float = 0.9,
        timeout: int = 32,
    ) -> ClientResponse:
        messages_str = self.tokenizer.apply_chat_template(messages, tokenize=False)
        if SAT_TOKEN not in messages_str:
            context = messages_str
            prompt = ""
        else:
            context, prompt = re.split(re.escape(SAT_TOKEN), messages_str)

        payload = CondensePayload(
            context=context,
            tier=tier,
            target_model=self.model_name,
            miner_uid=miner_uid,
            top_incentive=top_incentive,
        )
        response = self.client.post(
            "/api/organic",
            headers=self.headers,
            json=payload.model_dump(),
            timeout=timeout,
        )
        response.raise_for_status()
        condensed_tokens = response.json()["compressed_tokens_b64"]
        condensed_tokens = base64_to_tensor(condensed_tokens)
        prompt_embeds = None
        inputs_embeds = None
        if prompt:
            prompt_ids = self.tokenizer(prompt, return_tensors="pt")["input_ids"]
            prompt_embeds = self.embeddings(prompt_ids)
            prompt_embeds = prompt_embeds.squeeze(0)
            inputs_embeds = torch.cat([condensed_tokens, prompt_embeds], dim=0)
            inputs_embeds = inputs_embeds.unsqueeze(0)
        print(f"Condensed into {condensed_tokens.shape} tokens")
        return ClientResponse(
            condensed_tokens=condensed_tokens,
            prompt_tokens=prompt_embeds,
            inputs_embeds=inputs_embeds,
        )


class AsyncCondenseClient:
    def __init__(self, model_name: str, api_key: str = "", base_url: str = ""):
        if model_name not in INPUT_EMBEDDINGS_METADATA:
            raise ValueError(f"Model {model_name} not supported")
        api_key = api_key or os.getenv("CONDENSE_API_KEY")
        if not api_key:
            raise ValueError("API key is required")
        self.model_name = model_name
        self.base_url = base_url or BASE_URL
        self.api_key = api_key
        self.headers = {"user-api-key": api_key}
        self.client = httpx.AsyncClient(base_url=self.base_url)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.hf_api = HfApi()
        self.embedding_file = self.hf_api.hf_hub_download(
            repo_id=INPUT_EMBEDDINGS_METADATA[model_name]["repo_id"],
            filename=INPUT_EMBEDDINGS_METADATA[model_name]["path_in_repo"],
        )
        self.embeddings = nn.Embedding(
            **INPUT_EMBEDDINGS_METADATA[model_name]["params"]
        )
        load_model(self.embeddings, self.embedding_file)
        print(f"Loaded embeddings from {self.embedding_file}")
        print(f"Initialized AsyncCondenseClient for {model_name}")

    async def create_condensed_tokens(
        self,
        messages: list[dict],
        tier: str,
        miner_uid: int = -1,
        top_incentive: float = 0.9,
        timeout: int = 32,
    ) -> ClientResponse:
        messages_str = self.tokenizer.apply_chat_template(messages, tokenize=False)
        if SAT_TOKEN not in messages_str:
            context = messages_str
            prompt = ""
        else:
            context, prompt = re.split(re.escape(SAT_TOKEN), messages_str)

        payload = CondensePayload(
            context=context,
            tier=tier,
            target_model=self.model_name,
            miner_uid=miner_uid,
            top_incentive=top_incentive,
        )
        response = await self.client.post(
            "/api/organic",
            headers=self.headers,
            json=payload.model_dump(),
            timeout=timeout,
        )
        response.raise_for_status()
        condensed_tokens = response.json()["condensed_tokens_b64"]
        condensed_tokens = base64_to_tensor(condensed_tokens)
        prompt_embeds = None
        inputs_embeds = None
        if prompt:
            prompt_ids = self.tokenizer(prompt, return_tensors="pt")["input_ids"]
            prompt_embeds = self.embeddings(prompt_ids)
            prompt_embeds = prompt_embeds.squeeze(0)
            inputs_embeds = torch.cat([condensed_tokens, prompt_embeds], dim=0)
            inputs_embeds = inputs_embeds.unsqueeze(0)
        print(f"Condensed into {condensed_tokens.shape} tokens")
        return ClientResponse(
            condensed_tokens=condensed_tokens,
            prompt_tokens=prompt_embeds,
            inputs_embeds=inputs_embeds,
        )
