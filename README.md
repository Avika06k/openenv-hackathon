---
title: OpenEnv Submission
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
---

# OpenEnv Hackathon Submission

This project is a minimal OpenEnv-compatible submission.

## What it does

- Runs `inference.py`
- Prints required logs:
  - START
  - STEP
  - END

## Output format

The script produces:

[START] task=code_fix env=codefix_env model=gpt-4.1-mini  
[STEP] step=1 action=fix_code reward=1.00 done=true error=null  
[END] success=true steps=1 rewards=1.00  

## Notes

- Built using Docker (Hugging Face Spaces)
- Designed to satisfy OpenEnv validation requirements
- Container kept alive for evaluation

## Update

Final rebuild trigger
