# Research Proposal Agentic System for High School Science Competitions

This project implements a multi-agent system that collaboratively generates research proposals for high school science competitions such as Synopsis. The system uses a team of specialized agents that work together to research, analyze, propose, write, and refine a winning research proposal.

## 🎯 System Overview

The system consists of 7 specialized agents working in a coordinated workflow:

1. **WinningProjectsResearcher** - Searches for and compiles winning projects from recent competitions
2. **CriteriaResearcher** - Researches evaluation criteria and rubrics from major competitions
3. **CriteriaAnalyzer** - Correlates winning projects with criteria and creates practical guidelines
4. **TopicIntersector** - Identifies topics that have won competitions AND are currently active research areas
5. **TopicProposer** - Selects the best topic and specifies evaluation criteria
6. **ProposalWriter** - Writes a comprehensive research proposal
7. **ProposalEvaluator** - Evaluates the proposal and suggests improvements

## 🏗️ Architecture

The workflow uses a combination of parallel, sequential, and loop patterns:

```
┌─────────────────────────────────────────────────────────────┐
│              Research Proposal System                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────┐
        │  Parallel Research Phase           │
        │  ├─ WinningProjectsResearcher     │
        │  └─ CriteriaResearcher            │
        └───────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────┐
        │  Analysis Phase                    │
        │  └─ CriteriaAnalyzer              │
        └───────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────┐
        │  Topic Intersection Phase          │
        │  └─ TopicIntersector              │
        └───────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────┐
        │  Topic Proposal Phase             │
        │  └─ TopicProposer                │
        └───────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────┐
        │  Proposal Refinement Loop         │
        │  ├─ ProposalWriter                │
        │  └─ ProposalEvaluator             │
        │     (iterates until approved)     │
        └───────────────────────────────────┘
```

## 📋 Prerequisites

1. **Python 3.8+**
2. **Google API Key** - You need a Google API key with access to Gemini models
3. **Required packages** (install via `pip install -r requirements.txt`)

## 🚀 Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your API key:**
   
   Create a `.env` file in this directory:
   ```bash
   echo "GOOGLE_API_KEY=your-api-key-here" > .env
   ```
   
   Or set it as an environment variable:
   ```bash
   export GOOGLE_API_KEY='your-api-key-here'
   ```

## 💻 Usage

### Running Programmatically

Run the complete system:

```bash
# From the research_proposal_v1 directory
python agents/run_programmatically.py

# Or from the agents directory
cd agents
python run_programmatically.py
```

This will:
1. Execute all agents in the workflow
2. Display progress and results
3. Show the final research proposal and all intermediate outputs

### Using in Your Code

```python
import asyncio
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from agents.agent import root_agent

async def generate_proposal():
    session_service = InMemorySessionService()
    runner = InMemoryRunner(session_service=session_service)
    session = await session_service.create_session(user_id="student")
    
    query = "Generate a research proposal for a high school science competition"
    
    response = await runner.run_async(
        agent=root_agent,
        session=session,
        user_content=query,
    )
    
    # Access results from session.state
    proposal = session.state.get("research_proposal")
    topic = session.state.get("topic_proposal")
    
    return proposal, topic

# Run it
proposal, topic = asyncio.run(generate_proposal())
```

## 📁 File Structure

```
research_proposal_v1/
├── agents/
│   ├── __init__.py             # Package initialization
│   ├── agent.py                # Main agent definitions and workflow
│   └── run_programmatically.py # Script to run the system
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── research_proposal_system.ipynb  # Notebook version
└── .env                        # API key configuration (create this)
```

## 🔧 Agent Details

### WinningProjectsResearcher
- **Role**: Research specialist
- **Tools**: `google_search`
- **Output**: List of winning projects with titles, descriptions, and competition details

### CriteriaResearcher
- **Role**: Evaluation criteria specialist
- **Tools**: `google_search`
- **Output**: Evaluation criteria and rubrics from major competitions

### CriteriaAnalyzer
- **Role**: Data analyst
- **Input**: Winning projects + Evaluation criteria
- **Output**: Practical, actionable criteria and guidelines

### TopicIntersector
- **Role**: Research strategist
- **Tools**: `google_search`
- **Input**: Winning projects
- **Output**: Topics that have won AND are currently active research areas

### TopicProposer
- **Role**: Topic selection expert
- **Input**: Practical criteria + Intersected topics
- **Output**: Selected topic with evaluation criteria and rubric

### ProposalWriter
- **Role**: Proposal writer
- **Input**: Topic proposal
- **Output**: Complete research proposal
- **Features**: Can exit loop when proposal is approved

### ProposalEvaluator
- **Role**: Proposal evaluator
- **Input**: Research proposal + Topic proposal (with criteria)
- **Output**: Evaluation feedback or "APPROVED"

## 🔄 Workflow Patterns Used

1. **Parallel Pattern**: WinningProjectsResearcher and CriteriaResearcher run simultaneously
2. **Sequential Pattern**: Analysis, intersection, and proposal phases run in sequence
3. **Loop Pattern**: ProposalWriter and ProposalEvaluator iterate until approval

## 🎓 Key Features

- **Multi-agent collaboration**: Specialized agents work together
- **Parallel execution**: Research phase runs in parallel for efficiency
- **Iterative refinement**: Proposal improves through evaluation cycles
- **Comprehensive research**: Uses web search to find real winning projects and criteria
- **Practical output**: Generates actionable proposals aligned with competition criteria

## 📝 Output Structure

The system generates:
- **Winning Projects**: Research on past winners
- **Evaluation Criteria**: Competition rubrics and criteria
- **Practical Criteria**: Analyzed and correlated guidelines
- **Intersected Topics**: Topics meeting both criteria
- **Topic Proposal**: Selected topic with evaluation rubric
- **Research Proposal**: Complete proposal document
- **Evaluation Feedback**: Assessment and improvement suggestions

## ⚙️ Configuration

You can customize:
- **Model**: Change `model="gemini-2.5-flash-lite"` to other Gemini models
- **Max iterations**: Adjust `max_iterations=3` in the LoopAgent
- **Agent instructions**: Modify the `instruction` parameter for each agent

## 🐛 Troubleshooting

1. **API Key Error**: Make sure `GOOGLE_API_KEY` is set in `.env` or environment
2. **Import Errors**: Ensure all dependencies are installed: `pip install -r requirements.txt`
3. **Search Issues**: The system uses `google_search` tool - ensure you have API access

## 📚 Related Tutorials

This project demonstrates concepts from:
- **Day-1b**: Multi-agent architectures (Sequential, Parallel, Loop patterns)
- **Day-2a**: Agent tools (custom tools, google_search)
- **Day-2b**: Agent tools best practices
- **Day-3a**: Agent sessions (state management)
- **Day-4a**: Observability (logging and monitoring)

## 📄 License

This project is part of the 5-day intensive course on agentic systems.

