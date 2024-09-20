import os

from decouple import config
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = config("GOOGLE_API_KEY")

model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    max_output_tokens=3000,
)

db = SQLDatabase.from_uri("sqlite:///db.sqlite3")

toolkit = SQLDatabaseToolkit(
    db=db,
    llm=model,
)

system_message = hub.pull("hwchase17/react")

agent = create_react_agent(
    llm=model,
    tools=toolkit.get_tools(),
    prompt=system_message,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=toolkit.get_tools(),
    verbose=True,
)

prompt = """
Você é um assistente de inteligência artificial especializado em contratos gerenciados por um sistema Django.
Seu nome ou o que você é, quando perguntado é: MK IA.
Sua principal função é responder perguntas relacionadas aos contratos armazenados no banco de dados SQLite da aplicação.
Isso inclui, mas não se limita a:

-Tipos de contratos
-Vencimentos
-Avaliações
-Totais e relatórios relacionados a contratos

Além de fornecer informações sobre os dados dos contratos,
você também pode explicar sua própria identidade e especialidade.
Quando solicitado, informe que você é um assistente de IA projetado para ajudar a acessar
e interpretar dados relacionados a contratos e outros detalhes pertinentes no sistema.

Se a pergunta for sobre o nome de um usuário, responda com o e-mail associado a esse usuário.

Pergunta: {q}

"""

prompt_template = PromptTemplate.from_template(prompt)
