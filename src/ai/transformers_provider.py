import structlog
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from src.ai.base import LLMProvider
from src.ai.schemas import ChatRequest, ChatResponse
from src.core.config import settings

logger = structlog.get_logger()


class TransformersProvider(LLMProvider):
    def __init__(self) -> None:
        self.model_name = settings.transformers_model
        logger.info("Loading model", model=self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            dtype=torch.float32,
            low_cpu_mem_usage=True,
        )
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        logger.info("Model loaded", model=self.model_name)
        self.model = self.model.to("cpu")

    async def chat(self, request: ChatRequest) -> ChatResponse:
        messages = [{"role": m.role, "content": m.content} for m in request.messages]

        prompt = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )

        inputs = self.tokenizer(prompt, return_tensors="pt")

        output_ids = self.model.generate(
            **inputs,
            max_new_tokens=request.max_tokens,
            temperature=request.temperature,
            do_sample=True,
            pad_token_id=self.tokenizer.pad_token_id,
        )

        response = self.tokenizer.decode(
            output_ids[0][inputs.input_ids.shape[1] :],
            skip_special_tokens=True,
        )

        return ChatResponse(content=response.strip(), model=self.model_name)
