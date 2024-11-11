import dotenv
import os
import time
import datetime
import pickle
import json
import re
import requests
import hashlib

from openai import OpenAI
import google.generativeai as genai
from huggingface_hub import InferenceClient


# Set a default model for each major LLM provider
default_model_dict = dict(
    OpenAI="gpt-4o-2024-08-06",
    Google="gemini-1.5-pro",
    HuggingFace="meta-llama/Meta-Llama-3-8B-Instruct",
    Togetherai="mistralai/Mixtral-8x7B-Instruct-v0.1",
    DeepInfra="meta-llama/Meta-Llama-3.1-8B-Instruct",
    LambdaLabs="hermes-3-llama-3.1-405b-fp8",
)
# Provider name should have no whitespace or weirdness.
provider_list = [
    "OpenAI",
    "Google",
    "HuggingFace",
    "Togetherai",
    "DeepInfra",
    "LambdaLabs",
]

LLM_Client = {}
query_timestamp = {}
API_keys = {}
initialized_LLMs = {}


def stable_hash(s, out_bytes=10):
    # The intrinsic Python "hash" function is constant across a single process but
    # varies between processes. This function tries to give us a more stable
    # hash value.
    m = hashlib.sha256()
    s = str(s).encode("utf-8")
    m.update(s)
    out = m.hexdigest()
    out = out[:out_bytes]  # Drop to 4*out_bytes bits of entropy
    return out


def prepare_API_keys(logger=None):
    for provider in provider_list:
        if initialized_LLMs.get(provider) is not None:
            continue

        # Make sure API key is defined
        key_var = f"{provider.upper()}_API_KEY"
        if os.environ.get(key_var) is None:
            dotenv.load_dotenv(dotenv.find_dotenv())
        API_key = os.environ.get(key_var)
        if logger is not None:
            logger.info(f"Loading {provider} API keys to environment...")
        if API_key is None:
            # Require keys for all providers...
            # raise ValueError(
            #     f"API key error: Could not find {provider} API key {key_var}"
            # )
            # Or just use the keys you've got...
            continue
        API_keys[provider] = API_key

        if provider == "OpenAI":
            LLM_Client[provider] = OpenAI()
        elif provider == "Google":
            genai.configure(api_key=API_key)
        elif provider == "DeepInfra":
            LLM_Client[provider] = OpenAI(
                api_key=API_key, base_url="https://api.deepinfra.com/v1/openai"
            )
        elif provider == "LambdaLabs":
            LLM_Client[provider] = OpenAI(
                api_key=API_key, base_url="https://api.lambdalabs.com/v1"
            )
        initialized_LLMs[provider] = True
    if len(API_keys) == 0:
        raise ValueError("Could not find any LLM API keys. Maybe you need a .env file?")
    return


model_dict = {}


def get_model(provider=None, model_name=None):
    if model_dict.get((provider, model_name)) is None:
        API_key = API_keys[provider]
        if provider == "Google":
            model_dict[(provider, model_name)] = genai.GenerativeModel(model_name)
        elif provider == "HuggingFace":
            model_dict[(provider, model_name)] = InferenceClient(
                model=model_name, token=API_key
            )
        else:
            raise ValueError(f"Cannot process provider {provider}")
    return model_dict[(provider, model_name)]


safety_block_string = "Safety Block"
refusal_string = "REFUSAL"


def try_to_extract_JSON(text):
    # Regular expression to find the JSON substring
    json_match = re.search(r"\{.*?\}", text, re.DOTALL)

    # Check if a match is found and extract the JSON substring
    if json_match:
        json_str = json_match.group(0)
        return json_str
    else:
        return text


# A sample input for "response_format" in "structure_LLM_API()":
# import pydantic
# class polygon(pydantic.BaseModel):
#     name: str
#     num_sides: int
#     list_of_angles: list[float]
# Note that this requires Python 3.9+ and we would use it with:
# structured_LLM_API(prompt="Make a triangle", response_format=polygon)
def structured_LLM_API(
    prompt,
    system_prompt="You are a helpful assistant.",
    sleep_seconds=0,
    cache=True,
    cache_dir="cache",
    provider="OpenAI",
    model_name=None,
    index=0,
    response_format=None,
    logger=None,
    throw_safety_exception=True,
    mistrust_cache=False,
    flush_cache=False,
):
    """
    LLMs that guarantee structured output (e.g., JSON)
    """
    assert response_format is not None

    # Support for structured output is currently rare
    if provider not in ["OpenAI"]:
        raise ValueError("Provider does not support structured output")

    if model_name is None:
        model_name = default_model_dict[provider]

    if cache:
        os.makedirs(cache_dir, exist_ok=True)

        hash_gpt = stable_hash(
            ":".join(
                ["structured", str(index), provider, model_name, prompt, system_prompt]
            )
        )
        hash_gpt_file = os.path.join(cache_dir, f"{hash_gpt}_gpt.pkl")
        if flush_cache:
            os.remove(hash_gpt_file)
        if os.path.exists(hash_gpt_file):
            with open(hash_gpt_file, "rb") as fp:
                blob = pickle.load(fp)
            # In some cases, your LLM may start misbehaving but LLM_API will
            # suppress the error and just pretend the LLM reply was "".
            # If you're afraid of that, set mistrust_cache=True when
            # calling LLM_API and re-run your code.
            if blob["reply"] == "" and mistrust_cache:
                # Suspiciously empty cache... let's try that again.
                pass
            else:
                return blob["reply"]

    prepare_API_keys(logger=logger)

    # Don't flood the LLM server with requests
    now = datetime.datetime.now()

    if query_timestamp.get((provider, model_name)) is not None:
        delay = (
            sleep_seconds
            - (now - query_timestamp[(provider, model_name)]).total_seconds()
        )
        if delay > 0:
            time.sleep(delay)
    query_timestamp[(provider, model_name)] = now

    usage = None
    refusal = False
    if provider in ["OpenAI"]:
        response = LLM_Client[provider].beta.chat.completions.parse(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            user="Mirabolic",  # Track what project these tokens are for
            response_format=response_format,
        )
        usage = response.usage
        if response.choices[0].message.refusal is not None:
            refusal = True
            formatted_response_as_dict = None
        else:
            formatted_response_as_obj = response.choices[0].message.parsed
            formatted_response_as_dict = formatted_response_as_obj.__dict__
    else:
        raise ValueError(f"Unknown/unsupported provider {provider}")

    if cache:
        with open(hash_gpt_file, "wb") as fp:
            blob = dict(
                prompt=prompt,
                reply=formatted_response_as_dict,
                provider=provider,
                model=model_name,
                index=index,
                usage=usage,
                refusal=refusal,
            )
            pickle.dump(blob, fp)

    if throw_safety_exception and refusal:
        raise ValueError(refusal_string)

    # Return structured response.  If LLM refusal, return None.
    return formatted_response_as_dict


def LLM_API(
    prompt,
    system_prompt="You are a helpful assistant.",
    sleep_seconds=0,
    cache=True,
    cache_dir="cache",
    provider="OpenAI",
    model_name=None,
    index=0,
    make_json=False,
    logger=None,
    throw_safety_exception=False,
    mistrust_cache=False,
    flush_cache=False,
):
    # Note: for OpenAI, response_format = { "type": "json_object" } is useful.
    if model_name is None:
        model_name = default_model_dict[provider]

    if cache:
        os.makedirs(cache_dir, exist_ok=True)

        hash_gpt = stable_hash(
            ":".join([str(index), provider, model_name, prompt, system_prompt])
        )
        hash_gpt_file = os.path.join(cache_dir, f"{hash_gpt}_gpt.pkl")
        if flush_cache:
            os.remove(hash_gpt_file)
        if os.path.exists(hash_gpt_file):
            with open(hash_gpt_file, "rb") as fp:
                blob = pickle.load(fp)
            # In some cases, your LLM may start misbehaving but LLM_API will
            # suppress the error and just pretend the LLM reply was "".
            # If you're afraid of that, set mistrust_cache=True when
            # calling LLM_API and re-run your code.
            if blob["reply"] == "" and mistrust_cache:
                # Suspiciously empty cache... let's try that again.
                pass
            else:
                return blob["reply"]

    prepare_API_keys(logger=logger)

    # Don't flood the LLM server with requests
    now = datetime.datetime.now()

    if query_timestamp.get((provider, model_name)) is not None:
        delay = (
            sleep_seconds
            - (now - query_timestamp[(provider, model_name)]).total_seconds()
        )
        if delay > 0:
            time.sleep(delay)
    query_timestamp[(provider, model_name)] = now

    usage = None
    if provider in ["OpenAI", "DeepInfra", "LambdaLabs"]:
        if make_json:
            response_format = {"type": "json_object"}
        else:
            response_format = None

        response = LLM_Client[provider].chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            user="Mirabolic",  # Track what project these tokens are for
            response_format=response_format,
        )
        usage = response.usage
        text = response.choices[0].message.content
    elif provider == "Google":
        model = get_model(provider=provider, model_name=model_name)
        generation_config = {"system_prompt": system_prompt}
        if make_json:
            generation_config["response_mime_type"] = "application/json"
        response = model.generate_content(prompt, generation_config=generation_config)
        # Note: Google may refuse to respond on grounds of "safety"
        if (
            response.candidates[0].finish_reason
            == genai.protos.Candidate.FinishReason.SAFETY
        ):
            if throw_safety_exception:
                raise ValueError(safety_block_string)
            else:
                text = safety_block_string
        else:
            text = response.text
    elif provider == "HuggingFace":
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
        model = get_model(provider=provider, model_name=model_name)
        response = model.chat_completion(messages, max_tokens=6000)
        raw_text = response.choices[0].message.content
        # Sometimes replies look like "Here is you answer! <JSON blob>";
        # we try to fix that.
        text = try_to_extract_JSON(raw_text)
    elif provider == "Togetherai":
        togetherai_url = "https://api.together.xyz/v1/chat/completions"
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "model": model_name,
            "temperature": 0.7,
            "frequency_penalty": 0,
            "presence_penalty": 0,
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {API_keys[provider]}",
        }

        response = requests.post(togetherai_url, json=payload, headers=headers)
        try:
            blob = json.loads(response.text)
            if "error" in blob:
                logger.warn(blob["error"]["message"])
                # text = ""
                raise ValueError("Key 'error' in JSON blob.")
            else:
                text = blob["choices"][0]["message"]["content"]
        except Exception:
            logger.error("Response.text:")
            logger.error(f"{str(response.text)}")
            raise
    else:
        raise ValueError(f"Unknown provider {provider}")

    if cache:
        with open(hash_gpt_file, "wb") as fp:
            blob = dict(
                prompt=prompt,
                reply=text,
                provider=provider,
                model=model_name,
                index=index,
                usage=usage,
            )
            pickle.dump(blob, fp)
    # Extract text of reply and return it
    return text
