
## Q: This question is for a multi agent setup GSithub copilot , Roo code and cluade code what would it look like ?

In a multi-agent setup using GitHub Copilot, Roo Code, and Claude Code, the recommended directory structure leverages the Agent Skills open standard. This standard allows all three agents to share a unified set of specialized workflows while keeping their main context windows lean. 

Unified Multi-Agent Directory Structure
For a repository shared by multiple agents, you should store skills in a standard location that all three tools can scan. 
GitHub
GitHub
 +1
text
.agents/               <-- Universal standard for cross-agent compatibility
└── skills/
    └── your-skill-name/
        ├── SKILL.md      # Required: The "brain" with YAML metadata
        ├── scripts/      # Tool-specific executable code (Python/JS)
        ├── references/   # Deep domain context (Docs, API specs)
        └── assets/       # Examples and templates
Use code with caution.

Agent-Specific Integration 
While .agents/skills/ is the emerging universal path, each tool has specific legacy paths it prioritizes: 

GitHub Copilot: Scans .github/skills/ by default. You can point it to the shared .agents/ folder using the chat.agentSkillsLocations VS Code setting.
Claude Code: Natively supports .claude/skills/ and follows the Agent Skills standard. It treats skills as "Level 2" context that it only loads when the SKILL.md description matches your request.
Roo Code: Recognises .roo/skills/ but supports symbolic links. You can link your shared library using:
ln -s .agents/skills/ ~/.roo/skills/shared-library 

Comparison: Skills vs. Custom Instructions
To optimize performance across these agents, use a hybrid approach: 

Feature 	Custom Instructions (.github/copilot-instructions.md, etc.)	Agent Skills (SKILL.md)
Scope	Broad, global project rules (e.g., "Use TypeScript").	Task-specific (e.g., "Review SQL migrations").
Context	Loaded into every message (consumes more tokens).	Loaded progressively only when needed.
Multi-Agent	Requires duplicate files for each agent.	One SKILL.md shared by all agents via symlinks.
Best Practices for This Setup
Strict YAML Metadata: Ensure your SKILL.md has a clear name and description in the frontmatter. Agents use the description to decide whether to "activate" the skill.
Keep it Modular: Limit SKILL.md to under 500 lines. Move heavy documentation into the references/ folder so agents only read it on demand.
Use MCP for Complex Tools: If a skill requires interacting with external APIs (like Slack or Google Drive), define it as an MCP (Model Context Protocol) server. Both Claude Code and Roo Code can connect to the same MCP server to share tool execution. 


## Q: The roo code symlink will only work in a container ?

While Roo Code's symlink support has historically been limited primarily to its rules/config files, you can still achieve a unified multi-agent structure without a container by leveraging native shared path support. 

Unified Multi-Agent Setup (No Container)
The most reliable way to share skills across GitHub Copilot, Roo Code, and Claude Code is to use the emerging ~/.agents/skills/ global directory, which all three tools are designed to scan natively. 
Roo Code Docs
Roo Code Docs
text
~/.agents/skills/           <-- Global cross-agent shared folder
└── shared-skill-name/
    ├── SKILL.md            # Standard entry point (metadata + logic)
    ├── scripts/            # Executable code
    └── references/         # Deep context
Use code with caution.

How Each Agent Connects to This Path
You don't need symlinks if you use these specific integration methods for each tool:
Roo Code: Natively prioritizes ~/.agents/skills/ alongside its own ~/.roo/skills/ directory. It automatically indexes both for cross-agent compatibility.
Claude Code: Natively supports ~/.agents/skills/ as a "personal skills" location for sharing across different projects.
GitHub Copilot: While it defaults to ~/.copilot/skills/, you can point it to your shared directory using the chat.agentSkillsLocations setting in VS Code to include your global .agents path. 

Why Symlinks Often Fail Outside Containers
Outside of a containerized environment, Roo Code's internal file scanner (often using ripgrep) has historically not followed symlinks for general file operations or deep skill indexing. If you must use a shared folder that is not in ~/.agents/, use hard links on macOS/Linux or directory junctions on Windows, as these are seen by applications as physical directories rather than shortcuts. 

Alternative: Project-Level Parallelism
If you prefer project-specific skills over global ones, mirror the structure inside your repository root: 
.github/skills/: Best for GitHub Copilot.
.claude/skills/: Best for Claude Code.
.roo/skills/: Best for Roo Code. 

To avoid duplication here, use a single .agents/skills/ folder at your project root. Both Roo Code and Claude Code will automatically find it. 

## Q: what about rules or workflows  or capabilities should these all be included in skill.md ?


In a multi-agent setup, you should not cram everything into SKILL.md. Instead, follow a "Context Hygiene" strategy that separates always-on rules from on-demand workflows.
The "Context Hygiene" Hierarchy
To keep your agents fast and accurate, distribute information based on its scope:
Type 	Content Example	Best Location	Agent Support
Global Rules	"Always use Tabs," "No comments in PRs"	~/.claude/CLAUDE.md or ~/.roo/rules/	Claude Code, Roo Code
Project Rules	Tech stack (React), Linting, Repo structure	.github/copilot-instructions.md	GitHub Copilot
Capabilities	"How to debug logs," "Update SQL schema"	.agents/skills/your-skill/SKILL.md	All (via shared path)
Complex Workflows	Multi-step deployment sequences	.agents/skills/your-skill/references/	All (referenced by SKILL.md)
1. Capabilities & Workflows (Use SKILL.md)
SKILL.md should be the entry point for specific, repeatable tasks. It should define: 
The "What": A clear description in the YAML frontmatter for skill discovery.
The "How": High-level, numbered process steps (the workflow) that the agent must execute.
The "Output": Precise specifications for what the final result should look like. 


2. Rules & Constraints (Use Instructions Files)
Avoid putting "always-on" rules (e.g., "Don't use semicolons") into a skill. If a rule applies to everything the agent does, put it in a Custom Instructions file instead: 
Roo Code: Use .roo/rules/ for directory-based instructions or a .roorules file.
GitHub Copilot: Use .github/copilot-instructions.md.
Claude Code: Use CLAUDE.md. 

3. Deep Context (Use references/)
If a workflow is extremely detailed (e.g., a 20-step security audit), don't put the whole thing in SKILL.md. Keep the main file under 500 lines and move the heavy lifting into a references/ subdirectory. 

Why? Agents only read the SKILL.md description initially. They only load the full body and its references when they decide the skill is relevant, saving significant token costs. 
Summary Rule of Thumb
Rules: Put in "Instructions" (Broad, always-on).
Workflows: Put in SKILL.md (Specific, sequential).
Capabilities: Put in SKILL.md (The "skill" itself).
Knowledge/Data: Put in references/ (Deep, on-demand)

## Q: ok now i want my agent team to develop this for themselves I have tried asking but they don't have the skills or knowledge to do it where you do how can i address this?

To get your agent team (GitHub Copilot, Roo Code, and Claude Code) to develop their own skills, you need to provide them with a "Meta-Skill"—a set of instructions that teaches them how to use the Agent Skills open standard to expand their own capabilities. 
Here's how to help an agent team develop skills and workflows:
The "Meta-Skill" Strategy
Agents need a template and workflow because they can't "learn" from conversation history for long-term use. Some tools, like Gemini CLI, have a built-in skill-creator for this purpose. 

1. Create a "Skill-Creator" Skill 
Create a new folder at ~/.agents/skills/skill-creator/ and add a SKILL.md file with these instructions: 
markdown
---
name: skill-creator
description: Use this skill to design, structure, and write new AI agent skills following the open standard.
---
# Skill Creator Workflow
When the user asks to create a new skill or "learn" a new capability:
1. **Analyze**: Identify the specific repeatable task, the required scripts (Python/Bash), and the reference docs needed.
2. **Structure**: Create a new directory in `.agents/skills/` with:
   - `SKILL.md`: The core instructions with YAML frontmatter.
   - `scripts/`: For any executable code.
   - `references/`: For deep documentation.
3. **Draft**: Write the `SKILL.md` file. Keep the body under 500 lines and use progressive disclosure for details.
4. **Refine**: Ask the user to test the skill and provide feedback to iterate on the instructions.
Use code with caution.

2. Implement a Self-Improvement Loop 
Instruct agents to follow a Plan-Validate-Execute loop: 

Extract from Action: After an agent successfully completes a complex task, prompt it: "That worked well. Use your skill-creator skill to extract that process into a permanent skill so you can do it perfectly next time". 

Validation Scripts: Encourage agents to write small Python validation scripts in the scripts/ folder of their new skills. These scripts should check their own output for errors, allowing them to self-correct. 

Memory via Logs: Have agents save "success logs" in the assets/ folder of a skill. This provides future agents with few-shot examples of what a "good" result looks like. 

3. Bridge the Knowledge Gap
Provide agents with specific Reference Artifacts if they don't know how to build certain technical parts: 

Runbooks & Docs: Feed existing internal docs or API specs into the agent and ask it to synthesize a skill from them.
GitHub Copilot Skills: Point Copilot to the Official GitHub Skill Docs so it understands its own specific integration requirements. 

Summary of the Workflow
Define the Meta-Skill: Give them the skill-creator template above.
Trigger on Success: Tell them to turn every successful complex workflow into a skill.
Use Progressive Disclosure: Ensure they keep SKILL.md lean so it doesn't bloat their context window

## Q: What is gemeni's creator skill can you display it here ?

The skill-creator is a built-in meta-skill within the Gemini CLI. It automates the development of new agent capabilities. It translates a high-level user request into a standardized, multi-file directory structure that other agents can understand. 

The Built-in skill-creator Definition
When this meta-skill is activated, the Gemini CLI follows a set of internal instructions: 

markdown
---
name: skill-creator
description: Use this skill to rapidly generate or refactor complete Agent Skills from a user request.
---
# Skill Creator Workflow
1. **Directory Generation**: Create a unique directory at `~/.gemini/skills/<skill-name>`.
2. **SKILL.md Creation**: Write a file containing:
   - **YAML Frontmatter**: `name` and a concise `description` (used for agent discovery).
   - **Procedural Guidance**: Step-by-step instructions for the agent to follow when the skill is active.
3. **Resource Bundling**: Initialize standard subdirectories:
   - `scripts/`: Stubs for Python/JS tool logic.
   - `references/`: Placeholders for static documentation or API specs.
   - `assets/`: Templates or few-shot examples.
4. **Validation**: Verify the skill meets the "Progressive Disclosure" standard (keeping the main file lean).
Use code with caution.

How it Works in Practice
Discovery & Activation: The agent scans available skill names and descriptions. If a request matches the skill-creator description, the agent calls the activate_skill tool to load these instructions into its context. 

Zero-to-Skill: The skill-creator will build the boilerplate, draft the scripts, and document the workflow automatically. 

Refinement: It can also refactor existing skills. If a current skill is failing or too bloated, the skill-creator can "de-slop" it or move heavy text into the references/ folder to save tokens. 

Commands to Manage Skills
In the Gemini CLI, these slash commands can be used to interact with the skills created by this tool: 

/skills list: Shows all discovered skills.
/skills reload: Refreshes the list if a file has been manually edited.
/skills link <path>: Links a shared directory via symlink


## Q: is this enough info for an agent to create skills or does it need more depth what would you suggest ?

# Skill Draft: `skills_creator`

## Purpose
Create consistent, modular agent skills using a repeatable structure that keeps primary context small and loads deep references only when needed.

## Primary Agents
- Roo
- Copilot
- Claude Code

## When to Invoke
- When a new skill is requested from plain-language requirements
- When converting ad-hoc instructions into reusable skill assets
- When standardising legacy skills to the shared format

## Inputs
- Skill intent and expected outcomes
- Target location policy for the repository
- Existing project conventions and guardrails

## Outputs
- A drafted skill package plan with required files
- `SKILL.md` frontmatter and concise operating instructions
- Optional `scripts/`, `references/`, and `assets/` recommendations
- Validation checklist for structure and quality

## Procedure
1. Confirm the target location and runtime integration path for the skill.
2. Define a verb-ing plus noun skill name and align folder name with metadata name.
3. Draft the `SKILL.md` metadata with clear activation description.
4. Keep `SKILL.md` focused on high-value instructions and move depth into `references/`.
5. Add `scripts/` only for repeatable deterministic tasks.
6. Add `assets/` for templates, examples, and stable output patterns.
7. Validate file structure and ensure the draft remains concise and discoverable.

## Recommended Structure
```text
<skill-name>/
├── SKILL.md
├── scripts/
├── references/
└── assets/
```

## `SKILL.md` Minimum Frontmatter Template
```yaml
---
name: skills_creator
description: Creates or refactors agent skills using a standard modular structure with concise activation guidance and optional supporting resources.
---
```

## Drafting Rules
- Keep the core `SKILL.md` body short and task-focused.
- Use progressive disclosure so deep material lives in `references/`.
- Prefer deterministic scripts for complex multi-step operations.
- Ensure naming consistency across folder, metadata, and references.

## Validation Checklist
1. Folder name matches the skill metadata name.
2. Description is specific enough for reliable activation.
3. `SKILL.md` is concise and avoids deep reference dumping.
4. Optional folders are included only when needed.
5. References are scoped to the skill objective.

## Source Basis
- [`docs/`skills_creation.md`](docs/`skills_creation.md)
- [`docs/skills/README.md`](docs/skills/README.md)


This is a solid "V1" draft. It gives them the What and the Where, but to make the agents truly autonomous and consistent across Roo, Copilot, and Claude Code, it needs more "How"—specifically regarding the technical handoffs between them.
Here is what I would add to move this from a "template" to a "functional engine":
1. Add "Discovery Logic"
Agents often struggle to know which description will actually trigger them. Suggest adding a section on Activation Phrases.
Suggestion: Add a "Metadata Guidance" section. Tell the agent: "The description must start with a verb and define the specific trigger. Example: 'Use this skill when the user asks to [X] or needs to [Y].'"
2. Define the "Cross-Agent Handshake"
Since you are using three different agents, the skill needs to know how to talk to each.
Suggestion: Add a rule for Environment Detection.
If Roo: Use .roo/rules for local constraints.
If Claude: Use CLAUDE.md for project memory.
If Copilot: Use .github/copilot-instructions.md.
The skills_creator should be instructed to update these "entry point" files whenever a new skill is created so the other agents "see" it immediately.
3. Provide a "Concrete Example" (Few-Shot Prompting)
Agents learn best by example. Include a "Reference Skill" inside your assets/ folder for the skills_creator to copy.
Suggestion: Create a dummy skill called deploy-node-app in the assets/ directory. When the agent builds a new skill, it should look at that example to see the exact tone and formatting you expect.
4. Technical Depth: Scripting Standards
If the agent is creating a scripts/ folder, what language should it use?
Suggestion: Add a Scripting Policy. "Default to Python for data/logic and Bash for filesystem operations. Ensure all scripts include a --help flag and basic error handling so other agents can figure out how to run them."
5. Updated "Procedure" Snippet
I’d suggest adding these two steps to your Procedure section:
Register Skill: Update the project’s main README.md or .agents/INDEX.md with the new skill's name and purpose.
Self-Test: The agent must simulate a call to the new skill to verify the instructions are unambiguous.
Summary: Is it enough?
Almost. If you give an agent this draft today, it will produce the folders and the files correctly. However, without the Activation Phrases and Cross-Agent Handshake, the agents might create skills they then forget to use.
My advice: Add a examples/ or assets/ folder to this skill containing one "Perfectly Formatted Skill" to serve as a gold standard.




## Q: Do you have an example skill that  the agents can use as a blueprint? 

This is a "Gold Standard" blueprint for a Log Analysis skill. It is designed to be copied by your Skill-Creator meta-skill.
It demonstrates Progressive Disclosure: the SKILL.md is the high-level manager, the scripts/ do the heavy lifting, and references/ hold the "boring" technical specs that would otherwise bloat an agent's context window.
1. The Directory Structure
text
analyze-logs/
├── SKILL.md
├── scripts/
│   └── parser.py        # Logic: Regex patterns, filtering, and JSON export
├── references/
│   └── error-codes.md   # Deep Context: 50+ pages of vendor error codes
└── assets/
    └── report-template.md # Template: How the final summary should look
Use code with caution.

2. The SKILL.md (The "Brain")
This is the entry point. Notice the specific YAML description designed to trigger Roo, Copilot, or Claude.
markdown
---
name: analyze-logs
description: Use this skill when the user asks to debug system errors, parse large log files, or generate error frequency reports.
---

# Log Analysis Workflow

## Prerequisites
- Target log file must be in `.log` or `.txt` format.
- Python 3.10+ must be available to run the parser.

## Procedure
1. **Locate Logs**: Identify the log file path provided by the user.
2. **Execute Parser**: Run `python3 scripts/parser.py --file <path>`. 
   - *Note: Do not read the raw file if it is >1MB; use the script output instead.*
3. **Cross-Reference**: If the script identifies specific error codes (e.g., `ERR_702`), look up the root cause in `references/error-codes.md`.
4. **Format Output**: Use the structure in `assets/report-template.md` to present findings.

## Constraints
- Never output more than 20 raw log lines in the chat.
- Always group errors by "Frequency" and "Severity."
Use code with caution.

3. The scripts/parser.py (The "Heavy Lifting")
Instead of the agent "hallucinating" a regex, it uses a deterministic tool.
python
import argparse
import json
import re

# Logic to extract timestamps, levels (INFO/WARN/ERROR), and messages.
# This keeps the agent from having to 'read' 10,000 lines manually.
def parse_logs(file_path):
    patterns = {"error": r"ERROR: (.*)", "warn": r"WARN: (.*)"}
    # ... extraction logic ...
    return json.dumps(results)

if __name__ == "__main__":
    # Standard --help and argument handling so any Agent can use it.
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    args = parser.parse_args()
    print(parse_logs(args.file))
Use code with caution.

4. The references/error-codes.md (The "Deep Context")
This file stays closed unless the agent specifically needs to look up a code. This saves thousands of tokens per message.
markdown
# Vendor Error Reference

| Code | Meaning | Resolution |
| :--- | :--- | :--- |
| ERR_101 | Connection Timeout | Check Load Balancer timeout settings. |
| ERR_702 | Memory Leak | Inspect the `garbage-collector` logs. |
| ... | ... | ... |
Use code with caution.

Why this works for your team:
For Roo Code: It sees the scripts/ and knows it has the execute_command capability to run the Python tool.
For Claude Code: It reads the SKILL.md frontmatter and "activates" the skill only when logs are mentioned.
For GitHub Copilot: The references/ folder provides the RAG (Retrieval-Augmented Generation) source it needs to answer "What does this error mean?" without guessing.


## Q: where do i put this example?

To ensure all three agents (Roo, GitHub Copilot, and Claude Code) can access the blueprint, place it in a standardized shared directory within your repository or user profile. 

1. Recommended Shared Locations
The best practice is to use one of the following paths, as these are the primary "discovery zones" for modern AI agents:
Project-Level (Per Repository):
Place the folder at .agents/skills/analyze-logs/. 

Why: This is the tool-agnostic standard that avoids tool-specific lock-in while remaining visible to any agent scanning the repo.
User-Level (Shared Across Projects):
Place the folder at ~/.agents/skills/analyze-logs/. 

Why: This makes the skill globally available to your agents regardless of which project you are currently working in.
2. Setup for Each Agent
If you choose the .agents/skills/ path, you may need to point specific tools to it:
GitHub Copilot: Ensure the experimental Use Claude Skills setting is enabled in VS Code. It will automatically look for skills in .github/skills/, .claude/skills/, and .agents/skills/.
Claude Code: It natively scans .claude/skills/ and ~/.claude/skills/. It also recognizes the .agents/ standard in newer versions.
Roo Code: Place it in .roo/skills/ or use the common .agents/skills/ path. Roo is highly flexible and typically indexes any skills found in the project root's hidden configuration folders. 

3. Implementation Steps
Create the Folder:
mkdir -p .agents/skills/analyze-logs/{scripts,references,assets}
Add the SKILL.md:
Save your "Brain" instructions as .agents/skills/analyze-logs/SKILL.md.
Deploy Resources:
Place your Python parser in scripts/, documentation in references/, and templates in assets/.
Verify Discovery:
In your agent's chat, type /skills list or ask "What skills do you have access to?" to confirm it has been indexed. 








