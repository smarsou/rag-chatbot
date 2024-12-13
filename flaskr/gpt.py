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

    def process_user_request(self, chat_request):

        # Process user request
        if self.total_requests >= MAX_REQUESTS_PER_DAY:
            raise Exception("Max requests limit.")
        
        if len(chat_request)>30:
            chat_request = chat_request[30:]
        
        # Retrieve system prompt
        try :
            fetched_system_prompt = open('system.prompt', 'r').readlines()
            system_prompt = ''.join(fetched_system_prompt)
        except:
            raise Exception("System prompt error")
        
        # Init messages with system prompt
        messages=[
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": system_prompt
                }
            ]
            }
        ]
        
        # Add the messages to send in the prompt (used to keep short-term history of the discussion) 
        for chat_unit in chat_request:
            messages.append(
                {
            "role": chat_unit['role'],
            "content": [
                {
                "type": "text",
                "text": chat_unit['content']
                }
            ]
            }
            )
        
        # Send the request using the OpenAI API
        response = self.client.chat.completions.create(
        model="gpt-4o-mini",
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
        
        # Get the content of the message
        return str(response.choices[0].message.content)