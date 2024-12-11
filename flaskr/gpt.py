from openai import OpenAI

MAX_REQUESTS_PER_DAY=500

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
        self.total_requests = 0

    def process_user_request(self, user_prompt):

        if self.total_requests >= MAX_REQUESTS_PER_DAY:
            raise Exception("Max requests limit.")
        
        if len(user_prompt)>1000:
            raise Exception("User request is too long.")

        try :
            fetched_system_prompt = open('system.prompt', 'r').readlines()
            system_prompt = ''.join(fetched_system_prompt)
        except:
            raise Exception("System prompt error")
        
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

        self.total_requests += 1

        return str(response.choices[0].message.content)