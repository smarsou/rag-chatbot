import logging, os
from rag.pipelines import RAGQueryPipeline
from rag.embeddings import MyEmbedding
from rag.vectorstores import MyVectorStoreInterface
import requests

MAX_REQUESTS_PER_DAY=2000
MAX_LENGTH_TEXT=300
logger = logging.getLogger(__name__)

class SingletonMeta(type):
    """
    Meta class to implement singleton.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Redefined __call__ method to control the instantiation.
        
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class AssistantAPI(metaclass=SingletonMeta):

    def __init__(self, embedding_api_base : str, vector_db_connection : str, collection_name :str):
        logger.debug("Initializing the Assistant API and the RAG Pipeline.")
        self.total_requests = 0
        self.embedding = MyEmbedding(api_base=embedding_api_base)
        logger.debug("1/3 Connected to the embedding model")
        self.vector_store_interface = MyVectorStoreInterface(embedding=self.embedding, connection=vector_db_connection, collection_name=collection_name)
        logger.debug("2/3 Connected to the Vector Store DB for the RAG system")
        self.query_api = RAGQueryPipeline(self.vector_store_interface)
        logger.debug("3/3 RAG pipeline Ready !")

    def process_user_request(self, chat_request):

        # Process user request
        if self.total_requests >= MAX_REQUESTS_PER_DAY:
            raise Exception("Max requests limit.")
        
        if len(chat_request)>20:
            chat_request = chat_request[20:]

        # Retrieve RAG documents
        retrieved_docs = self.query_api.query(chat_request[-1]['content'], k=4)
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
            "content": system_prompt
            }
        ]

        # 2. Add the retrieved documents to the messages
        if docs_content:
            messages.append(
                {
                    "role": "user",
                    "content": f"Relevant context:\n{docs_content}"
                }
            )

        # 3. Add the user request with the history of the discussion to send in the prompt (used to keep short-term history of the discussion) 
        for chat_unit in chat_request:
            messages.append(
                {
            "role": chat_unit['role'],
            "content": chat_unit['content']
            }
            )
        
        # Send the request using the OpenAI API
        response = requests.post(url=os.getenv("OPENAI_BASE_URL") + "/v1/chat/completions",
                      json = { 
                          "model": os.getenv("CHAT_MODEL_NAME"),
                          "messages": messages
                      })

        self.total_requests += 1
        # Get the content of the message
        return str(response.json()["choices"][0]["message"]["content"])
