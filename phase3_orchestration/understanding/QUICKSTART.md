# ⚡ Quick Start Guide

Get up and running in 60 seconds!

## Instant Run (No Setup)

```bash
cd phase3_orchestration
python3 orchestrator.py
```

**That's it!** Works immediately with zero dependencies.

## With Virtual Environment

```bash
cd phase3_orchestration

# Automated setup
./setup.sh     # macOS/Linux
setup.bat      # Windows

# OR manual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # Optional: only for Claude
python3 orchestrator.py
```

## What You'll See

```
🧠 ROUTER AGENT: Analyzing status='Assessment'...
   ✅ Decision: Route to ASSESSMENT AGENT

📋 ASSESSMENT AGENT: Processing for Alice Chen...
  🔧 Tool Called: get_test_link('Python Developer')
   ✅ Message drafted: 345 characters

✉️  FINAL OUTPUT:
Hi Alice Chen! 🎯
Great news! You've been selected...
```

## Try Examples

```bash
python3 examples.py
```

## Use as Library

```python
from orchestrator import orchestrate

message = orchestrate(
    candidate_name="Alice Chen",
    candidate_email="alice@email.com",
    status="Assessment",
    job_id="J123"
)
```

## Enable Claude (Optional)

```bash
export ANTHROPIC_API_KEY='your-key-here'
python3 -c "from orchestrator import run_demo; run_demo(use_claude=True)"
```

## Customize

### Add Your Own Jobs

Edit `orchestrator.py` line ~25:

```python
JOB_DESCRIPTIONS["J999"] = {
    "title": "Your Job Title",
    "description": "Your job description here..."
}
```

### Add Test Links

Edit `orchestrator.py` line ~18:

```python
TEST_LINKS["Your Role"] = "https://your-assessment-platform.com/test"
```

## Next Steps

1. ✅ Run the demo
2. ✅ Read `orchestrator.py` top-to-bottom
3. ✅ Try the examples
4. ✅ Customize for your use case
5. ✅ Integrate with your system

