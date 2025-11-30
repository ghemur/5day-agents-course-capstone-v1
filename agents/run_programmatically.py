"""
Script to run the Research Proposal Agentic System programmatically.

This script demonstrates how to use the agentic system to generate a research proposal
for a high school science competition.
"""

import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Add parent directory to path to allow importing from agents package
# This allows the script to be run from the agents directory or parent directory
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from agents.agent import root_agent

# Load environment variables from parent directory (where .env file is located)
env_path = parent_dir / ".env"
load_dotenv(dotenv_path=env_path)

async def run_research_proposal_system():
    """
    Run the complete research proposal generation system.
    """
    # Initialize session service
    session_service = InMemorySessionService()
    app_name = "ResearchProposalSystem"
    user_id = "student_researcher"
    session_id = "research_session"
    
    # Create runner with session service
    runner = Runner(
        agent=root_agent,
        app_name=app_name,
        session_service=session_service,
    )
    
    # Create a session
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )
    
    print("=" * 80)
    print("🔬 Research Proposal Agentic System for High School Science Competitions")
    print("=" * 80)
    print("\nThis system will:")
    print("1. Research winning projects and evaluation criteria")
    print("2. Analyze and correlate criteria with winning projects")
    print("3. Intersect winning topics with current research")
    print("4. Propose a topic with evaluation criteria")
    print("5. Write and iteratively refine a research proposal")
    print("\n" + "=" * 80 + "\n")
    
    # User query - can be customized
    user_query = """Generate a research proposal for a high school science competition 
    such as Synopsis. The proposal should be for a one-semester research project that:
    - Is accessible to high school students
    - Is of interest to society, humanity, community, and research community
    - Is an area of current active research
    - Has a good chance of winning based on competition criteria"""
    
    print(f"📝 User Query:\n{user_query}\n")
    print("=" * 80)
    print("🚀 Starting agentic workflow...\n")
    
    # Convert query to Content format
    user_content = types.Content(
        role="user",
        parts=[types.Part(text=user_query)]
    )
    
    # Run the agent
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=user_content,
    ):
        # Process events if needed
        pass
    
    # Get the final session to access state
    final_session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )
    
    # Display results
    print("\n" + "=" * 80)
    print("✅ Workflow Complete!")
    print("=" * 80)
    
    # Extract and display key outputs from session state
    state = final_session.state
    
    print("\n📊 Key Outputs:\n")
    
    if "winning_projects" in state:
        print("1️⃣  WINNING PROJECTS RESEARCH:")
        print("-" * 80)
        print(state["winning_projects"][:500] + "..." if len(state.get("winning_projects", "")) > 500 else state.get("winning_projects", ""))
        print()
    
    if "evaluation_criteria" in state:
        print("2️⃣  EVALUATION CRITERIA RESEARCH:")
        print("-" * 80)
        print(state["evaluation_criteria"][:500] + "..." if len(state.get("evaluation_criteria", "")) > 500 else state.get("evaluation_criteria", ""))
        print()
    
    if "practical_criteria" in state:
        print("3️⃣  PRACTICAL CRITERIA ANALYSIS:")
        print("-" * 80)
        print(state["practical_criteria"][:500] + "..." if len(state.get("practical_criteria", "")) > 500 else state.get("practical_criteria", ""))
        print()
    
    if "intersected_topics" in state:
        print("4️⃣  INTERSECTED TOPICS:")
        print("-" * 80)
        print(state["intersected_topics"][:500] + "..." if len(state.get("intersected_topics", "")) > 500 else state.get("intersected_topics", ""))
        print()
    
    if "topic_proposal" in state:
        print("5️⃣  SELECTED TOPIC PROPOSAL:")
        print("-" * 80)
        print(state["topic_proposal"])
        print()
    
    if "research_proposal" in state:
        print("6️⃣  FINAL RESEARCH PROPOSAL:")
        print("=" * 80)
        print(state["research_proposal"])
        print()
    
    if "evaluation_feedback" in state:
        print("7️⃣  EVALUATION FEEDBACK:")
        print("-" * 80)
        print(state["evaluation_feedback"])
        print()
    
    print("=" * 80)
    print("✨ Process Complete!")
    print("=" * 80)
    
    return final_session


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  Warning: GOOGLE_API_KEY not found in environment variables.")
        print("Please set it in your .env file or environment.")
        print("Example: export GOOGLE_API_KEY='your-api-key-here'")
    
    # Run the async function
    asyncio.run(run_research_proposal_system())

