from pydantic import BaseModel
import torch




class CondensePayload(BaseModel):
    context: str
    tier: str
    target_model: str
    miner_uid: int = -1
    top_incentive: float = 0.9


class ClientResponse:
    def __init__(
        self,
        condensed_tokens: torch.Tensor,
        prompt_tokens: torch.Tensor = None,
        inputs_embeds: torch.Tensor = None,
    ):
        self.condensed_tokens = condensed_tokens
        self.prompt_tokens = prompt_tokens
        self.inputs_embeds = inputs_embeds
