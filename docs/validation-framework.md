# Validation Framework

Reusable validation patterns for skills. Load this when you need to validate inputs, configs, or outputs.

## Validation Types

### 1. File Structure Validation

Check that a file has required sections/headings.

```
Validate structure:
- config.yaml: must have `name`, `version`, `description`
- package.json: must have `name`, `scripts`
- SKILL.md: must have frontmatter with `name`, `description`
```

**Pattern:**
```
If file exists but structure is invalid → flag WARNING, proceed with what's usable.
If file doesn't exist → STOP, report missing file.
```

### 2. Field Validation

Check that required fields exist and have valid values.

```
Validate fields:
- email: must match RFC pattern
- version: must be semver (X.Y.Z)
- model_tier: must be one of: high, medium, fast
```

**Pattern:**
```
For each required field:
  If missing → ERROR
  If invalid format → WARNING, use default if available
```

### 3. Dependency Validation

Check that required tools/files exist before starting.

```
Validate prerequisites:
- Python 3.10+ installed
- requirements.txt exists
- .env file has API_KEY
```

**Pattern:**
```
For each dependency:
  If missing → STOP, report what's needed
  If wrong version → WARNING, proceed with caution
```

### 4. Output Validation

Check that output files have the right structure after processing.

```
Validate output:
- report.md: must have at least 3 sections
- output.json: must be valid JSON
- test_results: must have 0 failures
```

**Pattern:**
```
After generating output:
  If invalid → ROLLBACK, report what went wrong
  If partial → WARNING, note what's missing
```

## Validation Template

Add this to any skill that needs validation:

```markdown
## Validation

### Input Validation
- [ ] Required files exist
- [ ] Files have correct structure
- [ ] Fields have valid values

### Output Validation
- [ ] Output files created
- [ ] Output has correct structure
- [ ] No errors in output

### Error Handling
- If validation fails → STOP and report
- If partial → proceed with WARNING
- If critical → ROLLBACK changes
```

## Examples by Skill Type

### Data Processing Skills
```markdown
## Validation
- Input CSV: must have headers
- Input JSON: must be valid JSON
- Output: must match schema
```

### API Integration Skills
```markdown
## Validation
- API key exists in .env
- Endpoint is reachable
- Response has expected fields
```

### Code Generation Skills
```markdown
## Validation
- Generated code compiles
- Tests pass
- No lint errors
```

### File Transformation Skills
```markdown
## Validation
- Input file exists and is readable
- Output file created
- Output preserves required fields
```
