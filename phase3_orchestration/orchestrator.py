#!/usr/bin/env python3
"""
🧠 Smart Recruitment Dispatcher - Multi-Agent Orchestration
==========================================================

A compact, human-readable implementation showing how a router agent
delegates tasks to specialist agents based on candidate status.

Architecture:
    Status Update → Router Agent → [Assessment Agent | Interview Agent] → Output

Author: RecruitEM Team
Date: Dec 2024
"""

from typing import TypedDict, Literal
import os
from datetime import datetime

# ============= DATA (Inline) =============

TEST_LINKS = {
    "Python Developer": "https://assess.example.com/python",
    "Data Analyst": "https://assess.example.com/data",
    "Frontend Developer": "https://assess.example.com/frontend",
    "DevOps Engineer": "https://assess.example.com/devops",
    "Product Manager": "https://assess.example.com/product"
}

JOB_DESCRIPTIONS = {
    "J123": {
        "title": "Python Developer",
        "description": "Python Developer role requiring FastAPI, async programming, REST APIs, PostgreSQL, and Docker. Must have 3+ years experience building scalable backend services."
    },
    "J456": {
        "title": "Data Analyst",
        "description": "Data Analyst role requiring SQL, Tableau, Python for data analysis, statistical modeling, and experience with data warehousing concepts."
    },
    "J789": {
        "title": "Frontend Developer",
        "description": "Frontend Developer role requiring React, TypeScript, modern CSS frameworks, and experience with responsive design and accessibility standards."
    },
    "J101": {
        "title": "DevOps Engineer",
        "description": "DevOps Engineer role requiring Kubernetes, CI/CD pipelines, AWS/Azure, Terraform, and strong Linux system administration skills."
    }
}

INTERVIEW_TIPS_DB = {
    "python": "Review async/await patterns and how to handle concurrent requests efficiently.",
    "fastapi": "Understand dependency injection and how FastAPI uses Pydantic for validation.",
    "sql": "Practice complex JOIN queries and understand indexing strategies for performance.",
    "react": "Be ready to explain the virtual DOM, hooks lifecycle, and state management patterns.",
    "kubernetes": "Know the difference between Deployments, StatefulSets, and DaemonSets."
}

# ============= STATE MANAGEMENT =============

class AgentState(TypedDict):
    """Shared state passed between agents"""
    job_id: str
    candidate_name: str
    candidate_email: str
    status: Literal["Assessment", "Interview"]
    job_title: str
    job_description: str
    output_message: str
    metadata: dict

# ============= TOOLS (Simple Functions) =============

def get_test_link(role: str) -> str:
    """
    Tool: Fetch assessment link for a given role
    
    Args:
        role: Job title/role name
    
    Returns:
        Assessment URL
    """
    link = TEST_LINKS.get(role, "https://assess.example.com/general")
    print(f"  🔧 Tool Called: get_test_link('{role}') → {link}")
    return link

def rag_search(query: str) -> str:
    """
    Tool: Simple RAG (Retrieval Augmented Generation) search
    
    Performs keyword matching in job descriptions and tips database.
    In production, this would query a vector database.
    
    Args:
        query: Search query (job ID or keywords)
    
    Returns:
        Relevant snippet from knowledge base
    """
    print(f"  🔍 Tool Called: rag_search('{query}')")
    
    # First, try to find by job ID
    if query in JOB_DESCRIPTIONS:
        jd = JOB_DESCRIPTIONS[query]
        snippet = f"{jd['title']}: {jd['description'][:150]}..."
        print(f"     → Found JD: {snippet[:80]}...")
        return snippet
    
    # Otherwise, keyword search in tips
    query_lower = query.lower()
    for keyword, tip in INTERVIEW_TIPS_DB.items():
        if keyword in query_lower:
            print(f"     → Found tip for '{keyword}'")
            return tip
    
    return "No specific tips found. General advice: Review the job description carefully and prepare examples from your past experience."

def generate_prep_tip(job_description: str, use_claude: bool = False) -> str:
    """
    Tool: Generate personalized interview prep tip
    
    Args:
        job_description: The job description text
        use_claude: Whether to use Claude API (requires ANTHROPIC_API_KEY)
    
    Returns:
        Interview preparation tip
    """
    print(f"  💡 Tool Called: generate_prep_tip(use_claude={use_claude})")
    
    if use_claude and os.getenv("ANTHROPIC_API_KEY"):
        try:
            from anthropic import Anthropic
            
            client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            
            prompt = f"""Based on this job description, give ONE specific, high-impact tip to help a candidate prepare for their interview. Keep it under 50 words.

Job Description: {job_description}

Tip:"""
            
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}]
            )
            
            tip = message.content[0].text.strip()
            print(f"     → Claude generated tip: {tip[:60]}...")
            return tip
            
        except Exception as e:
            print(f"     ⚠️ Claude API error: {e}, falling back to keyword search")
    
    # Fallback: extract keywords and use tips DB
    keywords = ["python", "sql", "react", "kubernetes", "fastapi"]
    for keyword in keywords:
        if keyword in job_description.lower():
            return INTERVIEW_TIPS_DB.get(keyword, "Review the core concepts for this role.")
    
    return "Study the job requirements and prepare concrete examples from your experience."

# ============= AGENTS (Specialists) =============

def router_agent(state: AgentState) -> Literal["assessment", "interview"]:
    """
    🧠 THE BRAIN: Router Agent
    
    Decides which specialist agent should handle this candidate update.
    This is the orchestration decision point.
    
    Args:
        state: Current agent state
    
    Returns:
        Next agent to call: 'assessment' or 'interview'
    """
    status = state["status"]
    print(f"\n🧠 ROUTER AGENT: Analyzing status='{status}'...")
    
    # Simple rule-based routing (could be LLM-based for complex scenarios)
    if status.lower() == "assessment":
        decision = "assessment"
        print(f"   ✅ Decision: Route to ASSESSMENT AGENT (test logistics)")
    else:
        decision = "interview"
        print(f"   ✅ Decision: Route to INTERVIEW AGENT (prep coaching)")
    
    return decision

def assessment_agent(state: AgentState) -> AgentState:
    """
    📋 SPECIALIST A: Assessment Agent
    
    Handles assessment-related tasks:
    - Fetches correct test link
    - Drafts professional invitation message
    
    Args:
        state: Current agent state
    
    Returns:
        Updated state with output message
    """
    print(f"\n📋 ASSESSMENT AGENT: Processing for {state['candidate_name']}...")
    
    # Use tool to get test link
    test_link = get_test_link(state['job_title'])
    
    # Draft message
    message = f"""Hi {state['candidate_name']}! 🎯

Great news! You've been selected to move forward with the {state['job_title']} position.

Next Step: Please complete your technical assessment at your earliest convenience.

📝 Assessment Link: {test_link}
⏰ Time Limit: 60 minutes
💡 Tip: Review the job description before starting

Best of luck!
RecruitEM Team"""
    
    state["output_message"] = message
    state["metadata"] = {
        "agent": "assessment",
        "test_link": test_link,
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"   ✅ Message drafted: {len(message)} characters")
    return state

def interview_agent(state: AgentState, use_claude: bool = False) -> AgentState:
    """
    🎤 SPECIALIST B: Interview Agent
    
    Handles interview preparation:
    - Retrieves relevant info via RAG
    - Generates personalized prep tip
    - Drafts coaching message
    
    Args:
        state: Current agent state
        use_claude: Whether to use Claude for tip generation
    
    Returns:
        Updated state with output message
    """
    print(f"\n🎤 INTERVIEW AGENT: Processing for {state['candidate_name']}...")
    
    # Use RAG to get relevant context
    jd_snippet = rag_search(state['job_id'])
    
    # Generate personalized tip
    prep_tip = generate_prep_tip(state['job_description'], use_claude=use_claude)
    
    # Draft message
    message = f"""Hi {state['candidate_name']}! 🌟

Congratulations on reaching the interview stage for {state['job_title']}!

📅 Your interview is coming up soon. Here's a personalized tip to help you prepare:

💡 Key Focus Area:
{prep_tip}

📌 Role Context:
{jd_snippet}

Remember: Prepare specific examples from your experience that demonstrate these skills.

You've got this!
RecruitEM Team"""
    
    state["output_message"] = message
    state["metadata"] = {
        "agent": "interview",
        "prep_tip": prep_tip,
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"   ✅ Message drafted: {len(message)} characters")
    return state

# ============= ORCHESTRATOR (The Flow) =============

def orchestrate(
    candidate_name: str,
    candidate_email: str,
    status: Literal["Assessment", "Interview"],
    job_id: str,
    use_claude: bool = False
) -> str:
    """
    🎭 MAIN ORCHESTRATOR: The Conductor
    
    Coordinates the entire multi-agent workflow:
    1. Initializes state
    2. Calls router to decide next step
    3. Delegates to specialist agent
    4. Returns final output
    
    Args:
        candidate_name: Candidate's name
        candidate_email: Candidate's email
        status: Current recruitment status
        job_id: Job posting ID
        use_claude: Whether to use Claude API for dynamic responses
    
    Returns:
        Final message to send to candidate
    """
    print("=" * 70)
    print("🎭 ORCHESTRATOR: Starting multi-agent workflow...")
    print("=" * 70)
    
    # Step 1: Initialize state
    if job_id not in JOB_DESCRIPTIONS:
        print(f"⚠️  Warning: Job ID '{job_id}' not found, using generic data")
        job_title = "Software Engineer"
        job_description = "Software engineering role requiring technical expertise."
    else:
        job_info = JOB_DESCRIPTIONS[job_id]
        job_title = job_info["title"]
        job_description = job_info["description"]
    
    state: AgentState = {
        "job_id": job_id,
        "candidate_name": candidate_name,
        "candidate_email": candidate_email,
        "status": status,
        "job_title": job_title,
        "job_description": job_description,
        "output_message": "",
        "metadata": {}
    }
    
    print(f"📋 Initial State:")
    print(f"   • Candidate: {candidate_name} ({candidate_email})")
    print(f"   • Job: {job_title} ({job_id})")
    print(f"   • Status: {status}")
    
    # Step 2: Router decides the path
    next_agent = router_agent(state)
    
    # Step 3: Delegate to specialist
    if next_agent == "assessment":
        state = assessment_agent(state)
    else:
        state = interview_agent(state, use_claude=use_claude)
    
    # Step 4: Return result
    print(f"\n✅ ORCHESTRATOR: Workflow completed!")
    print(f"   • Agent Used: {state['metadata']['agent']}")
    print(f"   • Output Length: {len(state['output_message'])} chars")
    print("=" * 70)
    
    return state["output_message"]

# ============= DEMO (Run It!) =============

def run_demo(use_claude: bool = False):
    """
    Run demonstration test cases
    
    Args:
        use_claude: Whether to use Claude API (requires ANTHROPIC_API_KEY env var)
    """
    print("\n" + "🚀 " * 25)
    print("SMART RECRUITMENT DISPATCHER - DEMO")
    print("🚀 " * 25 + "\n")
    
    if use_claude:
        if os.getenv("ANTHROPIC_API_KEY"):
            print("✨ Claude API integration: ENABLED\n")
        else:
            print("⚠️  ANTHROPIC_API_KEY not set, using fallback methods\n")
            use_claude = False
    else:
        print("💡 Running in basic mode (set use_claude=True for AI-powered tips)\n")
    
    # Test Case 1: Assessment Path
    print("\n" + "📝 TEST CASE 1: Assessment Path ".center(70, "-"))
    result1 = orchestrate(
        candidate_name="Alice Chen",
        candidate_email="alice@email.com",
        status="Assessment",
        job_id="J123",
        use_claude=use_claude
    )
    print(f"\n✉️  FINAL OUTPUT:\n{'-'*70}\n{result1}\n{'-'*70}\n")
    
    # Test Case 2: Interview Path
    print("\n" + "📝 TEST CASE 2: Interview Path ".center(70, "-"))
    result2 = orchestrate(
        candidate_name="Bob Martinez",
        candidate_email="bob@email.com",
        status="Interview",
        job_id="J456",
        use_claude=use_claude
    )
    print(f"\n✉️  FINAL OUTPUT:\n{'-'*70}\n{result2}\n{'-'*70}\n")
    
    # Test Case 3: Different Role (Frontend)
    print("\n" + "📝 TEST CASE 3: Frontend Assessment ".center(70, "-"))
    result3 = orchestrate(
        candidate_name="Carol Kim",
        candidate_email="carol@email.com",
        status="Assessment",
        job_id="J789",
        use_claude=use_claude
    )
    print(f"\n✉️  FINAL OUTPUT:\n{'-'*70}\n{result3}\n{'-'*70}\n")
    
    print("\n" + "✅ " * 25)
    print("DEMO COMPLETED SUCCESSFULLY!")
    print("✅ " * 25 + "\n")
    
    print("📚 Key Takeaways:")
    print("   1. Router Agent made intelligent routing decisions")
    print("   2. Specialist agents handled their domains (assessment vs interview)")
    print("   3. Tools were called dynamically (get_test_link, rag_search)")
    print("   4. State was maintained and updated throughout the flow")
    print("   5. All orchestration logic is visible and traceable\n")

# ============= MAIN ENTRY POINT =============

if __name__ == "__main__":
    # Run the demo
    # Set use_claude=True and export ANTHROPIC_API_KEY to enable AI-powered tips
    run_demo(use_claude=False)
    
    print("\n💡 To enable Claude-powered interview tips:")
    print("   export ANTHROPIC_API_KEY='your-key-here'")
    print("   python orchestrator.py --claude")
    print("\n📖 Or use it as a library:")
    print("   from orchestrator import orchestrate")
    print("   message = orchestrate('John', 'john@email.com', 'Interview', 'J123')")

