#!/usr/bin/env python3
"""
Smart Recruitment Dispatcher - Multi-Agent Orchestration
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

# ANSI color codes for terminal output
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Text colors
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    RED = '\033[31m'
    WHITE = '\033[37m'
    
    # Background colors
    BG_BLUE = '\033[44m'
    BG_CYAN = '\033[46m'

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
    print(f"  {Colors.CYAN}→ Tool: get_test_link('{role}') → {link}{Colors.RESET}")
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
    print(f"  {Colors.CYAN}→ Tool: rag_search('{query}'){Colors.RESET}")
    
    # First, try to find by job ID
    if query in JOB_DESCRIPTIONS:
        jd = JOB_DESCRIPTIONS[query]
        snippet = f"{jd['title']}: {jd['description'][:150]}..."
        print(f"     {Colors.CYAN}→ Found JD: {snippet[:80]}...{Colors.RESET}")
        return snippet
    
    # Otherwise, keyword search in tips
    query_lower = query.lower()
    for keyword, tip in INTERVIEW_TIPS_DB.items():
        if keyword in query_lower:
            print(f"     {Colors.CYAN}→ Found tip for '{keyword}'{Colors.RESET}")
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
    print(f"  {Colors.CYAN}→ Tool: generate_prep_tip(use_claude={use_claude}){Colors.RESET}")
    
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
            print(f"     {Colors.CYAN}→ Claude generated tip: {tip[:60]}...{Colors.RESET}")
            return tip
            
        except Exception as e:
            print(f"     {Colors.RED}! Warning: Claude API error: {e}, falling back to keyword search{Colors.RESET}")
    
    # Fallback: extract keywords and use tips DB
    keywords = ["python", "sql", "react", "kubernetes", "fastapi"]
    for keyword in keywords:
        if keyword in job_description.lower():
            return INTERVIEW_TIPS_DB.get(keyword, "Review the core concepts for this role.")
    
    return "Study the job requirements and prepare concrete examples from your experience."

# ============= AGENTS (Specialists) =============

def router_agent(state: AgentState) -> Literal["assessment", "interview"]:
    """
    Router Agent - The decision maker
    
    This is the brain of the system. It looks at the candidate's status
    and decides which specialist agent should handle the task.
    Think of it as a dispatcher that routes work to the right team.
    
    Args:
        state: Current agent state with candidate info and status
    
    Returns:
        Next agent to call: 'assessment' or 'interview'
    """
    status = state["status"]
    print(f"\n{Colors.YELLOW}{Colors.BOLD}→ Router: Analyzing status='{status}'...{Colors.RESET}")
    
    # Simple rule-based routing (could be LLM-based for complex scenarios)
    if status.lower() == "assessment":
        decision = "assessment"
        print(f"   {Colors.GREEN}✓ Decision: Route to ASSESSMENT AGENT (test logistics){Colors.RESET}")
    else:
        decision = "interview"
        print(f"   {Colors.GREEN}✓ Decision: Route to INTERVIEW AGENT (prep coaching){Colors.RESET}")
    
    return decision

def assessment_agent(state: AgentState) -> AgentState:
    """
    Assessment Agent - Handles test logistics
    
    This agent is responsible for assessment-related tasks.
    It fetches the right test link for the job role and drafts
    a professional invitation message for the candidate.
    
    Args:
        state: Current agent state with candidate and job info
    
    Returns:
        Updated state with the generated message
    """
    print(f"\n{Colors.BLUE}{Colors.BOLD}→ Assessment Agent: Processing for {state['candidate_name']}...{Colors.RESET}")
    
    # Use tool to get test link
    test_link = get_test_link(state['job_title'])
    
    # Draft message
    message = f"""Hi {state['candidate_name']}!

Great news! You've been selected to move forward with the {state['job_title']} position.

Next Step: Please complete your technical assessment at your earliest convenience.

→ Assessment Link: {test_link}
→ Time Limit: 60 minutes
→ Tip: Review the job description before starting

Best of luck!
RecruitEM Team"""
    
    state["output_message"] = message
    state["metadata"] = {
        "agent": "assessment",
        "test_link": test_link,
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"   {Colors.GREEN}✓ Message drafted: {len(message)} characters{Colors.RESET}")
    return state

def interview_agent(state: AgentState, use_claude: bool = False) -> AgentState:
    """
    Interview Agent - Provides coaching and prep tips
    
    This agent helps candidates prepare for interviews by:
    - Searching the job description for relevant context
    - Generating personalized preparation tips
    - Drafting an encouraging coaching message
    
    Args:
        state: Current agent state with candidate and job info
        use_claude: If True, uses Claude AI for tip generation (requires API key)
    
    Returns:
        Updated state with the generated coaching message
    """
    print(f"\n{Colors.MAGENTA}{Colors.BOLD}→ Interview Agent: Processing for {state['candidate_name']}...{Colors.RESET}")
    
    # Use RAG to get relevant context
    jd_snippet = rag_search(state['job_id'])
    
    # Generate personalized tip
    prep_tip = generate_prep_tip(state['job_description'], use_claude=use_claude)
    
    # Draft message
    message = f"""Hi {state['candidate_name']}!

Congratulations on reaching the interview stage for {state['job_title']}!

→ Your interview is coming up soon. Here's a personalized tip to help you prepare:

→ Key Focus Area:
{prep_tip}

→ Role Context:
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
    
    print(f"   {Colors.GREEN}✓ Message drafted: {len(message)} characters{Colors.RESET}")
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
    Main Orchestrator - Coordinates the entire workflow
    
    This is the main function that ties everything together.
    It initializes the state, calls the router to decide which
    agent to use, delegates to the appropriate specialist,
    and returns the final message.
    
    Think of it as the conductor of an orchestra - it doesn't
    play the instruments, but it coordinates when each one plays.
    
    Args:
        candidate_name: The candidate's name
        candidate_email: The candidate's email address
        status: Current recruitment status ("Assessment" or "Interview")
        job_id: The job posting ID (e.g., "J123")
        use_claude: If True, uses Claude AI for interview tips (optional)
    
    Returns:
        The final message string to send to the candidate
    """
    print("=" * 70)
    print(f"{Colors.BOLD}{Colors.WHITE}→ Orchestrator: Starting multi-agent workflow...{Colors.RESET}")
    print("=" * 70)
    
    # Step 1: Initialize state with candidate and job information
    if job_id not in JOB_DESCRIPTIONS:
        print(f"{Colors.RED}{Colors.BOLD}! Warning: Job ID '{job_id}' not found, using generic data{Colors.RESET}")
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
    
    print(f"{Colors.CYAN}→ Initial State:{Colors.RESET}")
    print(f"   {Colors.WHITE}• Candidate: {candidate_name} ({candidate_email}){Colors.RESET}")
    print(f"   {Colors.WHITE}• Job: {job_title} ({job_id}){Colors.RESET}")
    print(f"   {Colors.WHITE}• Status: {status}{Colors.RESET}")
    
    # Step 2: Router decides the path
    next_agent = router_agent(state)
    
    # Step 3: Delegate to specialist
    if next_agent == "assessment":
        state = assessment_agent(state)
    else:
        state = interview_agent(state, use_claude=use_claude)
    
    # Step 4: Return result
    print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Orchestrator: Workflow completed!{Colors.RESET}")
    print(f"   {Colors.WHITE}• Agent Used: {state['metadata']['agent']}{Colors.RESET}")
    print(f"   {Colors.WHITE}• Output Length: {len(state['output_message'])} chars{Colors.RESET}")
    print("=" * 70)
    
    return state["output_message"]

# ============= MAIN ENTRY POINT =============

if __name__ == "__main__":
    # When run directly, execute the demo script
    import subprocess
    import sys
    
    print("Running demonstration...\n")
    subprocess.run([sys.executable, "demo.py"])

