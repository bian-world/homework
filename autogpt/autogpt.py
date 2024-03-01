import os
import gradio as gr


os.environ["SERPAPI_API_KEY"] = "XXXX"
os.environ["OPENAI_API_KEY"] = "sk-XXXXX"
os.environ["http_proxy"] = "http://127.0.0.1:XXXX"
os.environ["https_proxy"] = "http://127.0.0.1:XXXX"

from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import Tool
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool
from langchain_openai import OpenAIEmbeddings
from langchain_experimental.autonomous_agents import AutoGPT
from langchain_community.chat_models import ChatOpenAI
import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.docstore import InMemoryDocstore

def init_vectorstore():
    # OpenAI Embedding 模型
    embeddings_model = OpenAIEmbeddings()
    embedding_size = 1536
    # 使用 Faiss 的 IndexFlatL2 索引
    index = faiss.IndexFlatL2(embedding_size)
    global vectorstore
    vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})


def init_agent():
    # 构造 AutoGPT 的工具集
    search = SerpAPIWrapper()
    tools = [
        Tool(
            name="search",
            func=search.run,
            description="useful for when you need to answer questions about current events. You should ask targeted questions",
        ),

        # WriteFileTool(),
        # ReadFileTool(),
    ]

    agent = AutoGPT.from_llm_and_tools(
        ai_name="Jarvis",
        ai_role="Assistant",
        tools=tools,
        llm=ChatOpenAI(model_name="gpt-4", temperature=0, verbose=True),
        memory=vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold": 0.8}),  # 实例化 Faiss 的 VectorStoreRetriever
    )
    # 打印 Auto-GPT 内部的 chain 日志
    # agent.chain.verbose = True
    return agent


def sales_chat(message, history):
    print(f"[message]{message}")
    print(f"[history]{history}")
    ans = init_agent().run([message])
    enable_chat = True
    if ans or enable_chat:
        # print(f"[result]{ans['result']}")
        # print(f"[source_documents]{ans['source_documents']}")
        return ans
    # 否则输出套路话术
    else:
        return "这是个好问题，我目前还没有答案"

def launch_gradio():
    demo = gr.ChatInterface(
        fn=sales_chat,
        title="AutoGpt",
        # retry_btn=None,
        # undo_btn=None,
        chatbot=gr.Chatbot(height=600),
    )
    demo.launch(share=True, server_name="0.0.0.0")


if __name__ == "__main__":

    init_vectorstore()
    # 启动 Gradio 服务
    launch_gradio()