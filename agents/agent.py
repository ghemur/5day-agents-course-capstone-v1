"""
Research Proposal Agentic System for High School Science Competitions

This system uses a team of specialized agents to:
1. Research winning projects and evaluation criteria
2. Analyze and correlate criteria with winning projects
3. Intersect winning topics with current research
4. Propose a topic with evaluation criteria
5. Write and iteratively refine a research proposal
"""

import logging
import os
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.tools import FunctionTool, google_search
from google.genai import types

# ============================================================================
# Logging Configuration
# ============================================================================

# Get the directory where this script is located
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(_CURRENT_DIR, "agent.log")

# Configure logging with DEBUG log level for comprehensive observability
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    force=True,  # Force reconfiguration in case logging was already configured
)

# Configure ADK loggers to capture framework-level logs
adk_logger = logging.getLogger("google.adk")
adk_logger.setLevel(logging.DEBUG)

# Get a logger for this module
module_logger = logging.getLogger(__name__)
module_logger.info("Research Proposal Agentic System - Logging initialized")
module_logger.debug(f"Log file: {LOG_FILE}")

print(f"✅ Logging configured - log file: {LOG_FILE}")

# ============================================================================
# Custom Tools
# ============================================================================

def exit_proposal_loop():
    """
    Call this function when the proposal evaluation indicates approval.
    This exits the iterative refinement loop.
    """
    return {"status": "approved", "message": "Proposal approved. Exiting refinement loop."}


# ============================================================================
# Agent 1: WinningProjectsResearcher
# ============================================================================

winning_projects_researcher = Agent(
    name="WinningProjectsResearcher",
    model="gemini-2.5-flash-lite",
    instruction="""You are a research specialist focused on finding winning high school science competition projects.

Your task is to search for and compile information about projects that have won major high school science competitions 
(such as Synopsis, Regeneron Science Talent Search, Intel ISEF, Google Science Fair, etc.) in recent years (2020-2024).

For each winning project you find, extract:
- Project title
- Brief description (2-3 sentences)
- Competition name and year
- Key research area/topic

Present your findings as a structured list with at least 8-10 winning projects across different scientific disciplines.
Focus on projects that demonstrate:
- Real-world relevance and societal impact
- Scientific rigor appropriate for high school students
- Innovation and creativity

Use the google_search tool to find this information.""",
    tools=[google_search],
    output_key="winning_projects",
)

# ============================================================================
# Agent 2: CriteriaResearcher
# ============================================================================

criteria_researcher = Agent(
    name="CriteriaResearcher",
    model="gemini-2.5-flash-lite",
    instruction="""You are a specialist in understanding evaluation criteria for high school science competitions.

Your task is to search for and compile the official criteria and rubrics used to evaluate projects in major 
high school science competitions (Synopsis, Regeneron STS, Intel ISEF, Google Science Fair, etc.).

For each competition, extract:
- Evaluation criteria categories (e.g., Scientific Method, Innovation, Impact, Presentation)
- Scoring rubrics or point allocations
- Key factors that judges look for
- Common reasons projects win or lose

Present your findings in a structured format that clearly shows:
- What criteria are most important
- How projects are scored
- What distinguishes winning projects

Use the google_search tool to find this information.""",
    tools=[google_search],
    output_key="evaluation_criteria",
)

# ============================================================================
# Agent 3: CriteriaAnalyzer
# ============================================================================

criteria_analyzer = Agent(
    name="CriteriaAnalyzer",
    model="gemini-2.5-flash-lite",
    instruction="""You are an expert analyst who correlates winning projects with evaluation criteria.

Your task is to analyze the winning projects and evaluation criteria provided, and create a practical, 
actionable set of criteria and rubrics that can guide the generation of a winning topic and project proposal.

Inputs:
- Winning Projects: {winning_projects}
- Evaluation Criteria: {evaluation_criteria}

Analyze:
1. What common characteristics do winning projects share?
2. How do these characteristics align with the evaluation criteria?
3. What patterns emerge across different competitions?
4. What are the critical success factors?

Output a comprehensive, practical guide that includes:
- A prioritized list of evaluation criteria (most important first)
- Specific rubrics or checklists for each criterion
- Key characteristics that winning projects demonstrate
- Actionable guidelines for topic selection
- Actionable guidelines for proposal writing

Format your output clearly with sections and bullet points.""",
    output_key="practical_criteria",
)

# ============================================================================
# Agent 4: TopicIntersector
# ============================================================================

topic_intersector = Agent(
    name="TopicIntersector",
    model="gemini-2.5-flash-lite",
    instruction="""You are a research strategist who identifies topics that are both:
1. Proven winners in high school competitions
2. Currently of active interest to the research community

Your task is to:
1. Extract the main topic areas from the winning projects: {winning_projects}
2. For each topic area, search for current active research using google_search
3. Identify 3-5 topics that meet BOTH criteria:
   - Have won competitions (proven track record)
   - Are currently active areas of research (2024-2025)

For each selected topic, provide:
- Topic name and brief description
- Evidence it has won competitions (cite specific projects)
- Evidence of current research activity
- Why it's suitable for high school students (accessibility)
- Why it matters to society/humanity

Use google_search to verify current research activity for each topic.""",
    tools=[google_search],
    output_key="intersected_topics",
)

# ============================================================================
# Agent 5: TopicProposer
# ============================================================================

topic_proposer = Agent(
    name="TopicProposer",
    model="gemini-2.5-flash-lite",
    instruction="""You are a topic selection expert who proposes the best research topic for a high school science competition.

Based on the following inputs:
- Practical Criteria: {practical_criteria}
- Intersected Topics: {intersected_topics}

Your task is to:
1. Select the BEST single topic from the intersected topics that:
   - Best aligns with the practical criteria
   - Has the highest potential for winning
   - Is most accessible to high school students
   - Has strong societal/research community interest

2. Specify the evaluation criteria and rubric that will be used to evaluate a project with this topic:
   - Adapt the practical criteria to this specific topic
   - Create a detailed rubric with scoring guidelines
   - Identify key success factors for this topic

Output your proposal in this format:

**SELECTED TOPIC:**
[Topic name and description]

**WHY THIS TOPIC:**
- Alignment with winning criteria: [explanation]
- Accessibility for high school students: [explanation]
- Current research interest: [explanation]
- Societal impact: [explanation]

**EVALUATION CRITERIA AND RUBRIC:**
[Detailed criteria and scoring rubric specific to this topic]

**KEY SUCCESS FACTORS:**
[List of critical factors that will determine success]""",
    output_key="topic_proposal",
)

# ============================================================================
# Agent 6: Initial ProposalWriter (for first iteration)
# ============================================================================

initial_proposal_writer = Agent(
    name="InitialProposalWriter",
    model="gemini-2.5-flash-lite",
    instruction="""You are an expert proposal writer for high school science competitions.

Your task is to write a comprehensive research proposal based on:
- Selected Topic: {topic_proposal}

Write a complete research proposal that includes:

1. **Title**: Clear, descriptive, and engaging
2. **Abstract/Summary**: Brief overview (150-200 words)
3. **Introduction & Background**: 
   - Problem statement
   - Why this research matters (societal, community, research community)
   - Current state of knowledge
4. **Research Objectives**: Clear, specific, measurable objectives
5. **Methodology**: 
   - Detailed research plan
   - Methods appropriate for high school students
   - Timeline for one semester
   - Resources needed
6. **Expected Outcomes & Impact**:
   - What will be learned/discovered
   - How it benefits society/humanity
   - Contribution to research community
7. **Feasibility**: 
   - Why this is achievable in one semester
   - Student capabilities required
   - Risk assessment and mitigation

The proposal should be:
- Well-structured and professional
- Aligned with the evaluation criteria and rubric specified in the topic proposal
- Appropriate for high school level
- Compelling and likely to win""",
    output_key="research_proposal",
)

# ============================================================================
# Agent 7: ProposalEvaluator (for initial evaluation)
# ============================================================================

initial_proposal_evaluator = Agent(
    name="InitialProposalEvaluator",
    model="gemini-2.5-flash-lite",
    instruction="""You are a strict but fair evaluator of high school science research proposals.

Your task is to evaluate the research proposal against the criteria and rubric specified in the topic proposal.

Inputs:
- Research Proposal: {research_proposal}
- Topic Proposal (contains criteria): {topic_proposal}

Evaluate the proposal on:
1. Alignment with evaluation criteria
2. Scientific rigor and methodology
3. Feasibility for high school students
4. Potential impact and significance
5. Clarity and presentation quality
6. Likelihood of winning

Provide:
- Overall assessment (score/rating)
- Strengths of the proposal
- Specific weaknesses or gaps
- Actionable suggestions for improvement

If the proposal meets all criteria and has a high likelihood of winning, respond with EXACTLY: "APPROVED"
Otherwise, provide detailed, specific feedback for improvement.""",
    output_key="evaluation_feedback",
)

# ============================================================================
# Agent 8: ProposalEvaluator (for refinement loop)
# ============================================================================

refinement_proposal_evaluator = Agent(
    name="RefinementProposalEvaluator",
    model="gemini-2.5-flash-lite",
    instruction="""You are a strict but fair evaluator of high school science research proposals.

Your task is to evaluate the research proposal against the criteria and rubric specified in the topic proposal.

Inputs:
- Research Proposal: {research_proposal}
- Topic Proposal (contains criteria): {topic_proposal}

Evaluate the proposal on:
1. Alignment with evaluation criteria
2. Scientific rigor and methodology
3. Feasibility for high school students
4. Potential impact and significance
5. Clarity and presentation quality
6. Likelihood of winning

Provide:
- Overall assessment (score/rating)
- Strengths of the proposal
- Specific weaknesses or gaps
- Actionable suggestions for improvement

If the proposal meets all criteria and has a high likelihood of winning, respond with EXACTLY: "APPROVED"
Otherwise, provide detailed, specific feedback for improvement.""",
    output_key="evaluation_feedback",
)

# ============================================================================
# Workflow Orchestration
# ============================================================================

# Step 1: Parallel research phase - both researchers work simultaneously
parallel_research_phase = ParallelAgent(
    name="ParallelResearchPhase",
    sub_agents=[winning_projects_researcher, criteria_researcher],
)

# Step 2: Analysis phase - analyze criteria after research is complete
analysis_phase = SequentialAgent(
    name="AnalysisPhase",
    sub_agents=[criteria_analyzer],
)

# Step 3: Topic intersection phase - find topics that meet both criteria
topic_intersection_phase = SequentialAgent(
    name="TopicIntersectionPhase",
    sub_agents=[topic_intersector],
)

# Step 4: Topic proposal phase - select best topic with criteria
topic_proposal_phase = SequentialAgent(
    name="TopicProposalPhase",
    sub_agents=[topic_proposer],
)

# Step 5: Proposal refinement loop - iterative improvement
# Create a refined proposal writer that can exit the loop
# This writer is used for revisions after the initial proposal
# Note: evaluation_feedback will be available after the evaluator runs (which runs first in the loop)
refined_proposal_writer = Agent(
    name="RefinedProposalWriter",
    model="gemini-2.5-flash-lite",
    instruction="""You are an expert proposal writer for high school science competitions.

Your task is to revise the research proposal based on:
- Selected Topic: {topic_proposal}
- Current Proposal: {research_proposal}
- Evaluation Feedback (from the evaluator): {evaluation_feedback}

IMPORTANT: 
- Check the evaluation feedback. If it is EXACTLY "APPROVED", you MUST call the `exit_proposal_loop` function.
- Otherwise, revise the proposal to address all feedback points while maintaining all required sections:
  1. Title
  2. Abstract/Summary (150-200 words)
  3. Introduction & Background
  4. Research Objectives
  5. Methodology
  6. Expected Outcomes & Impact
  7. Feasibility

The revised proposal should be well-structured, aligned with criteria, and compelling.""",
    output_key="research_proposal",
    tools=[FunctionTool(exit_proposal_loop)],
)

# Create the refinement workflow
# Step 1: Write initial proposal
initial_proposal_phase = SequentialAgent(
    name="InitialProposalPhase",
    sub_agents=[initial_proposal_writer],
)

# Step 2: Initial evaluation (creates evaluation_feedback so it exists for the loop)
initial_evaluation_phase = SequentialAgent(
    name="InitialEvaluationPhase",
    sub_agents=[initial_proposal_evaluator],
)

# Step 3: Refinement loop for iterative improvement
# Order: Writer (revises based on feedback), then Evaluator (evaluates revised proposal)
# Note: evaluation_feedback exists from initial evaluation, so writer can reference it
proposal_refinement_loop = LoopAgent(
    name="ProposalRefinementLoop",
    sub_agents=[refined_proposal_writer, refinement_proposal_evaluator],
    max_iterations=3,  # Limit iterations to prevent infinite loops
)

# Combine all phases: initial proposal → initial evaluation → refinement loop
proposal_development_phase = SequentialAgent(
    name="ProposalDevelopmentPhase",
    sub_agents=[
        initial_proposal_phase,      # Write initial proposal
        initial_evaluation_phase,    # Evaluate it (creates evaluation_feedback)
        proposal_refinement_loop,    # Refine iteratively
    ],
)

# Root agent: Orchestrates the entire workflow
root_agent = SequentialAgent(
    name="ResearchProposalSystem",
    sub_agents=[
        parallel_research_phase,       # Step 1: Parallel research
        analysis_phase,                # Step 2: Analyze criteria
        topic_intersection_phase,      # Step 3: Intersect topics
        topic_proposal_phase,          # Step 4: Propose topic
        proposal_development_phase,    # Step 5: Write initial proposal and refine
    ],
)

module_logger.info("All agents and workflow orchestration complete")
module_logger.info(f"Root agent '{root_agent.name}' created with {len(root_agent.sub_agents)} phases")

