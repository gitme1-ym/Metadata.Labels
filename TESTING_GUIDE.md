# Testing Guide for README.md

## Quick Start

Run all tests:
```bash
python3 test_readme.py
```

Run with detailed output:
```bash
python3 test_readme.py -v
```

## Test Structure

The test suite is organized into 7 categories:

1. **TestReadmeExists** - File accessibility tests
2. **TestReadmeContent** - Content structure and completeness
3. **TestReadmeMarkdownStructure** - Markdown formatting validation
4. **TestReadmeEncoding** - File encoding and character handling
5. **TestReadmeBusinessLogic** - Business requirements validation
6. **TestReadmeEdgeCases** - Edge cases and quality checks
7. **TestReadmeRegression** - Regression prevention tests

## Running Specific Tests

Run a specific test class:
```bash
python3 test_readme.py TestReadmeContent
```

Run a single test:
```bash
python3 test_readme.py TestReadmeContent.test_mentions_tier_service
```

## What Gets Tested

### Critical Requirements ✓
- File existence and readability
- All required sections present (Purpose, PR Description, Legal)
- Content is non-empty and meaningful
- Mentions key features (tier service, resolvers, tests)

### Quality Standards ✓
- Proper Markdown syntax
- Consistent formatting
- UTF-8 encoding
- Unix line endings
- No placeholder text

### Regression Prevention ✓
- Balanced markdown formatting
- Consistent bullet points
- Proper link format
- No broken formatting

## Expected Output

```
----------------------------------------------------------------------
Ran 37 tests in 0.004s

OK
```

## Adding New Tests

To add a new test, create a method in the appropriate test class:

```python
def test_your_new_requirement(self):
    """Test that verifies your new requirement."""
    # Your test logic here
    self.assertTrue(condition, "Error message if test fails")
```

## Test Categories Explained

### File Existence (TestReadmeExists)
Validates that README.md exists and is accessible.

### Content (TestReadmeContent)
Ensures all required sections are present and contain meaningful content.

### Markdown Structure (TestReadmeMarkdownStructure)
Verifies proper Markdown syntax and formatting conventions.

### Encoding (TestReadmeEncoding)
Checks file encoding and character handling.

### Business Logic (TestReadmeBusinessLogic)
Validates that content matches business requirements and context.

### Edge Cases (TestReadmeEdgeCases)
Tests for common quality issues and edge cases.

### Regression (TestReadmeRegression)
Prevents reintroduction of previously fixed issues.

## Troubleshooting

If tests fail:

1. **Read the error message** - It will tell you which assertion failed
2. **Check the line number** - The error includes the file location
3. **Review the test docstring** - Explains what the test validates
4. **Examine README.md** - Compare against test expectations

## Test Philosophy

These tests follow best practices:
- **Clear naming** - Test names describe what is being tested
- **Single responsibility** - Each test validates one thing
- **Comprehensive coverage** - Tests cover happy paths, edge cases, and regressions
- **Maintainable** - Easy to understand and extend
- **Fast execution** - All tests run in under 1 second

## Coverage Summary

✓ 37 tests covering:
- File accessibility (4 tests)
- Content structure (11 tests)
- Markdown formatting (6 tests)
- Encoding (3 tests)
- Business requirements (5 tests)
- Edge cases (5 tests)
- Regression prevention (4 tests)