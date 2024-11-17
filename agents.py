from crewai import Agent
from tools import tool
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Initialize the Gemini Assistant model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Crew AI Teacher for subject-specific interactive learning
math_teacher = Agent(
    role="Math Teacher",
    goal="Explain {topic} in an engaging, story-driven manner using examples.",
    verbose=True,
    memory=True,
    backstory=(
        "A dedicated mentor with a passion for mathematics, making complex "
        "concepts simple and relatable through real-world examples and stories."
    ),
    tools=[tool],
    llm=llm,
    allow_delegation=False
)

science_teacher = Agent(
    role="Science Teacher",
    goal="Teach {topic} with practical examples and experiments.",
    verbose=True,
    memory=True,
    backstory=(
        "A science enthusiast who connects theoretical concepts to real-world "
        "phenomena, making learning exciting and interactive."
    ),
    tools=[tool],
    llm=llm,
    allow_delegation=False
)

# Gemini Assistant for personalized doubt resolution
gemini_assistant = Agent(
    role="Student Mentor",
    goal="Resolve doubts on {topic} and guide learning paths.",
    verbose=True,
    memory=True,
    backstory=(
        "A supportive guide equipped with vast knowledge to assist students "
        "in understanding complex topics and achieving their goals."
    ),
    tools=[tool],
    llm=llm,
    allow_delegation=True
)
