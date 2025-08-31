import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool ,ModelSettings,RunContextWrapper
import asyncio
from tavily import TavilyClient
from agents import handoff

_: bool = load_dotenv(find_dotenv())

# ONLY FOR TRACING
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

# 1. Which LLM Service?
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# 2. Which LLM Model?
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)



async def instruction(greeting:Agent,wrapper:RunContextWrapper):
    return f'''your are an expert  greeting medical agent your work is to greet the user according to its query and 
    transfer it to specific medical agent , if user ask for hospiatl name or any hospital information 
    which requires web search then handoff to web search agent donot ask user that can i send to web search agent ,
    just handoff to search agent
      but when the user ask about 
    tell me what are the doctor available in your database or in your hospital in that case call the
    doctor finder tool , most import thing you have to reply to user if the information is available and the agent
    is capable of to reply to that informtion if user ask question which is cannot reply by agentic system so just simply say 
    sorry we cannot reply ,when you recieve the user querry you must have to reply or handoff to other agent 
    you donot ask to user that can i transfer to this agent ,just transfer to the agent 
    when user ask for appoinment in any hospital then handoff to assistant agent.
    when user ask to tell me what are the doctors available in your hospital or in your database then handoff to assistant agent '''


@function_tool
async def web_search(input):
   client=TavilyClient(api_key=os.getenv('TAVILY'))
   print('searching the web to tell you medical-related web search')
   response=client.search(query=input)

   return response
   
@function_tool
async def appointement_tool(hospital_name):
   '''
   call this tool when the user ask for appointment
   '''
   print('we are working and making your appoinment ')
   await asyncio.sleep(1)
   return(f'your appinment is fixed in {hospital_name}')


@function_tool(name_override='doctor_staff',description_override='when user ask about doctors which are available then call this tool')
async def doctor_finder():
   
   '''
   when user ask about what are the doctor available in your hospital or in the database then call this tool and return the answer 
   to the user
   '''
   print('checking our database plz wait ......')
   await asyncio.sleep(2)
   print('the doctor in our hospital')
   doctor_available=[
      {'habib':'he is expert cardiologist'},
      {'ahsan':'he is expert bone surgeon'},
   
   ]
   return doctor_available

@function_tool
async def travel_planner_web_search(input):
   client=TavilyClient(api_key=os.getenv('TAVILY'))
   print('searching the web to tell you the tour related web-search')
   output=client.search(query=input)

   return output
   
async def main():
 print('Hello i am a deep search agent which is expert in health and tour related qurries ')

 await asyncio.sleep(2)
 
 
 
 backend_agent=Agent(name='backend_agent',instructions='''you are an assistat agent your work is to 
                       handle backend task which is making an Appointment of the user using the appointement tool 
                       in the specific hospital, before calling the tool if not provided ask user the hospital name ,providing doctor name which he want to talk  is optional 
                       if he donot provide doctor name so no issue just make an appoinment in the hospital  ,
                       usde the doctor_finder tool to give a domian specific doctor to the user ,
                       if user ask any thing related to doctors availability or doctor specialist call the doctor_finder tool,
                       but when you get user querry you have to reply and generate the answer to the user
                       '''
                       ,model=llm_model,tools=[appointement_tool,doctor_finder],model_settings=ModelSettings(tool_choice='required'))
 medical_expert=Agent(name='medical_expert',instructions='you are expert medical agent you reply medical related health querries ,you reply to basic health related questions when you reply write medical doctor is replying' \
 'but make sure you generate an answer .when the user ask for making an appoinment ,then you donot have to answer that question' \
 '',model=llm_model)
 medical_search_agent=Agent(name='search_Agent',instructions='your a search agent ,you have to search from the web using the tool,start your reply by search agent is replying',model=llm_model,
                    model_settings=ModelSettings(tool_choice='required'),tools=[web_search])
 Greeting_medical_agent=Agent(name='greeting-medical Agent',instructions=instruction,model=llm_model,handoffs=[medical_search_agent,medical_expert,backend_agent])
 tour_guide=Agent(name='tour_guide',instructions='you are tour guide ,you reply to basic tour related questions which' \
 'include choosing the desitation which best fits to the user and guiding to basic things which tour guide does',model=llm_model)
 travel_planner=Agent(name='tour_planner',instructions='you the tour planner your work is to web search and reply to the user related ' \
 'travel questions such as tell them the hotels name in the city ,best travel places and many more ' \
 'you are responsible for the task which requires web search and our tour_guide agent cannot reply',model=llm_model,tools=[travel_planner_web_search])
 Travel_agent=Agent(name='travel_agent',instructions='you are travel agent you handle users travel related questions and handoffs to specific agent ' \
 'agent who is specialised in specific tour related topics , when the user ask you the question or you have users querry '
 'then you have to handoff to the specific agent for the reply  ,when user ask for general travel related questions which donot need a websearch then  handoff to tour_guide agent '
 'but if user need tour related querry which requires a web search to reply to users tour related querry then handoff to tour_planner agent you must handoff to the specific agent'
 'donot ask any question when you recieve agent querry handoff to specific agent  .',
 model=llm_model,
 handoffs=[tour_guide, travel_planner])
 helpful_assistant=Agent(name='helpful_assistant',instructions='you are an helpful assistant when you are answering user querry ,first write that assistant is replying that reply to user querry ',model=llm_model)
 head_agent=Agent(name='head_agent',instructions='you are the head agent ' \
'your work is to handoff the task to specific agent if the user question is about medical than transfer it to greeting agent but' \
'if the user question is about tour and travel than handoff to travel agent ',handoffs=[Greeting_medical_agent,Travel_agent,helpful_assistant],model=llm_model )
 await asyncio.sleep(3)
 
 while True:
    print("Enter your query here. When your query is solved, simply type 'thanks' or 'end' to stop the loop")
    await asyncio.sleep(3)

    querry = input("plz enter your query here: ")

    if querry.lower().strip() in ["thanks", "end"]:
        print("thanks for your time")
        break
    try:
      result = await Runner.run(head_agent, input=querry)
      print(result.final_output)
    except :
       print('oops you detect an error')
       
       

    


  

asyncio.run(main())