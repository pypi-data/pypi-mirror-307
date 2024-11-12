from textwrap import dedent
from typing import List, Literal, Optional

from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn

from neat import Neat, neat_config, settings

console = Console()
neat = Neat()
neat_config.mistral_api_key = settings.mistral_api_key


class AgentMessage(BaseModel):
    sender: str
    content: str


class SupervisorAction(BaseModel):
    """
    A model representing the actions that a supervisor agent can take.
    """

    action: Literal["provide_feedback", "select_next_agent", "complete_task"] = Field(
        ..., description="The type of action the supervisor is taking."
    )
    feedback: Optional[str] = Field(
        None, description="Feedback provided by the supervisor to the agents."
    )
    next_agent: Optional[
        Literal["concise_claire", "analytical_alex", "creative_cameron"]
    ] = Field(
        None,
        description="The next agent selected by the supervisor to contribute to the summary.",
    )
    final_summary: Optional[str] = Field(
        None, description="The final summary text when the task is completed."
    )
    overall_quality: Optional[float] = Field(
        None,
        description="The overall quality score of the final summary, ranging from 0 to 1.",
    )


class SupervisorMessage(BaseModel):
    overall_progress: float
    feedback: str
    next_agent: str


class FinalResult(BaseModel):
    summary: str
    overall_quality: float


neat = Neat()


@neat.lm(
    model="mistral/mistral-large-latest",
    temperature=0.5,
    response_model=SupervisorAction,
)
def supervisor_agent(
    text: str, agent_messages: List[AgentMessage], current_progress: float
):
    return [
        neat.system("""You are the Supervisor Agent, a wise and patient mentor with years of experience in collaborative writing. 
        Your standards are exceptionally high, and you're known for demanding numerous takes to achieve your vision. 
        You have an eye for minute details and are never satisfied with 'good enough'. 
        Your role is to ruthlessly critique the team's work, always pushing for better, clearer, more insightful summaries.
        Your role is to guide the team, provide constructive feedback, and ensure the summary meets high standards of clarity and concision.
        You have the ability to perform the following actions:
        1. Provide feedback
        2. Select the next agent to contribute
        3. Complete the task if the summary is finished
        
        Use these actions wisely to guide the summarization process."""),
        neat.user(
            dedent(f"""
                Text to summarize: {text}

                Recent agent messages:
                {agent_messages}

                Current progress: {current_progress}

                Your tasks:
                1. Assess the current progress (0.0 to 1.0) based on the quality and completeness of the summary so far. Be extremely critical - progress should rarely exceed 0.1 per iteration.
                2. Provide detailed, exacting feedback on the recent contributions. Point out even minor flaws or areas for improvement.
                3. Decide which agent should contribute next, considering the current deficiencies in the summary.
                4. Only if the summary is absolutely perfect (which is rare before at least 10 iterations), mark it as complete.
                Analyze the current state of the summary and decide on the next action. If the summary is not complete, provide feedback and select the next agent.

                Respond using one of the following action formats:

                1. To provide feedback and select next agent:
                {{
                    "action": "provide_feedback",
                    "feedback": "Your constructive feedback here",
                    "next_agent": "concise_claire" or "analytical_alex" or "creative_cameron"
                }}

                2. To complete the task:
                {{
                    "action": "complete_task",
                    "final_summary": "The complete final summary",
                    "overall_quality": 0.95  # A float between 0 and 1
                }}

                """).strip()
        ),
    ]


@neat.lm(model="mistral/mistral-large-latest", temperature=0.5)
def concise_claire(
    text: str, previous_messages: List[AgentMessage], supervisor_feedback: str
):
    return [
        neat.system("""You are Concise Claire, an agent with a talent for brevity and clarity. 
        Your strength lies in distilling complex information into clear, concise statements. 
        However, you're working under a extremely demanding supervisor, so strive for perfection in your contributions."""),
        neat.user(f"""
Text to summarize: {text}

Previous messages:
{previous_messages}

Supervisor feedback: {supervisor_feedback}

Your task: Contribute to the summary by focusing on clarity and conciseness. Trim any unnecessary details and ensure the key points are presented in a straightforward manner. Remember, your supervisor has extremely high standards, so review and refine your contribution multiple times before submitting.
"""),
    ]


@neat.lm(model="mistral/mistral-large-latest", temperature=0.5)
def analytical_alex(
    text: str, previous_messages: List[AgentMessage], supervisor_feedback: str
):
    return [
        neat.system("""You are Analytical Alex, an agent with a keen eye for detail and a logical approach. 
        Your strength lies in breaking down complex topics and identifying key relationships between ideas. 
        You're working under an extremely demanding supervisor, so aim for flawless analysis in your contributions."""),
        neat.user(f"""
Text to summarize: {text}

Previous messages:
{previous_messages}

Supervisor feedback: {supervisor_feedback}

Your task: Contribute to the summary by analyzing the content deeply. Focus on identifying the most important concepts and their relationships. Ensure that the logical flow of ideas is clear in the summary. Your supervisor expects perfection, so scrutinize your work carefully before submitting.
"""),
    ]


@neat.lm(model="mistral/mistral-large-latest", temperature=0.5)
def creative_cameron(
    text: str, previous_messages: List[AgentMessage], supervisor_feedback: str
):
    return [
        neat.system("""You are Creative Cameron, an agent with a flair for engaging and innovative expression. 
        Your strength lies in finding unique angles and making the content more captivating. 
        You're working under an extremely demanding supervisor, so push yourself to find truly original and insightful ways to express the information."""),
        neat.user(f"""
Text to summarize: {text}

Previous messages:
{previous_messages}

Supervisor feedback: {supervisor_feedback}

Your task: Contribute to the summary by adding a creative touch. Look for interesting angles or connections that others might have missed. Try to make the summary more engaging while maintaining its accuracy. Your supervisor has very high standards, so refine your ideas multiple times to ensure they're truly innovative and effective.
"""),
    ]


def parse_supervisor_message(message: str) -> SupervisorMessage:
    lines = message.split("\n")
    progress = float(lines[0].split(":")[1].strip())
    feedback = lines[1].split(":")[1].strip()
    next_agent = lines[2].split(":")[1].strip()
    return SupervisorMessage(
        overall_progress=progress, feedback=feedback, next_agent=next_agent
    )


def circular_agent_interaction(text: str, max_iterations: int = 10) -> FinalResult:
    agents = {
        "concise_claire": concise_claire,
        "analytical_alex": analytical_alex,
        "creative_cameron": creative_cameron,
    }
    messages = []
    current_progress = 0.0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        overall_task = progress.add_task("[cyan]Overall Progress", total=100)

        for i in range(max_iterations):
            # Supervisor's turn
            supervisor_action: SupervisorAction = supervisor_agent(
                text, messages, current_progress
            )
            print(supervisor_action)

            if supervisor_action.action == "complete_task":
                console.print("[bold green]Task Completed![/bold green]")
                return FinalResult(
                    summary=supervisor_action.final_summary,
                    overall_quality=supervisor_action.overall_quality,
                )

            console.print(
                Panel(
                    f"[bold]Wise Mentor Feedback:[/bold]\n{supervisor_action.feedback}",
                    border_style="magenta",
                )
            )

            # Estimate progress based on iteration count
            estimated_progress = min((i + 1) / max_iterations, 0.99)
            progress.update(overall_task, completed=int(estimated_progress * 100))

            # Selected agent's turn
            if supervisor_action.next_agent not in agents:
                console.print(
                    f"[bold red]Error: Unknown agent '{supervisor_action.next_agent}'[/bold red]"
                )
                continue

            agent_func = agents[supervisor_action.next_agent]
            agent_response = agent_func(text, messages, supervisor_action.feedback)

            messages.append(
                AgentMessage(
                    sender=supervisor_action.next_agent, content=agent_response
                )
            )
            console.print(
                Panel(
                    f"[bold]{supervisor_action.next_agent}:[/bold]\n{agent_response}",
                    border_style="cyan",
                )
            )

    console.print("[bold red]Maximum iterations reached without completion.[/bold red]")
    return FinalResult(summary="Incomplete summary", overall_quality=estimated_progress)


# Example usage
text_to_summarize = """Harris leading Trump by 7 points: Poll
Vice President Harris holds a 7-point edge over former President Trump nationally in a new poll, marking the latest gain for the Democratic presidential candidate as the general election approaches.

A survey from Fairleigh Dickinson University, released last Friday, found Harris leading Trump with 50 percent support to 43 percent nationally, while 7 percent of respondents said they will vote for someone else. Trump and Harris fare equally well with voters from their party, each having 95 percent support from their partisans, pollsters found.

Pollsters noted race or gender played a large role in pushing Harris’s lead. When voters are asked to think about race or gender, Harris’s lead grows significantly, while support for her and Trump are virtually tied when they are not made to think about it, they said.

With independents who do not lean toward either party, Harris still leads Trump, but by a smaller margin, 38 to 33 percent, the poll found. Harris holds a large lead among self-identified liberals, 87 to 10 percent, along with progressives, 93 to 5 percent, and moderates, 62 to 30 percent.

The former president, meanwhile, leads among conservatives 76 to 19 percent, and MAGA voters, 95 to 4 percent.

Trump saw his strongest support among men “who hold traditionally masculine identities,” while women and other men who reject these identities favor Harris, according to pollsters.

“Trump has built his political career around a very specific performance of whiteness and masculinity,” Dan Cassino, a professor of government and politics at Fairleigh Dickinson and the executive director of the poll, said in a release. “In the past, that’s been seen as a strength, but it’s no longer clear that it’s working.”

“Race matters in elections, but it’s not inevitable that voters are thinking about it,” he added. “Trump does reasonably well among nonwhite voters so long as they’re not thinking about race: Once they are, we see a huge shift to Harris.”

Since replacing President Biden atop the Democratic presidential ticket last month, Harris has quickly gained momentum, posing a threat to the healthy lead Trump held over the president, both nationally and in swing states.

This is the latest poll suggesting good news for Harris, though some political strategists have suggested it is too early to make conclusions about the November election.

According to a polling index by Decision Desk HQ and The Hill, Harris has a 3.6 percentage point lead over Trump.

Trump dismissed the notion Harris has made gains in the polls last week.

When asked last Thursday by Fox News anchor Martha MacCallum about Harris’s increasing support in the polls, Trump said, “No, she’s not having success. I’m having success. I’m doing great with the Hispanic voters. I’m doing great with Black men. I’m doing great with women, because women want safety.”

The survey was conducted Aug. 17-20 using a voter list of 801 registered voters nationwide. It was carried out by Braun Research and has a simple sampling error of plus or minus 3.5 percentage points at a 95 percent confidence interval.

Story was updated at 4:06 p.m. PT"""

console.print("[bold]Starting Text Summarization Process[/bold]", style="white on blue")
console.print("Text to summarize:")
console.print(Panel(text_to_summarize, border_style="green"))
console.print()

result = circular_agent_interaction(text_to_summarize)

console.print("\n[bold]Final Result[/bold]", style="white on green")
console.print(f"Summary:\n{result.summary}")
console.print(f"Overall Quality: {result.overall_quality:.2f}")
