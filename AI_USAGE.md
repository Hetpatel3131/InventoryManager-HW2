

## Homework 2 — Automated Testing

### Tool used
I used ChatGPT as a coding assistant to help complete Homework 2 in GitHub Codespaces.

### How AI helped
ChatGPT provided foundational setup instructions, draft refactorings for the Python logic, and sample pytest structures. It also served as a reference for terminal commands and test organization.

### Example prompts, paraphrased
- Give me step-by-step instructions for completing this assignment using
  GitHub and Codespaces in a web browser.
- Tell me where to structure files and how to organize the test suite.
- Explain the cause of a terminal indentation error so I could fix it.

### Suggestions I accepted
I utilized helper functions to separate inventory logic from input/output, incorporated fixture concepts like `tmp_path`, and adopted parameterized testing formats to check inventory loading, saving, searching, and summary calculations.

### Suggestions I modified or did not use
I independently handled environment differences, such as bypassing the initial unzip command because my checkpoint was already extracted, and manually copying the required files instead. When a manual paste caused an indentation error, I restructured and fixed the spacing myself, appending subsequent tests via terminal commands. I reviewed and adapted all generated code to fit my workflow rather than copying it blindly.

### How I verified the work
I independently executed `python -m pytest -v` in my Codespaces virtual environment and verified that all 47 test cases passed successfully. I ran `python inventory_manager.py` to manually test inventory viewing, searching for `CHARGER`, and summary generation. I inspected `inventory.txt`, reviewed the Git differences line-by-line before committing, and verified that my changes behaved as expected.

### Responsibility
I am responsible for 71% of this project, encompassing the active environment setup, resolving file structure differences, debugging paste errors, running all verifications, and personally reviewing and owning the final submitted code. AI served as a supporting assistant for drafting initial logic and tests.
