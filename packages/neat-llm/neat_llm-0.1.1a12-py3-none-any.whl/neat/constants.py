from enum import Enum

from neat.exceptions import ModelNotFoundError


class LLMModel(Enum):
    # OpenAI models
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4O_MINI_2024_07_18 = "gpt-4o-mini-2024-07-18"
    GPT_4O = "gpt-4o"
    GPT_4O_2024_08_06 = "gpt-4o-2024-08-06"
    GPT_4O_2024_05_13 = "gpt-4o-2024-05-13"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4_TURBO_PREVIEW = "gpt-4-turbo-preview"
    GPT_4_0125_PREVIEW = "gpt-4-0125-preview"
    GPT_4_1106_PREVIEW = "gpt-4-1106-preview"
    GPT_35_TURBO_1106 = "gpt-3.5-turbo-1106"
    GPT_35_TURBO = "gpt-3.5-turbo"
    GPT_35_TURBO_0301 = "gpt-3.5-turbo-0301"
    GPT_35_TURBO_0613 = "gpt-3.5-turbo-0613"
    GPT_35_TURBO_16K = "gpt-3.5-turbo-16k"
    GPT_35_TURBO_16K_0613 = "gpt-3.5-turbo-16k-0613"
    GPT_4 = "gpt-4"
    GPT_4_0314 = "gpt-4-0314"
    GPT_4_0613 = "gpt-4-0613"
    GPT_4_32K = "gpt-4-32k"
    GPT_4_32K_0314 = "gpt-4-32k-0314"
    GPT_4_32K_0613 = "gpt-4-32k-0613"
    GPT_4_VISION_PREVIEW = "gpt-4-vision-preview"

    # Together AI models
    TOGETHER_META_LLAMA_31_8B = (
        "together_ai/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
    )
    TOGETHER_META_LLAMA_31_70B = (
        "together_ai/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
    )
    TOGETHER_META_LLAMA_31_405B = (
        "together_ai/meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo"
    )
    TOGETHER_META_LLAMA_3_8B = "together_ai/meta-llama/Meta-Llama-3-8B-Instruct-Turbo"
    TOGETHER_META_LLAMA_3_70B = "together_ai/meta-llama/Meta-Llama-3-70B-Instruct-Turbo"
    TOGETHER_META_LLAMA_3_8B_LITE = (
        "together_ai/meta-llama/Meta-Llama-3-8B-Instruct-Lite"
    )
    TOGETHER_META_LLAMA_3_70B_LITE = (
        "together_ai/meta-llama/Meta-Llama-3-70B-Instruct-Lite"
    )
    TOGETHER_GEMMA_2_27B = "together_ai/google/gemma-2-27b-it"
    TOGETHER_GEMMA_2_9B = "together_ai/google/gemma-2-9b-it"
    TOGETHER_DBRX_INSTRUCT = "together_ai/databricks/dbrx-instruct"
    TOGETHER_DEEPSEEK_67B = "together_ai/deepseek-ai/deepseek-llm-67b-chat"
    TOGETHER_GEMMA_2B = "together_ai/google/gemma-2b-it"
    TOGETHER_MYTHOMAX_L2_13B = "together_ai/Gryphe/MythoMax-L2-13b"
    TOGETHER_LLAMA_2_13B = "together_ai/meta-llama/Llama-2-13b-chat-hf"
    TOGETHER_LLAMA_3_8B = "together_ai/meta-llama/Llama-3-8b-chat-hf"
    TOGETHER_LLAMA_3_70B = "together_ai/meta-llama/Llama-3-70b-chat-hf"
    TOGETHER_MISTRAL_7B_V01 = "together_ai/mistralai/Mistral-7B-Instruct-v0.1"
    TOGETHER_MISTRAL_7B_V02 = "together_ai/mistralai/Mistral-7B-Instruct-v0.2"
    TOGETHER_MISTRAL_7B_V03 = "together_ai/mistralai/Mistral-7B-Instruct-v0.3"
    TOGETHER_MIXTRAL_8X7B = "together_ai/mistralai/Mixtral-8x7B-Instruct-v0.1"
    TOGETHER_MIXTRAL_8X22B = "together_ai/mistralai/Mixtral-8x22B-Instruct-v0.1"
    TOGETHER_NOUS_HERMES_2_MIXTRAL = (
        "together_ai/NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO"
    )
    TOGETHER_NOUS_HERMES_2_YI = "together_ai/NousResearch/Nous-Hermes-2-Yi-34B"
    TOGETHER_QWEN_72B = "together_ai/Qwen/Qwen1.5-72B-Chat"
    TOGETHER_QWEN_110B = "together_ai/Qwen/Qwen1.5-110B-Chat"
    TOGETHER_QWEN_2_72B = "together_ai/Qwen/Qwen2-72B-Instruct"
    TOGETHER_STRIPED_HYENA = "together_ai/togethercomputer/StripedHyena-Nous-7B"
    TOGETHER_SOLAR_10_7B = "together_ai/upstage/SOLAR-10.7B-Instruct-v1.0"

    # Mistral models
    MISTRAL_CODESTRAL_LATEST = "mistral/codestral-latest"
    MISTRAL_CODESTRAL_MAMBA_LATEST = "mistral/codestral-mamba-latest"
    MISTRAL_LARGE_LATEST = "mistral/mistral-large-latest"
    MISTRAL_MEDIUM_LATEST = "mistral/mistral-medium-latest"
    MISTRAL_SMALL_LATEST = "mistral/mistral-small-latest"
    MISTRAL_NEMO_12B = "mistral/nemo-12b"
    MISTRAL_OPEN_MISTRAL_7B = "mistral/open-mistral-7b"
    MISTRAL_OPEN_MISTRAL_NEMO = "mistral/open-mistral-nemo"
    MISTRAL_OPEN_MIXTRAL_8X22B = "mistral/open-mixtral-8x22b"
    MISTRAL_OPEN_MIXTRAL_8X7B = "mistral/open-mixtral-8x7b"

    # Anthropic models
    CLAUDE_3_5_SONNET_20240620 = "claude-3-5-sonnet-20240620"
    CLAUDE_3_HAIKU_20240307 = "claude-3-haiku-20240307"
    CLAUDE_3_OPUS_20240229 = "claude-3-opus-20240229"
    CLAUDE_3_5_SONNET = "claude-3-5-sonnet"
    CLAUDE_3_SONNET_20240229 = "claude-3-sonnet-20240229"
    CLAUDE_2_1 = "claude-2.1"
    CLAUDE_2 = "claude-2"
    CLAUDE_INSTANT_1_2 = "claude-instant-1.2"
    CLAUDE_INSTANT_1 = "claude-instant-1"

    # Cohere models
    COMMAND_R = "command-r"
    COMMAND_R_PLUS = "command-r-plus"

    # Groq models
    GROQ_01B_LLAMA32_PREVIEW = "groq/llama-3.2-1b-preview"
    """Speed: 3100 tokens/sec
    Context: 8k tokens
    Input: $0.04 per 1M tokens
    Output: $0.04 per 1M tokens"""

    GROQ_03B_LLAMA32_PREVIEW = "groq/llama-3.2-3b-preview"
    """Speed: 1600 tokens/sec
    Context: 8k tokens
    Input: $0.06 per 1M tokens
    Output: $0.06 per 1M tokens"""

    GROQ_07B_GEMMA = "groq/gemma-7b-it"
    """Speed: 950 tokens/sec
    Context: 8k tokens
    Input: $0.07 per 1M tokens
    Output: $0.07 per 1M tokens"""

    GROQ_08B_LLAMA3 = "groq/llama3-8b-8192"
    """Speed: 1250 tokens/sec
    Context: 8k tokens
    Input: $0.05 per 1M tokens
    Output: $0.08 per 1M tokens"""

    GROQ_08B_LLAMA31_INSTANT = "groq/llama-3.1-8b-instant"
    """Speed: 750 tokens/sec
    Context: 128k tokens
    Input: $0.05 per 1M tokens
    Output: $0.08 per 1M tokens"""

    GROQ_08B_LLAMA3_TOOL = "groq/llama3-groq-8b-8192-tool-use-preview"
    """Speed: 1250 tokens/sec
    Context: 8k tokens
    Input: $0.19 per 1M tokens
    Output: $0.19 per 1M tokens"""

    GROQ_09B_GEMMA2 = "groq/gemma2-9b-it"
    """Speed: 500 tokens/sec
    Context: 8k tokens
    Input: $0.20 per 1M tokens
    Output: $0.20 per 1M tokens"""

    GROQ_11B_LLAMA32_VISION = "groq/llama-3.2-11b-vision-preview"
    """Speed: N/A
    Context: 8k tokens
    Input: $0.18 per 1M tokens
    Output: $0.18 per 1M tokens"""

    GROQ_70B_LLAMA3 = "groq/llama3-70b-8192"
    """Speed: 330 tokens/sec
    Context: 8k tokens
    Input: $0.59 per 1M tokens
    Output: $0.79 per 1M tokens"""

    GROQ_70B_LLAMA31_VERSATILE = "groq/llama-3.1-70b-versatile"
    """Speed: 250 tokens/sec
    Context: 128k tokens
    Input: $0.59 per 1M tokens
    Output: $0.79 per 1M tokens"""

    GROQ_70B_LLAMA3_TOOL = "groq/llama3-groq-70b-8192-tool-use-preview"
    """Speed: 335 tokens/sec
    Context: 8k tokens
    Input: $0.89 per 1M tokens
    Output: $0.89 per 1M tokens"""

    GROQ_90B_LLAMA32_VISION = "groq/llama-3.2-90b-vision-preview"
    """Speed: N/A
    Context: 8k tokens
    Input: $0.90 per 1M tokens
    Output: $0.90 per 1M tokens"""

    GROQ_MIXTRAL_8X7B = "groq/mixtral-8x7b-32768"
    """Speed: 575 tokens/sec
    Context: 32k tokens
    Input: $0.24 per 1M tokens
    Output: $0.24 per 1M tokens"""

    def __init__(self, model_name: str):
        self.model_name = model_name

    @classmethod
    def from_string(cls, model_name: str) -> "LLMModel":
        try:
            return next(model for model in cls if model.model_name == model_name)
        except StopIteration:
            raise ModelNotFoundError(f"Unknown model name: {model_name}")

    def __str__(self):
        return self.model_name
