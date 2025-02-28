from openai import OpenAI
import requests

def response_ai(url, api_key, input_lang, output_lang, text, model):
    """
    Function to get the response from the models on openrouter.ai
        Args:
            url: str: url of the openrouter.ai
            api_key: str: api key to access the models
            input_lang: str: input language
            output_lang: str: output language
            text: str: text to translate
            model: str: model to use
        Returns:
            str: translated text
    """
    try:
        client = OpenAI(
            base_url=url,
            api_key=api_key
        )

        response = client.chat.completions.create(
            model=model,
            extra_body={},
            messages=[
                {
                    "role": "user",
                    "content": f"Translate the following text from {input_lang} to {output_lang}: {text} in medical terms only answer with the translation",
                }
            ],
        )

        if response:
            translated_text = response.choices[0].message.content
        else:
            translated_text = "No response from the model"

    except Exception as e:
        translated_text = f"translation failed {str(e)}"
    finally:
        return translated_text




def response_my_memory(my_memory_url, input_lang, output_lang, text):
    """
    Function to get the response from the my_memory translation service
        Args:
            my_memory_url: str: url of the my_memory service
            input_lang: str: input language
            output_lang: str: output language
            text: str: text to translate
        Returns:
            str: translated text
    """
    try:
        params = {"q": text, "langpair": f"{input_lang}|{output_lang}"}
        response = requests.get(my_memory_url, params=params)
        if response.status_code == 200:
            translated_text = response.json().get("responseData", {}).get("translatedText", "")
        else:
            translated_text = "Error en la traducción"

    except Exception as e:
        translated_text = f"Error en la traducción: {str(e)}"
    finally:
        return translated_text

