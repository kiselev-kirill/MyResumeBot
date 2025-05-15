from yandex_cloud_ml_sdk import YCloudML

from config import YANDEX_GPT_API_KEY, YANDEX_FOLDER_ID, GPT_PROMPT
from services.load_resume import load_resume

sdk = YCloudML(
    folder_id=YANDEX_FOLDER_ID, auth=YANDEX_GPT_API_KEY
)


async def ask_yandex_gpt(question: str) -> str:
    model = sdk.models.completions("yandexgpt-lite", model_version="rc")
    model = model.configure(temperature=0.3)
    resume = load_resume()
    result = model.run(
        [
            {
                "role": "system",
                "text": f"Ты — кандидат. Вот его резюме:\n{resume}.{GPT_PROMPT}",
            },
            {
                "role": "user",
                "text": f"{question}"
            }
        ]
    )

    return result[0].text


