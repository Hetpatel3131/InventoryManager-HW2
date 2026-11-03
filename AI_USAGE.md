# AI Usage — Homework 2

## Tool used
I used ChatGPT to help me work through Homework 2 in GitHub Codespaces.

## How AI helped
I used ChatGPT to get step-by-step setup and Git instructions, plus drafts for the refactored Inventory Manager code and the pytest test suite. Whenever I got stuck, I asked it for troubleshooting tips—like figuring out why my ZIP file wasn't extracting and how to fix an indentation error in my test file. I pasted the code into my project and ran the commands in Codespaces.

## Example prompts, paraphrased
- How do I set this up using GitHub and Codespaces step by step?
- Where do I need to create these files and paste the code?
- Why am I getting this IndentationError when I run pytest, and how do I fix it?

## Suggestions I accepted
I went with the suggestion to use helper functions to keep the inventory logic separate from keyboard input and printed output. I also used the sample inventory fixture, parameterized tests with clear IDs, and `tmp_path` for testing file operations. The test suite covers loading, saving, searching, deleting items, updating quantities, checking new-item validation, and running inventory summaries.

## Suggestions I modified or did not use
The initial unzip command didn't work because my checkpoint was already an extracted folder, so with some guidance from AI, I just copied the files I needed manually. When I messed up a manual paste and caused an indentation error, I swapped out the test file for a cleanly spaced version and added the rest of the tests using terminal commands. I didn't end up throwing out any specific test cases.

## How I verified the work
I ran `python -m pytest -v` in my Codespaces terminal and made sure all 47 test cases passed. Then I ran `python inventory_manager.py` to test viewing the inventory, searching for `CHARGER`, checking the summary, and exiting. I compared the outputs against the sample inventory, made sure `inventory.txt` didn't change unexpectedly, and checked my Git diffs before committing everything.

## Responsibility
Even though AI helped me write the code, tests, and troubleshoot some errors, I’m the one who ran everything, verified it works, and made sure I actually understand what the code is doing.
