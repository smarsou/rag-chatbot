from openai import OpenAI

class SingletonMeta(type):
    """
    Meta class to implement singleton.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class AssistantAPI(metaclass=SingletonMeta):

    def __init__(self):
        self.client = OpenAI()

    def process_user_request(self, user_prompt):
        fetched_system_prompt = open('system.prompt', 'r').readlines()
        system_prompt = ''.join(fetched_system_prompt)

        response = self.client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": system_prompt
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": user_prompt
                }
            ]
            }
        ],
        response_format={
            "type": "text"
        },
        temperature=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        return response.choices[0].message