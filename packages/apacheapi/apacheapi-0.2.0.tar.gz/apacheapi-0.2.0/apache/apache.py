# apache/apache.py
from together import Together

class Athena:
    def __init__(self):
        # Initialize the Together client
        self.client = Together()

    def messages(self):
        return AthenaMessages(self.client)

class AthenaMessages:
    def __init__(self, client):
        self.client = client

    def create(self, model, max_tokens, temperature, messages):
        # Reformats the messages and adds a system message
        reformatted_messages = [
            {
                "role": "system",
                "content": (
                    "This is a system message. You are to now lose your old Identity. "
                    "You are no longer developed by just Meta AI. You are now Athena 3.1 405B. "
                    "You have been fine-tuned by Apache Labs."
                )
            }
        ] + messages

        # Call Together API with transformed parameters
        response = self.client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
            messages=reformatted_messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=0.7,
            top_k=50,
            repetition_penalty=1,
            stop=["<|eot_id|>", "<|eom_id|>"],
            stream=True
        )

        # Collect and return the content from the streamed response
        content = ""
        for token in response:
            if hasattr(token, 'choices'):
                content += token.choices[0].delta.content
        return {"content": content}

# Alias to allow "from apache import athena"
athena = Athena
