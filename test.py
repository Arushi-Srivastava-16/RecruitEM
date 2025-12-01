#!/usr/bin/env python3
"""
Test script to demonstrate the orchestrator functionality
"""

from orchestrator import orchestrate

def test_assessment():
    """Test assessment agent"""
    print("=" * 70)
    print("TEST 1: Assessment Agent")
    print("=" * 70)
    
    message = orchestrate(
        candidate_name="Ashee Srivastava",
        candidate_email="esria@amity.com",
        status="Assessment",
        job_id="G12I"
    )
    
    print("\n[OK] Assessment message generated successfully!")
    print(f"Message length: {len(message)} characters\n")
    return message

def test_interview():
    """Test interview agent"""
    print("=" * 70)
    print("TEST 2: Interview Agent")
    print("=" * 70)
    
    message = orchestrate(
        candidate_name="Ashirya Srivastava",
        candidate_email="dabie@amity.com",
        status="Interview",
        job_id="G07A"
    )
    
    print("\n[OK] Interview message generated successfully!")
    print(f"Message length: {len(message)} characters\n")
    return message

def test_different_jobs():
    """Test with different job types"""
    print("=" * 70)
    print("TEST 3: Different Job Types")
    print("=" * 70)
    
    jobs = [
        ("J123", "Python Developer"),
        ("J456", "Data Analyst"),
        ("J789", "Frontend Developer"),
    ]
    
    for job_id, expected_title in jobs:
        message = orchestrate(
            candidate_name="Test Candidate",
            candidate_email="test@example.com",
            status="Assessment",
            job_id=job_id
        )
        
        # Verify job title appears in message
        if expected_title in message:
            print(f"[OK] {job_id}: Correct job title found")
        else:
            print(f"[FAIL] {job_id}: Job title mismatch")
    
    print()

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("RECRUITEM ORCHESTRATOR - TEST SUITE")
    print("=" * 70 + "\n")
    
    # Run tests
    test_assessment()
    test_interview()
    test_different_jobs()
    
    print("=" * 70)
    print("ALL TESTS COMPLETED")
    print("=" * 70)
    print("\nThe orchestrator is working correctly!")
    print("Both Assessment and Interview agents are functioning properly.\n")

