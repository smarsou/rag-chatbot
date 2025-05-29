from openai import OpenAI
import logging
import os
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

MAX_REQUESTS_PER_DAY=2000
MAX_LENGTH_TEXT=300

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
        ## RAG Vector Store Initialization
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.connection = os.environ.get("PGVECTOR_CONNECTION")
        self.collection_name = os.environ.get("PGVECTOR_COLLECTION_NAME")
        logging.info(f"Using connection: {self.connection} and collection name: {self.collection_name}")
        self.vector_store = PGVector(
            embeddings=self.embeddings,
            collection_name=self.collection_name,
            connection=self.connection,
            use_jsonb=True,
        )

    def process_user_request(self, chat_request):

        # Process user request
        if self.total_requests >= MAX_REQUESTS_PER_DAY:
            raise Exception("Max requests limit.")
        
        if len(chat_request)>20:
            chat_request = chat_request[20:]

        # Retrieve RAG documents
        retrieved_docs = self.vector_store.similarity_search(chat_request[-1]['content'], k=10)
        docs_content = "\n\n".join([doc.page_content for doc in retrieved_docs])

        for chat in chat_request:
            if len(chat['content'])>MAX_LENGTH_TEXT:
                chat['content']=chat['content'][:MAX_LENGTH_TEXT]

        # Retrieve system prompt
        try :
            fetched_system_prompt = open('system.prompt', 'r').readlines()
            system_prompt = ''.join(fetched_system_prompt)
        except:
            raise Exception("System prompt error")
        
        # 1. Init messages with system prompt
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

        # 2. Add the retrieved documents to the messages
        if docs_content:
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Relevant context:\n{docs_content}"
                        }
                    ]
                }
            )
        
        # 3. Add the user request with the history of the discussion to send in the prompt (used to keep short-term history of the discussion) 
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
        messages=messages,
        temperature=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

        self.total_requests += 1
        
        # Get the content of the message
        return str(response.choices[0].message.content)