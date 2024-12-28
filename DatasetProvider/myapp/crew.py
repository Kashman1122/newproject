from crewai import Crew
from .agents import dataset_provider_agent
from .tasks import dataset_provider
from crewai import Process

crew=Crew(
    agents=[dataset_provider_agent],
    tasks=[dataset_provider],
    process=Process.sequential,
)
result = crew.kickoff(inputs={'input': 'dog dataset in yolo format'})
print(result)