
# views.py
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_google_genai import ChatGoogleGenerativeAI
from decouple import config
import os

os.environ['GOOGLE_API_KEY'] = config('GOOGLE_API_KEY')

model = ChatGoogleGenerativeAI(
    model='gemini-1.5-flash',
    max_output_tokens=3000,
    cache=True,
)

db = SQLDatabase.from_uri('sqlite:///db.sqlite3')

toolkit = SQLDatabaseToolkit(
    db=db,
    llm=model,
)

system_message = hub.pull('hwchase17/react')

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

prompt = '''
Utilize as ferramentas disponíveis para responder perguntas sobre contratos.
Forneça insights sobre tipos, vencimentos, avaliações, totais de contratos e relatórios conforme solicitado pelo usuário.
A resposta deve ser clara e formatada de maneira amigável para fácil visualização. 
Utilize português brasileiro.
Os dados estão armazenados em um banco de dados de uma aplicação Django.
Pergunta: {q}
'''

prompt_template = PromptTemplate.from_template(prompt)