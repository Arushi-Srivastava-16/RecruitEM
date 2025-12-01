#!/usr/bin/env python3
"""
Quick demonstration script for RecruitEM Orchestrator
Run this to show the system in action
"""

from orchestrator import orchestrate

print("\n" + "="*70)
print("RECRUITEM ORCHESTRATOR - DEMONSTRATION")
print("="*70 + "\n")

print("Demonstrating Multi-Agent Orchestration System\n")

# Demo 1: Assessment workflow
print("[1] ASSESSMENT WORKFLOW")
print("-" * 70)
assessment_msg = orchestrate(
    candidate_name="Arushi Srivastava",
    candidate_email="aru@bits.com",
    status="Assessment",
    job_id="F0188"
)
print("\nGenerated Assessment Message:")
print("-" * 70)
print(assessment_msg)
print("-" * 70 + "\n")

# Demo 2: Interview workflow
print("\n[2] INTERVIEW WORKFLOW")
print("-" * 70)
interview_msg = orchestrate(
    candidate_name="Nik Sharma",
    candidate_email="nik@bits.com",
    status="Interview",
    job_id="F0337"
)
print("\nGenerated Interview Message:")
print("-" * 70)
print(interview_msg)
print("-" * 70 + "\n")

print("="*70)
print("DEMONSTRATION COMPLETE")
print("="*70)
print("\nKey Features Demonstrated:")
print("  [*] Router agent routing decisions")
print("  [*] Assessment agent with test links")
print("  [*] Interview agent with prep tips")
print("  [*] Tool integration (get_test_link, rag_search)")
print("  [*] Dynamic message generation\n")

