# Research Proposal Agentic System: Project Description

## Problem Statement

High school students participating in science competitions like Synopsis face a significant challenge: identifying research topics that are simultaneously accessible to their skill level, relevant to current scientific research, aligned with competition evaluation criteria, and likely to win. This problem is multi-faceted and requires synthesizing information from multiple domains:

1. **Historical Analysis**: Understanding what types of projects have won in the past
2. **Evaluation Criteria**: Knowing how judges assess proposals
3. **Current Research Landscape**: Identifying topics that are actively being researched
4. **Topic Selection**: Choosing a topic that balances all these factors
5. **Proposal Writing**: Crafting a compelling proposal that meets all criteria

Traditionally, students and mentors must manually research winning projects, study competition rubrics, stay current with research trends, and iteratively refine proposals—a time-consuming process that often results in suboptimal outcomes due to incomplete information or misalignment with evaluation criteria.

This problem is important because:
- **Educational Impact**: High-quality research experiences in high school can shape students' academic and career trajectories
- **Accessibility**: Not all students have access to experienced mentors who can guide them through this complex process
- **Efficiency**: The manual process is time-consuming and can take months, limiting students' ability to explore multiple topics
- **Success Rate**: Better-aligned proposals increase students' chances of success, which can open doors to scholarships, recognition, and further research opportunities

## Why Agents?

Agents are the ideal solution to this problem because it requires **collaborative intelligence** across multiple specialized domains. No single agent could effectively:
- Search and analyze historical competition data
- Research current scientific trends
- Correlate patterns between winning projects and evaluation criteria
- Synthesize this information to propose optimal topics
- Write and iteratively refine proposals

The problem naturally decomposes into specialized tasks that benefit from:
1. **Parallel Processing**: Research tasks (winning projects and criteria) can be done simultaneously
2. **Sequential Dependencies**: Analysis must follow research, topic selection must follow analysis
3. **Iterative Refinement**: Proposal writing requires multiple evaluation-revision cycles
4. **State Management**: Each agent's output becomes input for subsequent agents
5. **Tool Integration**: Agents need access to web search, custom analysis functions, and loop control mechanisms

Multi-agent systems excel at this type of problem because they can:
- **Specialize**: Each agent focuses on one aspect, leading to better results
- **Scale**: Easy to add new agents (e.g., for specific competition types)
- **Maintain**: Changes to one agent don't affect others
- **Debug**: Issues can be isolated to specific agents
- **Compose**: Complex workflows emerge from simple agent interactions

## What You Created

The system implements a **multi-agent orchestration architecture** using Google's Agent Development Kit (ADK), consisting of 9 specialized agents organized into a sophisticated workflow:

### Agent Team

1. **WinningProjectsResearcher**: Searches for and compiles winning projects from recent competitions (2020-2024)
2. **CriteriaResearcher**: Researches official evaluation criteria and rubrics from major competitions
3. **CriteriaAnalyzer**: Correlates winning projects with criteria to create practical, actionable guidelines
4. **TopicIntersector**: Identifies topics that have both won competitions AND are currently active research areas
5. **TopicProposer**: Selects the optimal topic and specifies evaluation criteria tailored to that topic
6. **InitialProposalWriter**: Writes the first complete research proposal
7. **InitialProposalEvaluator**: Evaluates the initial proposal and creates feedback
8. **RefinedProposalWriter**: Revises proposals based on evaluation feedback (can exit loop when approved)
9. **RefinementProposalEvaluator**: Evaluates revised proposals during iterative refinement

### Architecture

The workflow combines three orchestration patterns:

```
Parallel Research Phase
    ├─ WinningProjectsResearcher (parallel)
    └─ CriteriaResearcher (parallel)
         ↓
Sequential Analysis Phase
    └─ CriteriaAnalyzer
         ↓
Sequential Topic Discovery Phase
    └─ TopicIntersector
         ↓
Sequential Topic Selection Phase
    └─ TopicProposer
         ↓
Proposal Development Phase
    ├─ Initial Proposal Writing
    ├─ Initial Evaluation (creates evaluation_feedback)
    └─ Refinement Loop (iterative)
         ├─ Refined Proposal Writer
         └─ Refinement Evaluator
```

**Key Design Decisions**:
- **Separate evaluator instances**: Prevents agent parent conflicts in ADK
- **Initial evaluation phase**: Ensures `evaluation_feedback` exists before the refinement loop
- **Loop exit mechanism**: Custom `exit_proposal_loop` function allows graceful termination
- **State management**: All outputs stored in session state for cross-agent communication

## Demo

The system can be run programmatically or via Jupyter notebook:

```bash
python agents/run_programmatically.py
```

**Example Output Flow**:

1. **Winning Projects Research**: 
   - "2023 Synopsis Winner: AI-based water quality monitoring system..."
   - "2022 Regeneron STS Finalist: Machine learning approach to drug discovery..."

2. **Evaluation Criteria Research**:
   - "Synopsis evaluation: 40% Scientific Method, 30% Innovation, 20% Impact, 10% Presentation..."

3. **Practical Criteria Analysis**:
   - "Winning projects consistently demonstrate: clear problem statement, feasible methodology, measurable outcomes..."

4. **Intersected Topics**:
   - "Topic: AI for Environmental Monitoring - Won 3 competitions, 15+ active research papers in 2024..."

5. **Selected Topic Proposal**:
   - "SELECTED TOPIC: Developing an AI-powered system for real-time air quality prediction using low-cost sensors..."

6. **Final Research Proposal**:
   - Complete proposal with title, abstract, introduction, objectives, methodology, expected outcomes, and feasibility analysis

7. **Evaluation Feedback**:
   - "APPROVED" or detailed feedback for improvement

The system handles the entire pipeline from research to final proposal, with iterative refinement ensuring quality.

## The Build

### Technologies Used

- **Google Agent Development Kit (ADK)**: Core framework for agent creation and orchestration
- **Gemini 2.5 Flash Lite**: LLM model for all agents (fast, cost-effective)
- **Python 3.8+**: Implementation language
- **Google Search Tool**: Built-in ADK tool for web research
- **Custom Function Tools**: Python functions wrapped as tools (e.g., `exit_proposal_loop`)

### Architecture Patterns

1. **Agent Types**:
   - `Agent`: Basic LLM agents with instructions and tools
   - `SequentialAgent`: Runs agents in sequence
   - `ParallelAgent`: Runs agents simultaneously
   - `LoopAgent`: Iterates until exit condition

2. **State Management**:
   - `InMemorySessionService`: Manages conversation state
   - `output_key`: Each agent stores results in session state
   - State variables: `{winning_projects}`, `{evaluation_criteria}`, `{practical_criteria}`, `{intersected_topics}`, `{topic_proposal}`, `{research_proposal}`, `{evaluation_feedback}`

3. **Tool Integration**:
   - `google_search`: Web research capability
   - `FunctionTool`: Custom Python functions as tools
   - `exit_proposal_loop`: Loop control mechanism

### Development Process

1. **Design Phase**: Identified 7 core tasks → mapped to specialized agents
2. **Implementation**: Created agents with specific instructions and tools
3. **Orchestration**: Combined agents using parallel, sequential, and loop patterns
4. **Iteration**: Fixed state variable dependencies and agent parent conflicts
5. **Refinement**: Separated initial and refinement phases to ensure proper state initialization

### Key Challenges Solved

- **State Variable Dependencies**: Initial evaluation phase ensures `evaluation_feedback` exists before refinement loop
- **Agent Parent Conflicts**: Separate evaluator instances for initial and refinement phases
- **Runner Configuration**: Switched from `InMemoryRunner` to `Runner` for proper session management
- **Instruction Placeholders**: Careful ordering ensures all referenced state variables exist

### Code Structure

```
agents/
├── agent.py                # All agent definitions and workflow
├── run_programmatically.py # Execution script
└── __init__.py             # Package initialization
```

The system is designed for both programmatic use and interactive notebook exploration.

## If I Had More Time, This Is What I'd Do

I would extend the initial project with a **meta-agent system** that makes the research proposal generation system self-evolving. While I used my intuition to design the team of specialized agents to solve the problem, a meta-agent would read the current `research_proposal_v1` implementation and generate improved versions (`research_proposal_v2`, `v3`, etc.) by:

1. **Architecture Analysis**: The meta-agent would analyze the current agent team structure, workflow patterns, and agent interactions to identify potential improvements

2. **Proposal Generation**: It would propose alternative team structures, such as:
   - Adding new specialized agents (e.g., a "CompetitionTrendAnalyzer" or "MentorFeedbackSimulator")
   - Reorganizing workflow patterns (e.g., different parallel/sequential arrangements)
   - Modifying agent instructions based on performance patterns
   - Adjusting loop iteration strategies

3. **Version Evaluation**: The meta-agent would:
   - Run both the current version and the proposed new version
   - Compare outputs on metrics like proposal quality, coherence, alignment with criteria
   - Evaluate efficiency (execution time, token usage)
   - Assess maintainability and extensibility

4. **Evolutionary Selection**: If the new version performs better, it becomes the baseline for the next iteration. This creates a self-improving system that:
   - Adapts to changing competition landscapes
   - Optimizes for different competition types
   - Learns from successful proposal patterns
   - Continuously refines agent specializations

This meta-agent approach would transform the system from a static, manually-designed solution into a **self-evolving agentic architecture** that improves over time through automated experimentation and evaluation. It would enable the system to discover optimal agent configurations that might not be immediately obvious through manual design, potentially leading to more effective proposal generation strategies.

