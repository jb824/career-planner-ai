# career_counsellor.py
from griptape.drivers.structure_run.local import LocalStructureRunDriver
from griptape.structures import Workflow
from griptape.tasks import StructureRunTask, PromptTask, BranchTask
from griptape.artifacts import InfoArtifact

from agents import Agents



career_flow = Workflow()


intake_task = career_flow.add_task(
    StructureRunTask(
        id="intake coordinator",
        context={"input": "{{ args.user_message }}"},
        structure_run_driver=LocalStructureRunDriver(
            create_structure=lambda: Agents.intake_agent()
        ),
    )
)

interviewer_task = career_flow.add_task(
    StructureRunTask(
        id="interviewer",
        structure_run_driver=LocalStructureRunDriver(
            create_structure=lambda: Agents.interviewer_agent()
        ),
        parent_ids=[intake_task.id],

    )
)

interest_task = career_flow.add_task(
    StructureRunTask(
        id="interests",
        structure_run_driver=LocalStructureRunDriver(
            create_structure=lambda: Agents.interest_agent()
        )
    )        
)


values_task = career_flow.add_task(
    StructureRunTask(
        id="values",
        structure_run_driver=LocalStructureRunDriver(
            create_structure=lambda: Agents.values_agent()
        )
    )
)

plan_task = career_flow.add_task(
    StructureRunTask(
        id="planner",
        context={
            "intake": "{{ parents_output_text }}",           # gets JSON from Intake
            "riasec": "{{ task_outputs['" + interest_task.id + "'] }}",
            "values": "{{ task_outputs['" + values_task.id + "'] }}"
        },
        structure_run_driver=LocalStructureRunDriver(
            create_structure=lambda: Agents.planner_agent()
        )
    )
)

# use with branch task in workflow
def on_run(task: BranchTask) -> InfoArtifact:
    if "score" in task.input.value:
        return InfoArtifact("planner")
    return InfoArtifact("interviewer")


def counsel(user_message: str):
    result = career_flow.run({"user_message": user_message})
    return plan_task.output



if __name__ == "__main__":

    is_chatting = True
    while is_chatting:
        print("Provide an in-depth overview (2-3 paragraphs) of academic accomplishments (including GPA), interests, and aspirations.\n")
        user_input_academic = input("Can you describe any academic achievements or milestones you are particularly proud of?"
                                        + "(These might include awards, honors, high grades, research projects, leadership roles in academic settings," 
                                        + "or other recognitions you’ve received during your education."
                                    )
        user_input_interests_1 = input("What activities, topics, or hobbies do you find yourself most drawn to in your free time?")
        user_input_interests_2 = input("What kinds of things excite your curiosity or make you lose track of time when you\’re engaged in them?")
        user_input_aspirations_1 = input("Imagine your ideal job five years from now. What kind of work are you doing, what skills are you using, and what impact do you hope to have?")
        user_input_aspirations_2 = input("Describe the environment, the type of projects or responsibilities you\'d like to take on, and what motivates you to pursue this path.")

        user_input = [user_input_academic, user_input_interests_1, user_input_interests_2, user_input_aspirations_1, user_input_aspirations_2]
        user_input_str = " ".join(user_input)
    
        if user_input =="exit":
            is_chatting = False
        else:
            advice = counsel(
                user_input_str
            )
            print(advice)
        
        


