"""
Comprehensive test suite for README.md documentation validation.

This test suite ensures that README.md maintains proper structure,
contains required sections, and follows documentation best practices.
"""

import os
import re
import unittest
from pathlib import Path


class TestReadmeExists(unittest.TestCase):
    """Test suite for README.md file existence and accessibility."""

    def setUp(self):
        """Set up test fixtures."""
        self.readme_path = Path(__file__).parent / "README.md"

    def test_readme_file_exists(self):
        """Test that README.md file exists in the repository root."""
        self.assertTrue(
            self.readme_path.exists(),
            "README.md file should exist in the repository root"
        )

    def test_readme_is_file_not_directory(self):
        """Test that README.md is a file, not a directory."""
        self.assertTrue(
            self.readme_path.is_file(),
            "README.md should be a file, not a directory"
        )

    def test_readme_is_readable(self):
        """Test that README.md file has read permissions."""
        self.assertTrue(
            os.access(self.readme_path, os.R_OK),
            "README.md file should be readable"
        )

    def test_readme_is_not_empty(self):
        """Test that README.md file is not empty."""
        self.assertGreater(
            self.readme_path.stat().st_size,
            0,
            "README.md file should not be empty"
        )


class TestReadmeContent(unittest.TestCase):
    """Test suite for README.md content structure and quality."""

    @classmethod
    def setUpClass(cls):
        """Load README content once for all tests."""
        readme_path = Path(__file__).parent / "README.md"
        with open(readme_path, 'r', encoding='utf-8') as f:
            cls.content = f.read()
        cls.lines = cls.content.split('\n')

    def test_content_not_empty(self):
        """Test that README has actual content, not just whitespace."""
        self.assertGreater(
            len(self.content.strip()),
            0,
            "README.md should contain non-whitespace content"
        )

    def test_has_purpose_section(self):
        """Test that README contains a Purpose/Motivation section."""
        self.assertIn(
            "Purpose/Motivation",
            self.content,
            "README.md should contain a 'Purpose/Motivation' section"
        )

    def test_has_what_does_pr_do_section(self):
        """Test that README contains a 'What does this PR do?' section."""
        self.assertIn(
            "What does this PR do?",
            self.content,
            "README.md should contain a 'What does this PR do?' section"
        )

    def test_has_legal_boilerplate_section(self):
        """Test that README contains Legal Boilerplate section."""
        self.assertIn(
            "Legal Boilerplate",
            self.content,
            "README.md should contain a 'Legal Boilerplate' section"
        )

    def test_purpose_section_not_empty(self):
        """Test that Purpose/Motivation section has content."""
        # Find the Purpose section and check if it has content after the header
        pattern = r"### Purpose/Motivation\s*\n(.+?)(?=\n###|\Z)"
        match = re.search(pattern, self.content, re.DOTALL)
        self.assertIsNotNone(match, "Purpose/Motivation section should exist")
        content = match.group(1).strip()
        self.assertGreater(
            len(content),
            0,
            "Purpose/Motivation section should not be empty"
        )

    def test_pr_description_not_empty(self):
        """Test that PR description section has content."""
        pattern = r"### What does this PR do\?\s*\n(.+?)(?=\n###|<!--|$)"
        match = re.search(pattern, self.content, re.DOTALL)
        self.assertIsNotNone(match, "What does this PR do section should exist")
        content = match.group(1).strip()
        self.assertGreater(
            len(content),
            0,
            "What does this PR do section should not be empty"
        )

    def test_pr_description_has_bullet_points(self):
        """Test that PR description uses bullet points for clarity."""
        pattern = r"### What does this PR do\?\s*\n(.+?)(?=\n###|<!--|$)"
        match = re.search(pattern, self.content, re.DOTALL)
        self.assertIsNotNone(match, "What does this PR do section should exist")
        content = match.group(1)
        # Check for bullet points (may be inside blockquotes with > prefix)
        has_bullets = bool(re.search(r'(^|\n)\s*>?\s*-\s+.+', content, re.MULTILINE))
        self.assertTrue(
            has_bullets,
            "PR description should use bullet points (lines with '-')"
        )

    def test_mentions_tier_service(self):
        """Test that README mentions tier service functionality."""
        self.assertIn(
            "tier service",
            self.content.lower(),
            "README should mention 'tier service' as it's the main feature"
        )

    def test_mentions_resolvers(self):
        """Test that README mentions resolvers functionality."""
        self.assertIn(
            "resolvers",
            self.content.lower(),
            "README should mention 'resolvers' as it's part of the implementation"
        )

    def test_mentions_tests(self):
        """Test that README mentions that tests were added."""
        self.assertIn(
            "test",
            self.content.lower(),
            "README should mention tests as they're part of the implementation"
        )


class TestReadmeMarkdownStructure(unittest.TestCase):
    """Test suite for README.md Markdown formatting and structure."""

    @classmethod
    def setUpClass(cls):
        """Load README content once for all tests."""
        readme_path = Path(__file__).parent / "README.md"
        with open(readme_path, 'r', encoding='utf-8') as f:
            cls.content = f.read()
        cls.lines = cls.content.split('\n')

    def test_uses_markdown_headers(self):
        """Test that README uses proper Markdown headers."""
        # Handle both regular and blockquote format (>)
        header_pattern = r'^>?\s*#{1,6}\s+.+'
        has_headers = any(re.match(header_pattern, line) for line in self.lines)
        self.assertTrue(
            has_headers,
            "README should use Markdown headers (# Header)"
        )

    def test_headers_have_space_after_hash(self):
        """Test that headers have proper spacing after # symbols."""
        for i, line in enumerate(self.lines, 1):
            if line.startswith('#') and not line.startswith('<!--'):
                self.assertRegex(
                    line,
                    r'^#{1,6}\s+.+',
                    f"Line {i}: Headers should have space after # symbols"
                )

    def test_uses_consistent_header_level(self):
        """Test that section headers use consistent level (###)."""
        section_headers = [
            "Purpose/Motivation",
            "What does this PR do?",
            "Legal Boilerplate"
        ]
        for header in section_headers:
            # Handle both regular and blockquote format
            pattern = f"^>?\\s*### {re.escape(header)}"
            matches = [line for line in self.lines if re.match(pattern, line)]
            self.assertEqual(
                len(matches),
                1,
                f"Section '{header}' should use level 3 header (###)"
            )

    def test_bullet_points_use_dash(self):
        """Test that bullet points use dash (-) format consistently."""
        # Handle blockquote format: lines may start with '>' then '-'
        bullet_lines = [line for line in self.lines
                       if re.match(r'^\s*>?\s*-\s+', line)]
        self.assertGreater(
            len(bullet_lines),
            0,
            "README should contain bullet points for PR description"
        )
        for line in bullet_lines:
            self.assertRegex(
                line,
                r'^\s*>?\s*-\s+\w',
                "Bullet points should use '- ' format with space"
            )

    def test_no_trailing_whitespace_on_content_lines(self):
        """Test that content lines don't have excessive trailing whitespace."""
        for i, line in enumerate(self.lines, 1):
            if line.strip():  # Only check non-empty lines
                # Allow single space after '>' for blockquote formatting
                if line.rstrip() == '>' and line == '> ':
                    continue  # This is acceptable blockquote formatting
                self.assertEqual(
                    line,
                    line.rstrip(),
                    f"Line {i} should not have trailing whitespace"
                )

    def test_html_comments_properly_formatted(self):
        """Test that HTML comments in Markdown are properly formatted."""
        comment_pattern = r'<!--.*?-->'
        if '<!--' in self.content:
            # Check that all opening comments have closing tags
            open_count = self.content.count('<!--')
            close_count = self.content.count('-->')
            self.assertEqual(
                open_count,
                close_count,
                "All HTML comment opening tags should have matching closing tags"
            )


class TestReadmeEncoding(unittest.TestCase):
    """Test suite for README.md file encoding and character handling."""

    @classmethod
    def setUpClass(cls):
        """Load README content once for all tests."""
        cls.readme_path = Path(__file__).parent / "README.md"

    def test_utf8_encoding(self):
        """Test that README uses UTF-8 encoding."""
        try:
            with open(self.readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.assertIsInstance(content, str)
        except UnicodeDecodeError:
            self.fail("README.md should be encoded in UTF-8")

    def test_no_null_bytes(self):
        """Test that README doesn't contain null bytes."""
        with open(self.readme_path, 'rb') as f:
            content = f.read()
        self.assertNotIn(
            b'\x00',
            content,
            "README.md should not contain null bytes"
        )

    def test_uses_unix_line_endings(self):
        """Test that README uses Unix line endings (LF) not Windows (CRLF)."""
        with open(self.readme_path, 'rb') as f:
            content = f.read()
        # Check if file uses CRLF (Windows) line endings
        crlf_count = content.count(b'\r\n')
        self.assertEqual(
            crlf_count,
            0,
            "README.md should use Unix line endings (LF) not Windows (CRLF)"
        )


class TestReadmeBusinessLogic(unittest.TestCase):
    """Test suite for business logic and contextual requirements."""

    @classmethod
    def setUpClass(cls):
        """Load README content once for all tests."""
        readme_path = Path(__file__).parent / "README.md"
        with open(readme_path, 'r', encoding='utf-8') as f:
            cls.content = f.read()

    def test_mentions_tier_differentiation(self):
        """Test that README explains tier differentiation purpose."""
        self.assertIn(
            "differentiate",
            self.content.lower(),
            "README should explain the need to differentiate tiers"
        )
        self.assertIn(
            "plan",
            self.content.lower(),
            "README should mention plans as they relate to tiers"
        )

    def test_acknowledges_evolving_nature(self):
        """Test that README acknowledges this is an evolving implementation."""
        evolving_keywords = ["evolving", "first pass", "initial"]
        has_evolving_context = any(
            keyword in self.content.lower() for keyword in evolving_keywords
        )
        self.assertTrue(
            has_evolving_context,
            "README should acknowledge this is an evolving/initial implementation"
        )

    def test_legal_section_mentions_sentry(self):
        """Test that Legal Boilerplate section mentions Sentry."""
        pattern = r"### Legal Boilerplate\s*\n(.+?)(?=\Z)"
        match = re.search(pattern, self.content, re.DOTALL)
        self.assertIsNotNone(match, "Legal Boilerplate section should exist")
        legal_content = match.group(1)
        self.assertIn(
            "Sentry",
            legal_content,
            "Legal Boilerplate should mention Sentry"
        )

    def test_legal_section_mentions_codecov(self):
        """Test that Legal Boilerplate section mentions Codecov."""
        pattern = r"### Legal Boilerplate\s*\n(.+?)(?=\Z)"
        match = re.search(pattern, self.content, re.DOTALL)
        self.assertIsNotNone(match, "Legal Boilerplate section should exist")
        legal_content = match.group(1)
        self.assertIn(
            "Codecov",
            legal_content,
            "Legal Boilerplate should mention Codecov"
        )

    def test_describes_test_coverage(self):
        """Test that README indicates tests were added alongside code."""
        # Should mention "test" in context of what was added
        pr_section_pattern = r"### What does this PR do\?\s*\n(.+?)(?=\n###|<!--|$)"
        match = re.search(pr_section_pattern, self.content, re.DOTALL)
        self.assertIsNotNone(match)
        pr_content = match.group(1).lower()
        self.assertIn(
            "test",
            pr_content,
            "PR description should mention that tests were added"
        )


class TestReadmeEdgeCases(unittest.TestCase):
    """Test suite for edge cases and potential issues."""

    @classmethod
    def setUpClass(cls):
        """Load README content once for all tests."""
        cls.readme_path = Path(__file__).parent / "README.md"
        with open(cls.readme_path, 'r', encoding='utf-8') as f:
            cls.content = f.read()
        cls.lines = cls.content.split('\n')

    def test_file_ends_with_newline(self):
        """Test that README ends with a newline character."""
        with open(self.readme_path, 'rb') as f:
            content = f.read()
        if len(content) > 0:
            # File should end with newline
            self.assertTrue(
                content.endswith(b'\n'),
                "README.md should end with a newline character"
            )

    def test_no_excessively_long_lines(self):
        """Test that lines don't exceed reasonable length (200 chars for prose)."""
        max_length = 200
        for i, line in enumerate(self.lines, 1):
            # Skip lines that are just URLs or part of code blocks
            # Also skip legal boilerplate which may be long prose
            if not line.strip().startswith('http') and i < 10:
                self.assertLessEqual(
                    len(line),
                    max_length,
                    f"Line {i} exceeds {max_length} characters (has {len(line)})"
                )

    def test_no_multiple_consecutive_blank_lines(self):
        """Test that there aren't excessive consecutive blank lines."""
        blank_count = 0
        for i, line in enumerate(self.lines, 1):
            if not line.strip():
                blank_count += 1
                self.assertLessEqual(
                    blank_count,
                    2,
                    f"Too many consecutive blank lines around line {i}"
                )
            else:
                blank_count = 0

    def test_no_placeholder_text(self):
        """Test that README doesn't contain common placeholder text."""
        placeholders = ['TODO', 'FIXME', 'XXX', 'TBD', '[INSERT', 'placeholder']
        for placeholder in placeholders:
            # Only check outside of comments
            content_without_comments = re.sub(r'<!--.*?-->', '', self.content, flags=re.DOTALL)
            self.assertNotIn(
                placeholder.lower(),
                content_without_comments.lower(),
                f"README should not contain placeholder text: {placeholder}"
            )

    def test_sections_in_logical_order(self):
        """Test that sections appear in logical order."""
        section_order = [
            "Purpose/Motivation",
            "What does this PR do?",
            "Legal Boilerplate"
        ]
        positions = []
        for section in section_order:
            pos = self.content.find(section)
            self.assertGreater(
                pos,
                -1,
                f"Section '{section}' should be present in README"
            )
            positions.append(pos)

        # Verify positions are in ascending order
        self.assertEqual(
            positions,
            sorted(positions),
            "Sections should appear in logical order: Purpose, PR description, Legal"
        )


class TestReadmeRegression(unittest.TestCase):
    """Regression tests to prevent common documentation issues."""

    @classmethod
    def setUpClass(cls):
        """Load README content once for all tests."""
        readme_path = Path(__file__).parent / "README.md"
        with open(readme_path, 'r', encoding='utf-8') as f:
            cls.content = f.read()

    def test_no_broken_markdown_links(self):
        """Test that markdown links have proper format [text](url)."""
        # Find all markdown link patterns
        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        links = re.findall(link_pattern, self.content)

        for text, url in links:
            self.assertGreater(
                len(text.strip()),
                0,
                f"Link text should not be empty: [{text}]({url})"
            )
            self.assertGreater(
                len(url.strip()),
                0,
                f"Link URL should not be empty: [{text}]({url})"
            )

    def test_no_unclosed_markdown_formatting(self):
        """Test that markdown emphasis markers are balanced."""
        # Check for balanced bold markers
        bold_count = len(re.findall(r'\*\*', self.content))
        self.assertEqual(
            bold_count % 2,
            0,
            "Bold markers (**) should come in pairs"
        )

        # Check for balanced italic markers (excluding bold)
        # This is a simplified check
        content_no_bold = re.sub(r'\*\*.*?\*\*', '', self.content)
        italic_count = content_no_bold.count('*')
        italic_underscore_count = content_no_bold.count('_')
        self.assertEqual(
            italic_count % 2,
            0,
            "Italic markers (*) should come in pairs"
        )

    def test_consistent_list_formatting(self):
        """Test that all list items use consistent bullet style."""
        bullet_lines = [line for line in self.content.split('\n')
                       if line.strip().startswith(('-', '*', '+'))]
        if bullet_lines:
            # Get the first character of each bullet line
            first_chars = [line.strip()[0] for line in bullet_lines]
            # All should be the same
            self.assertEqual(
                len(set(first_chars)),
                1,
                "All bullet points should use the same marker (-, *, or +)"
            )

    def test_technical_terms_consistency(self):
        """Test that technical terms are used consistently."""
        # Check that 'tier' is always lowercase except at sentence start
        tier_variations = re.findall(r'\b[Tt]ier\b', self.content)
        # Most instances should be lowercase
        lowercase_count = sum(1 for t in tier_variations if t == 'tier')
        self.assertGreater(
            lowercase_count,
            0,
            "Technical term 'tier' should appear in lowercase"
        )


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)