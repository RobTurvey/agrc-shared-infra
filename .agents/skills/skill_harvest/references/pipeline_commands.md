# skill_harvest pipeline commands

Run from repo root.

## 1) Fetch

```bash
python3 .agents/skill_harvest/scripts/fetch_external_skill.py \
  --url <source-url> \
  --fetch-linked \
  --issue <beads-issue-id>
```

## 2) Analyze

```bash
python3 .agents/skill_harvest/scripts/analyze_harvested_skill.py \
  --candidate-id <candidate-id>
```

## 3) QA

```bash
python3 .agents/skill_harvest/scripts/qa_validate_harvested_skill.py \
  --candidate-id <candidate-id>
```

## 4) Approval package + decision

```bash
python3 .agents/skill_harvest/scripts/build_approval_package.py \
  --candidate-id <candidate-id>

python3 .agents/skill_harvest/scripts/record_approval_decision.py \
  --candidate-id <candidate-id> \
  --decision approve \
  --rationale "<why approved>"
```

## 5) Register + publish

```bash
python3 .agents/skill_harvest/scripts/register_approved_skill.py \
  --candidate-id <candidate-id>

python3 .agents/skill_harvest/scripts/publish_live_skill.py \
  --skill-id <skill-id> \
  --force \
  --issue <beads-issue-id>
```

## 6) Policy check

```bash
python3 .agents/skill_harvest/scripts/check_governance_policy.py
```
