#!/usr/bin/env python3
"""
📚 Examples - Using the Smart Recruitment Dispatcher

This file shows different ways to use the orchestrator system.
"""

from orchestrator import orchestrate

# ============= EXAMPLE 1: Basic Usage =============

def example_basic():
    """Most straightforward use case"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Assessment Invitation")
    print("="*70)
    
    message = orchestrate(
        candidate_name="Sarah Johnson",
        candidate_email="sarah.j@email.com",
        status="Assessment",
        job_id="J123"
    )
    
    print(f"\nGenerated Message:\n{message}\n")


# ============= EXAMPLE 2: Interview Preparation =============

def example_interview():
    """Generate interview prep message"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Interview Preparation Coaching")
    print("="*70)
    
    message = orchestrate(
        candidate_name="Michael Chen",
        candidate_email="m.chen@email.com",
        status="Interview",
        job_id="J456"
    )
    
    print(f"\nGenerated Message:\n{message}\n")


# ============= EXAMPLE 3: Batch Processing =============

def example_batch():
    """Process multiple candidates"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Batch Processing Multiple Candidates")
    print("="*70)
    
    candidates = [
        {"name": "Alice", "email": "alice@test.com", "status": "Assessment", "job": "J123"},
        {"name": "Bob", "email": "bob@test.com", "status": "Interview", "job": "J456"},
        {"name": "Carol", "email": "carol@test.com", "status": "Assessment", "job": "J789"},
    ]
    
    results = []
    for candidate in candidates:
        message = orchestrate(
            candidate_name=candidate["name"],
            candidate_email=candidate["email"],
            status=candidate["status"],
            job_id=candidate["job"]
        )
        results.append({
            "candidate": candidate["name"],
            "status": candidate["status"],
            "message_length": len(message)
        })
    
    print("\nBatch Processing Results:")
    for result in results:
        print(f"  ✅ {result['candidate']} ({result['status']}): {result['message_length']} chars")


# ============= EXAMPLE 4: With Claude AI =============

def example_with_claude():
    """Use Claude for AI-powered tips (requires ANTHROPIC_API_KEY)"""
    import os
    
    print("\n" + "="*70)
    print("EXAMPLE 4: AI-Powered Interview Tips")
    print("="*70)
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("\n⚠️  ANTHROPIC_API_KEY not set. Set it to see AI-powered tips:")
        print("   export ANTHROPIC_API_KEY='your-key-here'")
        return
    
    message = orchestrate(
        candidate_name="David Kim",
        candidate_email="david.k@email.com",
        status="Interview",
        job_id="J123",
        use_claude=True  # Enable AI-powered tips
    )
    
    print(f"\nAI-Generated Message:\n{message}\n")


# ============= EXAMPLE 5: Custom Integration =============

def example_integration():
    """
    Show how to integrate with other systems
    (e.g., email sender, WhatsApp API, CRM)
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Integration with Email System")
    print("="*70)
    
    # Mock email sender
    def send_email(to: str, subject: str, body: str):
        print(f"\n📧 [MOCK EMAIL SENT]")
        print(f"   To: {to}")
        print(f"   Subject: {subject}")
        print(f"   Body: {body[:100]}...")
    
    # Generate message using orchestrator
    candidate_email = "priya.sharma@email.com"
    message = orchestrate(
        candidate_name="Priya Sharma",
        candidate_email=candidate_email,
        status="Interview",
        job_id="J101"
    )
    
    # Send via email
    send_email(
        to=candidate_email,
        subject="Your Interview Preparation Tips - RecruitEM",
        body=message
    )
    
    print("\n✅ Successfully integrated with email system!")


# ============= EXAMPLE 6: Error Handling =============

def example_error_handling():
    """Show robust error handling"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Error Handling")
    print("="*70)
    
    # Valid case
    try:
        message = orchestrate(
            candidate_name="John Doe",
            candidate_email="john@test.com",
            status="Assessment",
            job_id="J123"
        )
        print("\n✅ Valid case succeeded")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    # Edge case: Unknown job ID (system handles gracefully)
    try:
        message = orchestrate(
            candidate_name="Jane Doe",
            candidate_email="jane@test.com",
            status="Interview",
            job_id="UNKNOWN_JOB"  # Not in database
        )
        print("\n✅ Edge case handled gracefully (fallback to generic data)")
    except Exception as e:
        print(f"\n❌ Error: {e}")


# ============= EXAMPLE 7: Monitoring & Analytics =============

def example_monitoring():
    """Track orchestration metrics"""
    print("\n" + "="*70)
    print("EXAMPLE 7: Monitoring & Analytics")
    print("="*70)
    
    import time
    
    metrics = {
        "total_candidates": 0,
        "assessment_messages": 0,
        "interview_messages": 0,
        "total_time": 0
    }
    
    test_cases = [
        ("Alice", "Assessment", "J123"),
        ("Bob", "Interview", "J456"),
        ("Carol", "Assessment", "J789"),
        ("David", "Interview", "J101"),
    ]
    
    for name, status, job_id in test_cases:
        start = time.time()
        
        message = orchestrate(
            candidate_name=name,
            candidate_email=f"{name.lower()}@test.com",
            status=status,
            job_id=job_id
        )
        
        elapsed = time.time() - start
        
        metrics["total_candidates"] += 1
        metrics["total_time"] += elapsed
        
        if status == "Assessment":
            metrics["assessment_messages"] += 1
        else:
            metrics["interview_messages"] += 1
    
    print("\n📊 Orchestration Metrics:")
    print(f"   • Total Candidates Processed: {metrics['total_candidates']}")
    print(f"   • Assessment Messages: {metrics['assessment_messages']}")
    print(f"   • Interview Messages: {metrics['interview_messages']}")
    print(f"   • Average Time per Message: {metrics['total_time']/metrics['total_candidates']:.3f}s")
    print(f"   • Total Time: {metrics['total_time']:.3f}s")


# ============= RUN ALL EXAMPLES =============

if __name__ == "__main__":
    print("\n🎓 " * 30)
    print("SMART RECRUITMENT DISPATCHER - EXAMPLES")
    print("🎓 " * 30)
    
    examples = [
        ("Basic Usage", example_basic),
        ("Interview Prep", example_interview),
        ("Batch Processing", example_batch),
        ("With Claude AI", example_with_claude),
        ("Email Integration", example_integration),
        ("Error Handling", example_error_handling),
        ("Monitoring", example_monitoring),
    ]
    
    print("\n📚 Available Examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"   {i}. {name}")
    
    print("\n" + "="*70)
    print("Running all examples...")
    print("="*70)
    
    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\n❌ Error in {name}: {e}")
    
    print("\n✅ " * 30)
    print("ALL EXAMPLES COMPLETED!")
    print("✅ " * 30 + "\n")

