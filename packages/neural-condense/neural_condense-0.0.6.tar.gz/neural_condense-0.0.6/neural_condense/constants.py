BASE_URL = "https://ncs-client.condenses.ai"
SAT_TOKEN = "START-ACTIVATE-TOKEN"
EAT_TOKEN = "END-ACTIVATE-TOKEN"

INPUT_EMBEDDINGS_METADATA = {
    "mistralai/Mistral-7B-Instruct-v0.2": {
        "repo_id": "Condense-AI/Mistral-7B-Instruct-v0.2",
        "path_in_repo": "input_embeddings.safetensors",
        "params": {
            "num_embeddings": 32000,
            "embedding_dim": 4096,
        },
    }
}
