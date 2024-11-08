from shy_sh.settings import settings
from functools import lru_cache


@lru_cache
def get_llm():
    llm = None
    match settings.llm.provider:
        case "openai":
            from langchain_openai import ChatOpenAI

            llm = ChatOpenAI(
                model=settings.llm.name,
                temperature=settings.llm.temperature,
                api_key=settings.llm.api_key,
            )
        case "ollama":
            from langchain_ollama import ChatOllama

            llm = ChatOllama(
                model=settings.llm.name, temperature=settings.llm.temperature
            )

        case "groq":
            from langchain_groq import ChatGroq

            llm = ChatGroq(
                model=settings.llm.name,
                temperature=settings.llm.temperature,
                api_key=settings.llm.api_key,
            )

        case "anthropic":
            from langchain_anthropic import ChatAnthropic

            llm = ChatAnthropic(
                model_name=settings.llm.name,
                temperature=settings.llm.temperature,
                anthropic_api_key=settings.llm.api_key,
            )

        case "google":
            from langchain_google_genai import ChatGoogleGenerativeAI
            import os

            # Suppress logging warnings
            os.environ["GRPC_VERBOSITY"] = "ERROR"
            os.environ["GLOG_minloglevel"] = "2"

            llm = ChatGoogleGenerativeAI(
                model=settings.llm.name,
                temperature=settings.llm.temperature,
                api_key=settings.llm.api_key,
            )

        case "aws":
            from langchain_aws import ChatBedrockConverse

            region, access_key, secret_key = settings.llm.api_key.split(" ")

            llm = ChatBedrockConverse(
                model=settings.llm.name,
                temperature=settings.llm.temperature,
                region_name=region,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
            )
    return llm


DEFAULT_CONTEXT_LEN = 8192
LLM_CONTEXT_WINDOWS = {
    "openai": {
        "default": DEFAULT_CONTEXT_LEN * 4,
    },
    "ollama": {
        "default": DEFAULT_CONTEXT_LEN,
    },
    "groq": {
        "default": DEFAULT_CONTEXT_LEN,
    },
    "anthropic": {
        "default": DEFAULT_CONTEXT_LEN * 4,
    },
    "google": {
        "default": DEFAULT_CONTEXT_LEN * 4,
    },
    "aws": {
        "default": DEFAULT_CONTEXT_LEN * 4,
    },
}


def get_llm_context():
    provider = LLM_CONTEXT_WINDOWS.get(settings.llm.provider, None)
    if not provider:
        return DEFAULT_CONTEXT_LEN
    return provider.get(
        settings.llm.name,
        provider.get("default", DEFAULT_CONTEXT_LEN),
    )
