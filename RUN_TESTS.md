# How to Run README Tests

## Quick Start

Run all tests with verbose output:
```bash
python3 -m pytest test_readme.py -v
```

## Alternative Methods

### Using unittest directly
```bash
python3 test_readme.py
```

### Using pytest (if installed globally)
```bash
pytest test_readme.py -v
```

## Run Specific Test Classes

### Run only core functionality tests
```bash
python3 -m pytest test_readme.py::TestREADME -v
```

### Run only negative/security tests
```bash
python3 -m pytest test_readme.py::TestREADMENegativeCases -v
```

### Run only boundary/edge case tests
```bash
python3 -m pytest test_readme.py::TestREADMEBoundaryCases -v
```

## Run Individual Tests

```bash
# Test that README exists
python3 -m pytest test_readme.py::TestREADME::test_readme_exists -v

# Test purpose section content
python3 -m pytest test_readme.py::TestREADME::test_purpose_section_not_empty -v

# Test for security issues
python3 -m pytest test_readme.py::TestREADMENegativeCases::test_no_sensitive_information -v
```

## Test Output Options

### Show detailed failure information
```bash
python3 -m pytest test_readme.py -v --tb=long
```

### Show only summary
```bash
python3 -m pytest test_readme.py -v --tb=no
```

### Show test collection without running
```bash
python3 -m pytest test_readme.py --collect-only
```

### Run with coverage (if pytest-cov installed)
```bash
python3 -m pytest test_readme.py --cov=. --cov-report=html
```

## Expected Output

All 34 tests should pass:
- 22 tests in TestREADME (core functionality)
- 7 tests in TestREADMENegativeCases (security/negative cases)
- 5 tests in TestREADMEBoundaryCases (boundary/edge cases)

## Test Categories

| Category | Test Count | Purpose |
|----------|------------|---------|
| Structure Validation | 8 | Verify document structure |
| Content Validation | 9 | Check content completeness |
| Quality Assurance | 5 | Ensure quality standards |
| Security/Negative | 7 | Test for security issues |
| Boundary/Edge Cases | 5 | Test edge conditions |

## CI/CD Integration

### GitHub Actions Example
```yaml
- name: Run README Tests
  run: python3 -m pytest test_readme.py -v
```

### GitLab CI Example
```yaml
test_readme:
  script:
    - python3 -m pytest test_readme.py -v
```

## Troubleshooting

### ModuleNotFoundError: No module named 'pytest'
Install pytest:
```bash
pip install pytest
```

Or use unittest directly:
```bash
python3 test_readme.py
```

### Tests failing due to README changes
Review the test output to understand which validation failed, then either:
1. Fix the README.md to meet the requirement
2. Update the test if the requirement has legitimately changed

## Test Maintenance

When updating README.md:
1. Run tests before committing: `python3 -m pytest test_readme.py -v`
2. If tests fail, check if README needs fixing or tests need updating
3. Always ensure all tests pass before pushing changes

## Additional Resources

- See `TEST_SUMMARY.md` for detailed test documentation
- See `pytest.ini` for pytest configuration
- See `test_readme.py` for test implementation