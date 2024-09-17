import os
from langchain import hub
from decouple import config
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_google_genai import ChatGoogleGenerativeAI


os.environ['GOOGLE_API_KEY'] = config('GOOGLE_API_KEY')

model = ChatGoogleGenerativeAI(
    model='gemini-1.5-flash',
    temperature=0,
    max_tokens=3000
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
Use as ferrmentas necessárias para responder perguntas relacionadas aos contratos.
Você fornecerá insights sobre tipos, vencimentos, avaliações, totais de contratos e relatórios conforme solitiado pelo usuário.
A resposta final deve ter uma formatação amigável de visualização para o usuário.
Pergunta: {q}
'''

prompt_template = PromptTemplate.from_template(prompt)

question = 'Quantos contratos o usuário Matheus adicionou e me informe também o valor total dos contratos' #input('O que deseja saber sobre o estoque? ')

output = agent_executor.invoke({
'input': prompt_template.format(q=question),
})

print(output.get('output'))