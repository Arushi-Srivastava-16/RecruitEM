# 🏗️ Architecture Deep Dive

## Multi-Agent Orchestration Pattern

This implementation demonstrates a **Router-Specialist Pattern** commonly used in production AI systems.

## The Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATOR                                │
│                    (Main Conductor)                              │
└────────────┬────────────────────────────────────────────────────┘
             │
             │ 1. Initialize State
             │
             ▼
    ┌────────────────┐
    │  Router Agent  │◄──── "What kind of task is this?"
    │   (The Brain)  │
    └────────┬───────┘
             │
             │ 2. Route Decision
             │
        ┌────┴────┐
        │         │
        ▼         ▼
┌──────────┐  ┌──────────┐
│Assessment│  │Interview │
│  Agent   │  │  Agent   │
│(Logistics)│  │(Coaching)│
└─────┬────┘  └────┬─────┘
      │            │
      │ 3. Call    │ 3. Call
      │    Tools   │    Tools
      │            │
      ▼            ▼
┌─────────────────────────┐
│  get_test_link()        │
│  rag_search()           │
│  generate_prep_tip()    │
└───────────┬─────────────┘
            │
            │ 4. Build
            │    Response
            │
            ▼
    ┌────────────────┐
    │ Output Message │
    └────────────────┘
```

## Component Breakdown

### 1. **Router Agent** (The Dispatcher)

**Role**: Decision maker

**Input**: `status` from the Recruiter Update

**Logic**: Simple conditional or LLM-based classification

**Output**: Next Node Name (`'assessment_node'` or `'interview_node'`)

```python
def router_agent(state: AgentState) -> Literal["assessment", "interview"]:
    status = state["status"]
    if status.lower() == "assessment":
        return "assessment"
    else:
        return "interview"
```

### 2. **Assessment Agent** (Specialist A)

**Role**: Fetch the correct test link for the job role

**Tools**: `get_assessment_link(job_role)`

**Prompt**: "You are an Assessment Coordinator. Draft a message inviting the candidate to take the test at {link}."

### 3. **Interview Agent** (Specialist B)

**Role**: Analyze the JD and Candidate Profile to give a personalized tip

**Tools**: `rag_retrieve(query)`

**Prompt**: "You are a Career Coach. The candidate is interviewing for {role}. Based on the JD, give them ONE specific, high-impact tip to prepare."

### 4. **The Orchestrator** (The Graph)

Stitching it all together:

```python
def run_orchestrator(state):
    # Step 1: Router
    next_step = router_agent(state)
    
    # Step 2: Delegation
    if next_step == 'assessment':
        response = assessment_agent(state)
    elif next_step == 'interview':
        response = interview_agent(state)
    
    return response
```

## Why This Highlights "Orchestration"?

- **Explicit Handoffs**: Students write the code that passes control from Router → Agent
- **Specialization**: Each agent has a distinct prompt and toolset
- **State Management**: Shows how data (Job ID, Profile) persists across the flow

## State Management

### AgentState (TypedDict)

```python
class AgentState(TypedDict):
    job_id: str
    candidate_id: str
    status: str  # 'Assessment' | 'Interview'
    job_description: str
    candidate_profile: str
    output_message: str
```

**Benefits**:
- Single source of truth
- Type safety
- Easy to debug (can print at any point)
- Clear data flow

## Tool Layer

### Tool 1: `get_test_link(role)`

**Purpose**: Fetch assessment URL for a given role

**Implementation**: Dictionary lookup

**Production Alternative**: Database query or API call

### Tool 2: `rag_search(query)`

**Purpose**: Retrieve relevant information from knowledge base

**Implementation**: Simple keyword matching

**Production Alternative**: Vector database (Pinecone, Weaviate) with embedding-based search

### Tool 3: `generate_prep_tip(jd, use_claude)`

**Purpose**: Generate personalized interview preparation advice

**Implementation**: 
- **Basic Mode**: Keyword matching in tips database
- **AI Mode**: Claude API call for dynamic generation

## Design Principles

1. **Single Responsibility**: Each agent has ONE clear purpose
2. **Observable Execution**: Every step prints to console
3. **Composable Tools**: Tools are simple functions that can be called from any agent
4. **State Immutability (Conceptual)**: Receive state → Do work → Return updated state

