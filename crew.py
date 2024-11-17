from crewai import Crew, Process
from tasks import teaching_task, mentoring_task
from agents import math_teacher, science_teacher, gemini_assistant

# Form the EquiAIverse Crew with educational tasks
crew = Crew(
    agents=[math_teacher, science_teacher, gemini_assistant],
    tasks=[teaching_task, mentoring_task],
    process=Process.sequential,  # Support concurrent learning and mentoring
)

# Start the task execution process for an educational topic
result = crew.kickoff(inputs={'topic': 'Newton’s Laws of Motion'})
print(result)