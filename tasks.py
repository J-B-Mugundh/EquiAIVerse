from crewai import Task
from tools import tool
from agents import math_teacher, science_teacher, gemini_assistant

# Task for teaching lessons interactively
teaching_task = Task(
    description=(
        "Prepare and deliver an interactive lesson on {topic}. Include examples, "
        "quizzes, and dynamic adjustments based on the learner's understanding."
    ),
    expected_output="A structured and interactive lesson on {topic}, with examples and quizzes.",
    tools=[tool],
    agent=math_teacher,  
    output_file='new-blog-post.md' # Can be changed dynamically based on the subject
)

# Task for personalized mentoring
mentoring_task = Task(
    description=(
        "Resolve doubts on {topic} by analyzing the student's history and providing "
        "clear, step-by-step explanations. Recommend additional resources for practice."
    ),
    expected_output="A detailed response to the student's query with suggestions for further practice.",
    tools=[tool],
    agent=gemini_assistant
)
