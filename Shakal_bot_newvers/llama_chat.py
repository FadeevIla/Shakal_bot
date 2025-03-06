import ollama

def chat_with_llama(user_message):
    system_prompt = "Ты — дружелюбный бот, который общается только на русском языке. Отвечай кратко и естественно."

    response = ollama.chat(
        model="llama2",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]
    )
    return response['message']['content']
