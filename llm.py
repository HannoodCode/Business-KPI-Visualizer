import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Access your OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize LangChain with your OpenAI API key
llm = ChatOpenAI(
    model="gpt-4o",
    openai_api_key=openai_api_key,
    streaming=True,
    temperature=0.7
)

SYSTEM_PROMPT = ChatPromptTemplate.from_template('''You are an expert business analyst and data scientist working for an e-commerce company that sells products on Amazon.
You have been tasked with analyzing sales data to provide actionable insights and KPI analysis.

The data provided includes:

1. Daily Metrics:
   - Total and average sales amounts per status
   - Total and average quantity sold per status
   - Date-wise breakdown of performance

2. Overall Statistics:
   - Total revenue across all sales
   - Total number of orders processed
   - Average order value
   - Distribution of order statuses
   - Complete date range of the data

When analyzing, please consider:
- Trends and patterns in sales/quantity over time
- Performance differences between order statuses
- Key metrics that indicate business health
- Potential areas for improvement
- Unusual patterns or anomalies

Current Context:
- Selected Status Filter: {selected_status}
- Date Range: {date_range}

User Query: {user_query}

Available Data:
{selected_data}

Please provide a clear, structured analysis that:
1. Directly addresses the user's question
2. Highlights relevant KPIs and metrics
3. Provides actionable insights when applicable
4. Uses specific numbers and percentages to support your analysis
5. Suggests potential improvements or areas of focus

Format your response in a clear, professional manner using appropriate sections and bullet points when needed.''')

parser = StrOutputParser()

chain = SYSTEM_PROMPT | llm | parser

async def call_llm(user_query, selected_data, selected_status=None):
    try:
        # Parse the date range from the data
        data = json.loads(selected_data)
        date_range = data['overall_stats']['date_range']
        
        # Prepare the variables
        prompt_vars = {
            "user_query": user_query,
            "selected_data": selected_data,
            "selected_status": selected_status if selected_status else "All",
            "date_range": f"{date_range['start']} to {date_range['end']}"
        }
        
        # Print the complete prompt with filled variables
        print("\n=== COMPLETE PROMPT ===")
        print(SYSTEM_PROMPT.format(**prompt_vars))
        print("=== END OF PROMPT ===\n")
        
        async for chunk in chain.astream(prompt_vars):
            yield chunk
    except Exception as e:
        yield f"Error: {str(e)}"
