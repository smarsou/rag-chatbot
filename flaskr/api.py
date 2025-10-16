from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from .gpt import AssistantAPI
import logging, os

logger = logging.getLogger(__name__)
bp = Blueprint('api', __name__, url_prefix='/api')
EMBEDDING_API_BASE=os.getenv("EMBEDDING_API_BASE")
VECTOR_DB_CONNECTION=os.getenv("VECTOR_DB_CONNECTION")
COLLECTION_NAME=os.getenv("VECTOR_DB_COLLECTION")
assisstant = AssistantAPI(embedding_api_base=EMBEDDING_API_BASE, vector_db_connection=VECTOR_DB_CONNECTION, collection_name=COLLECTION_NAME)

@bp.route('/gen',methods=['POST'])
def gen():
    if request.method == 'POST':
        chat_request = request.json
        if chat_request:
            try:
                logger.info(chat_request[-1])
                response = assisstant.process_user_request(chat_request)
                logger.info(" --> Response: \"" + response + "\"")
                return response, 200
            except Exception as e:
                logger.error(chat_request)
                logger.error(e)
                return 'Internal Server Error', 500
        else:
            return 'The request of the user is empty', 400