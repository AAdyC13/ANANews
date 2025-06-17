import json
import openai

default_prompt = "用戶偏好使用繁體中文對話。你的回答必須在300字以內。\n你可以和用戶聊任何話題。"

# keys.json 包含以下結構
{
    "OPENAI_API_KEY": "",
    "OPENAI_ORG_ID": "",
    "GEMINI_API_KEY": "",
    "ANTHROPIC_API_KEY": "",
    "REPLICATE_API_KEY": "",
    "GROQCLOUD_API_KEY": "",
    "HUGGINGFACE_API_KEY": "",
    "QWEN_API_KEY": "",
    "XAI_API_KEY": "",
    "MISTRAL_API_KEY": "",
    "DEEPSEEK_API_KEY": "",
    "GHLF_API_KEY": "",
    "HYPERBOLIC_API_KEY": "",
    "NOVITA_API_KEY": "",
    "OPENROUTER_API_KEY": ""
}


class OpenAIClient:
    def __init__(self, keys_path="keys.json"):
        # 從 keys.json 讀取 API 金鑰
        with open(keys_path, "r") as file:
            keys = json.load(file)
        self.api_key = keys.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found in keys.json")
        openai.api_key = self.api_key

    def send_prompt(self, sentence: str, history: list, model="o4-mini-2025-04-16", max_tokens=2000) -> str:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": default_prompt},
                # 加入歷史紀錄
                *[
                    {"role": "user", "content": item} if i % 2 == 0 else {
                        "role": "assistant", "content": item}
                    for i, item in enumerate(history)
                ],
                {"role": "user", "content": sentence}
            ],
            max_completion_tokens=max_tokens
        )
        text = response.choices[0].message.content.strip()
        return text


OpenAI = OpenAIClient()
