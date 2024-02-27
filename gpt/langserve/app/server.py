from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_community.callbacks import get_openai_callback
from langchain.schema.runnable import RunnableLambda
from langserve.schema import CustomUserType

from langserve import add_routes
from operator import itemgetter

from decouple import config
from fastapi import FastAPI
from app.constant import (
    INITIAL_SYSTEM_PROMPT,
    INITIAL_HUMAN_PROMPT,
    LIST_OF_INSTRUCTIONS,
    CURRENT_GAME_OBJECTS,
    NEXT_ACTION_PROMPT,
)


class InitiateChatInput(CustomUserType):
    list_of_instructions: str
    current_game_objects: str

class NextChatInput(CustomUserType):
    next_game_objects: str

def initiate_chat(custom_input: InitiateChatInput):
    global chat_prompt, model

    system_message_prompt = SystemMessagePromptTemplate.from_template(INITIAL_SYSTEM_PROMPT)
    human_message_prompt = HumanMessagePromptTemplate.from_template(INITIAL_HUMAN_PROMPT)
    chat_prompt = ChatPromptTemplate.from_messages(
                    [system_message_prompt, human_message_prompt]
                )

    chat_prompt = chat_prompt.format_prompt(
                    list_of_instructions=custom_input.list_of_instructions,
                    current_game_objects=custom_input.current_game_objects
                )

    with get_openai_callback() as cb:
        output = model(
            chat_prompt.to_messages()
        )
        chat_prompt.messages.append(output)

        print("=" * 40)
        print(f"Total Cost   : Rp {cb.total_cost * 15000:.2f}")
        print(f"Total Tokens : {cb.total_tokens}")
        print("\nModel Output:\n")
        print(output.content)

    return output.content
    
def respond_chat(custom_input: NextChatInput):
    global chat_prompt, model

    human_message_prompt = HumanMessagePromptTemplate.from_template(NEXT_ACTION_PROMPT).format(current_game_objects=custom_input.next_game_objects)
    chat_prompt.messages.append(human_message_prompt)

    with get_openai_callback() as cb:
        output = model(
            chat_prompt.to_messages()
        )
        chat_prompt.messages.append(output)

        print("\nRESULT:")
        print(f"Total Cost   : Rp {cb.total_cost * 15000:.2f}")
        print(f"Total Tokens : {cb.total_tokens}")
        print()

    return output.content
    
def init_system():
    app = FastAPI()
    model = ChatOpenAI(openai_api_key=config("OPENAI_API_KEY"), model_name="gpt-3.5-turbo-0613")
    
    return model, app

global chat_prompt

model, app = init_system()
initiate_chat_runnable = RunnableLambda(initiate_chat).with_types(
    input_type=InitiateChatInput,
)
respond_chat_runnable = RunnableLambda(respond_chat).with_types(
    input_type=NextChatInput,
)

add_routes(
    app,
    initiate_chat_runnable, 
    path="/initiate-chat"
)
add_routes(
    app,
    respond_chat_runnable, 
    path="/respond-chat"
)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)