# 🎬 Visual Walkthrough: Watch the Orchestrator Think

Step-by-step visual guide of how the orchestrator processes a candidate update.

## Scenario: Alice Gets an Assessment Invitation

### Step 1: Input Arrives

```
┌─────────────────────────────────────┐
│  📥 INPUT                            │
├─────────────────────────────────────┤
│  Candidate: Alice Chen              │
│  Email: alice@email.com             │
│  Status: Assessment                 │
│  Job ID: J123                       │
└─────────────────────────────────────┘
```

### Step 2: State Initialization

```
┌─────────────────────────────────────┐
│  🗂️  BUILDING STATE                  │
├─────────────────────────────────────┤
│  job_id: "J123"                     │
│  candidate_name: "Alice Chen"       │
│  status: "Assessment"               │
│  job_title: "Python Developer"      │
│  output_message: ""                 │
└─────────────────────────────────────┘
```

### Step 3: Router Thinks

```
         ┌─────────────┐
         │  🧠 ROUTER  │
         │   AGENT     │
         └──────┬──────┘
                │
                │ Analyzing: status == "Assessment"
                │
         ┌──────▼──────┐
         │  Decision:  │
         │ "assessment"│
         └─────────────┘
```

**Console Output**:
```
🧠 ROUTER AGENT: Analyzing status='Assessment'...
   ✅ Decision: Route to ASSESSMENT AGENT
```

### Step 4: Assessment Agent Activates

```
         ┌──────────────────┐
         │  📋 ASSESSMENT   │
         │     AGENT        │
         └────────┬─────────┘
                  │
                  │ Task: Get test link & draft message
                  │
         ┌────────▼─────────┐
         │  Need to call:   │
         │  get_test_link() │
         └──────────────────┘
```

### Step 5: Tool Call - Get Test Link

```
         ┌──────────────────────┐
         │  🔧 TOOL             │
         │  get_test_link()     │
         └──────┬───────────────┘
                │
                │ Input: "Python Developer"
                │
         ┌──────▼───────────────┐
         │ TEST_LINKS lookup:   │
         │ "Python Developer"   │
         │        ↓             │
         │ https://assess...    │
         └──────────────────────┘
```

**Console Output**:
```
  🔧 Tool Called: get_test_link('Python Developer') → https://assess.example.com/python
```

### Step 6: Message Drafting

```
         ┌──────────────────────────────┐
         │  ✍️  DRAFTING MESSAGE         │
         ├──────────────────────────────┤
         │  Template:                   │
         │  "Hi {name}! 🎯              │
         │   Test link: {link}          │
         │   Time: 60 minutes"          │
         │                              │
         │  Variables:                  │
         │  • name = "Alice Chen"       │
         │  • link = "https://..."      │
         └──────────────────────────────┘
```

### Step 7: Final Output

```
┌────────────────────────────────────────────────────┐
│  ✉️  OUTPUT MESSAGE                                │
├────────────────────────────────────────────────────┤
│  Hi Alice Chen! 🎯                                 │
│                                                    │
│  Great news! You've been selected to move forward │
│  with the Python Developer position.              │
│                                                    │
│  📝 Assessment Link:                               │
│     https://assess.example.com/python             │
│  ⏰ Time Limit: 60 minutes                        │
│                                                    │
│  Best of luck!                                     │
│  RecruitEM Team                                   │
└────────────────────────────────────────────────────┘
```

## Alternative Flow: Interview Path

If status was "Interview" instead:

1. Router → Decision: "interview"
2. Interview Agent activates
3. Calls 2 tools: `rag_search()` and `generate_prep_tip()`
4. Drafts coaching message with tips
5. Returns personalized prep advice

## The Full Picture

```
                    INPUT
                      │
                      ▼
              ┌───────────────┐
              │ ORCHESTRATOR  │
              │   (Init)      │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │  ROUTER       │◄──── "What kind of task?"
              │  AGENT        │
              └───────┬───────┘
                      │
         ┌────────────┴────────────┐
         │                         │
         ▼                         ▼
┌─────────────────┐      ┌─────────────────┐
│  ASSESSMENT     │      │  INTERVIEW      │
│  AGENT          │      │  AGENT          │
└────────┬────────┘      └────────┬────────┘
         │                        │
         │ Calls:                 │ Calls:
         │ • get_test_link()      │ • rag_search()
         │                        │ • generate_tip()
         │                        │
         └────────┬───────────────┘
                  │
                  ▼
          ┌───────────────┐
          │ Draft Message │
          └───────┬───────┘
                  │
                  ▼
              OUTPUT
```

## Key Observations

1. **Linear Flow**: Input → Router → Specialist → Tools → Output
2. **Decision Point**: Router is the only branching point
3. **Tool Usage**: Different specialists use different tools
4. **Observable**: Every step prints to console
5. **State Flows Through**: Like a conveyor belt carrying data

