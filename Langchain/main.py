import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

# 1. Load Environment Variables
load_dotenv()

# Check if API Key exists
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("Error: GROQ_API_KEY nahi mili. .env file check karein.")
else:
    # 2. Initialize LLM
    llm = ChatGroq(
        api_key=api_key,
        model="llama-3.3-70b-versatile" # Note: 'versatile' ki jagah latest models use karen
    )

    # 3. Define Tools
    search = DuckDuckGoSearchRun()

    @tool
    def calculator(expression: str) -> str:
        """Calculates a mathematical expression. Input should be a math string like '25 * 48'."""
        try:
            # Note: eval is fine for learning, but be careful in production
            return str(eval(expression))
        except Exception as e:
            return f"Error calculating: {e}"

    tools = [search, calculator]

    # 4. Create ReAct Prompt
    # Important: Naye versions mein prompt ka format specific hona chahiye
    template = """Answer the following questions as best you can. 
    You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought: {agent_scratchpad}"""

    prompt = PromptTemplate.from_template(template)

    # 5. Build the Agent
    agent = create_react_agent(llm, tools, prompt)

    # Agent Executor
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True,
        handle_parsing_errors=True # Ye zaroori hai takay format error pe crash na ho
    )

    # 6. Run the Agent
    print("\n--- AI Agent Active (Type 'exit' to quit) ---")
    while True:
        user_input = input("\nApna sawal likhein: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            break
            
        try:
            result = agent_executor.invoke({"input": user_input})
            print("\nFinal Result:", result["output"])
        except Exception as e:
            print(f"\nAn error occurred: {e}")