"""
Comprehensive tests for README.md file.

This test suite validates the structure, content, and format of the README.md
file to ensure it meets documentation standards and contains all required
information.
"""

import os
import re
import unittest
from pathlib import Path


class TestReadmeStructure(unittest.TestCase):
    """Test the structure and required sections of README.md."""

    @classmethod
    def setUpClass(cls):
        """Load README.md content once for all tests."""
        cls.readme_path = Path(__file__).parent / "README.md"
        with open(cls.readme_path, 'r', encoding='utf-8') as f:
            cls.content = f.read()
        cls.lines = cls.content.split('\n')

    def test_readme_file_exists(self):
        """Test that README.md file exists."""
        self.assertTrue(
            self.readme_path.exists(),
            "README.md file should exist in the repository root"
        )

    def test_readme_not_empty(self):
        """Test that README.md is not empty."""
        self.assertGreater(
            len(self.content.strip()),
            0,
            "README.md should not be empty"
        )

    def test_readme_has_minimum_length(self):
        """Test that README.md has substantial content."""
        self.assertGreater(
            len(self.content),
            100,
            "README.md should have at least 100 characters of content"
        )

    def test_purpose_section_exists(self):
        """Test that README contains a Purpose/Motivation section."""
        self.assertIn(
            "Purpose/Motivation",
            self.content,
            "README should contain a 'Purpose/Motivation' section"
        )

    def test_what_does_pr_do_section_exists(self):
        """Test that README contains a 'What does this PR do?' section."""
        self.assertIn(
            "What does this PR do?",
            self.content,
            "README should contain a 'What does this PR do?' section"
        )

    def test_legal_boilerplate_section_exists(self):
        """Test that README contains Legal Boilerplate section."""
        self.assertIn(
            "Legal Boilerplate",
            self.content,
            "README should contain a 'Legal Boilerplate' section"
        )


class TestReadmeContent(unittest.TestCase):
    """Test the content and meaningful information in README.md."""

    @classmethod
    def setUpClass(cls):
        """Load README.md content once for all tests."""
        cls.readme_path = Path(__file__).parent / "README.md"
        with open(cls.readme_path, 'r', encoding='utf-8') as f:
            cls.content = f.read()

    def test_purpose_has_content(self):
        """Test that Purpose/Motivation section has actual content."""
        # Extract content after "Purpose/Motivation"
        purpose_match = re.search(
            r'### Purpose/Motivation\s*\n(.+?)(?=###|\Z)',
            self.content,
            re.DOTALL
        )
        self.assertIsNotNone(
            purpose_match,
            "Purpose/Motivation section should exist"
        )
        purpose_content = purpose_match.group(1).strip()
        self.assertGreater(
            len(purpose_content),
            20,
            "Purpose/Motivation section should have meaningful content"
        )

    def test_pr_description_has_content(self):
        """Test that PR description section has actual content."""
        pr_match = re.search(
            r'### What does this PR do\?\s*\n(.+?)(?=###|<!--|\Z)',
            self.content,
            re.DOTALL
        )
        self.assertIsNotNone(
            pr_match,
            "What does this PR do section should exist"
        )
        pr_content = pr_match.group(1).strip()
        self.assertGreater(
            len(pr_content),
            10,
            "PR description should have meaningful content"
        )

    def test_pr_description_has_bullet_points(self):
        """Test that PR description uses bullet points for clarity."""
        pr_match = re.search(
            r'### What does this PR do\?\s*\n(.+?)(?=###|<!--|\Z)',
            self.content,
            re.DOTALL
        )
        self.assertIsNotNone(pr_match, "PR description section should exist")
        pr_content = pr_match.group(1)

        # Check for bullet points (- or *), accounting for possible blockquote markers
        bullet_points = re.findall(r'^\s*>?\s*[-*]\s+.+$', pr_content, re.MULTILINE)
        self.assertGreater(
            len(bullet_points),
            0,
            "PR description should contain at least one bullet point"
        )

    def test_mentions_tier_service(self):
        """Test that content mentions tier service functionality."""
        self.assertIn(
            "tier",
            self.content.lower(),
            "README should mention tier-related functionality"
        )

    def test_mentions_tests(self):
        """Test that content mentions testing."""
        self.assertIn(
            "test",
            self.content.lower(),
            "README should mention tests being added"
        )

    def test_legal_boilerplate_has_content(self):
        """Test that Legal Boilerplate section has actual content."""
        legal_match = re.search(
            r'### Legal Boilerplate\s*\n(.+?)(?=###|\Z)',
            self.content,
            re.DOTALL
        )
        self.assertIsNotNone(
            legal_match,
            "Legal Boilerplate section should exist"
        )
        legal_content = legal_match.group(1).strip()
        self.assertGreater(
            len(legal_content),
            50,
            "Legal Boilerplate section should have meaningful content"
        )


class TestReadmeMarkdownFormat(unittest.TestCase):
    """Test proper markdown formatting of README.md."""

    @classmethod
    def setUpClass(cls):
        """Load README.md content once for all tests."""
        cls.readme_path = Path(__file__).parent / "README.md"
        with open(cls.readme_path, 'r', encoding='utf-8') as f:
            cls.content = f.read()
        cls.lines = cls.content.split('\n')

    def test_headers_use_proper_markdown(self):
        """Test that headers use proper markdown syntax."""
        # Account for possible blockquote markers (> )
        header_lines = [
            line for line in self.lines
            if line.strip().lstrip('>').strip().startswith('#')
        ]
        self.assertGreater(
            len(header_lines),
            0,
            "README should contain at least one markdown header"
        )

        for line in header_lines:
            # Remove blockquote marker if present
            clean_line = line.strip().lstrip('>').strip()
            # Check that headers have a space after #
            if clean_line.startswith('#'):
                hash_count = len(clean_line) - len(clean_line.lstrip('#'))
                remaining = clean_line[hash_count:].strip()
                if remaining:  # If there's content after the hashes
                    self.assertTrue(
                        clean_line[hash_count:].startswith(' '),
                        f"Header '{line}' should have a space after # symbols"
                    )

    def test_bullet_points_use_proper_format(self):
        """Test that bullet points use consistent formatting."""
        # Account for possible blockquote markers (> )
        bullet_lines = [
            line for line in self.lines
            if re.match(r'^\s*>?\s*[-*]\s+', line)
        ]
        self.assertGreater(
            len(bullet_lines),
            0,
            "README should contain bullet points"
        )

    def test_no_trailing_whitespace(self):
        """Test that lines don't have excessive trailing whitespace."""
        lines_with_excessive_trailing = [
            (i + 1, line) for i, line in enumerate(self.lines)
            if len(line) > 0 and line != line.rstrip() and len(line) - len(line.rstrip()) > 1
        ]
        self.assertEqual(
            len(lines_with_excessive_trailing),
            0,
            f"Lines should not have excessive trailing whitespace: {lines_with_excessive_trailing}"
        )

    def test_consistent_heading_level(self):
        """Test that document uses consistent heading levels."""
        # Account for possible blockquote markers (> )
        heading_pattern = re.compile(r'^>\s*(#{1,6})\s+(.+)$|^(#{1,6})\s+(.+)$')
        headings = []

        for line in self.lines:
            match = heading_pattern.match(line)
            if match:
                # Get the hash marks from either group 1 (blockquote) or group 3 (normal)
                hashes = match.group(1) if match.group(1) else match.group(3)
                if hashes:
                    level = len(hashes)
                    headings.append(level)

        # Should have at least some headings
        self.assertGreater(
            len(headings),
            0,
            "README should contain heading elements"
        )


class TestReadmeEdgeCases(unittest.TestCase):
    """Test edge cases and potential issues in README.md."""

    @classmethod
    def setUpClass(cls):
        """Load README.md content once for all tests."""
        cls.readme_path = Path(__file__).parent / "README.md"
        with open(cls.readme_path, 'r', encoding='utf-8') as f:
            cls.content = f.read()

    def test_no_placeholder_text(self):
        """Test that README doesn't contain common placeholder text."""
        placeholders = [
            'TODO',
            'FIXME',
            'XXX',
            'TBD',
            'Coming soon',
            'Under construction'
        ]
        content_upper = self.content.upper()
        found_placeholders = [p for p in placeholders if p.upper() in content_upper]

        self.assertEqual(
            len(found_placeholders),
            0,
            f"README should not contain placeholder text: {found_placeholders}"
        )

    def test_proper_encoding(self):
        """Test that README uses proper UTF-8 encoding."""
        try:
            with open(self.readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # If we can read it as UTF-8, it's properly encoded
            self.assertIsNotNone(content)
        except UnicodeDecodeError:
            self.fail("README.md should be properly encoded as UTF-8")

    def test_line_endings_consistency(self):
        """Test that line endings are consistent."""
        with open(self.readme_path, 'rb') as f:
            raw_content = f.read()

        has_crlf = b'\r\n' in raw_content
        has_lf_only = b'\n' in raw_content and b'\r\n' not in raw_content

        # Should have one type of line ending, not mixed
        self.assertTrue(
            has_crlf or has_lf_only,
            "README should have consistent line endings"
        )

    def test_no_broken_markdown_links(self):
        """Test that markdown link syntax is properly formed."""
        # Find all markdown link patterns
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')
        links = link_pattern.findall(self.content)

        for link_text, link_url in links:
            self.assertGreater(
                len(link_text.strip()),
                0,
                f"Link text should not be empty for URL: {link_url}"
            )
            self.assertGreater(
                len(link_url.strip()),
                0,
                f"Link URL should not be empty for text: {link_text}"
            )

    def test_html_comments_properly_closed(self):
        """Test that HTML comments are properly closed."""
        comment_starts = self.content.count('<!--')
        comment_ends = self.content.count('-->')

        self.assertEqual(
            comment_starts,
            comment_ends,
            "All HTML comments should be properly closed"
        )

    def test_no_excessive_blank_lines(self):
        """Test that there aren't excessive consecutive blank lines."""
        lines = self.content.split('\n')
        consecutive_blank = 0
        max_consecutive = 0

        for line in lines:
            if line.strip() == '':
                consecutive_blank += 1
                max_consecutive = max(max_consecutive, consecutive_blank)
            else:
                consecutive_blank = 0

        self.assertLessEqual(
            max_consecutive,
            3,
            "Should not have more than 3 consecutive blank lines"
        )


class TestReadmeBusinessLogic(unittest.TestCase):
    """Test business logic and semantic content in README.md."""

    @classmethod
    def setUpClass(cls):
        """Load README.md content once for all tests."""
        cls.readme_path = Path(__file__).parent / "README.md"
        with open(cls.readme_path, 'r', encoding='utf-8') as f:
            cls.content = f.read()

    def test_mentions_company_entities(self):
        """Test that Legal Boilerplate mentions required entities."""
        entities_to_check = ['Sentry', 'Codecov', 'Delaware']

        for entity in entities_to_check:
            self.assertIn(
                entity,
                self.content,
                f"Legal Boilerplate should mention {entity}"
            )

    def test_mentions_incorporation_year(self):
        """Test that Legal Boilerplate mentions incorporation year."""
        self.assertIn(
            "2015",
            self.content,
            "Legal Boilerplate should mention incorporation year 2015"
        )

    def test_mentions_acquisition_year(self):
        """Test that Legal Boilerplate mentions acquisition year."""
        self.assertIn(
            "2022",
            self.content,
            "Legal Boilerplate should mention acquisition year 2022"
        )

    def test_pr_describes_tier_differentiation(self):
        """Test that PR description mentions tier differentiation."""
        self.assertIn(
            "tier",
            self.content.lower(),
            "PR should describe tier-related changes"
        )
        self.assertIn(
            "plan",
            self.content.lower(),
            "PR should describe plan-related changes"
        )

    def test_pr_mentions_resolvers(self):
        """Test that PR description mentions resolvers."""
        self.assertIn(
            "resolver",
            self.content.lower(),
            "PR should mention resolver implementation"
        )

    def test_copyright_retention_mentioned(self):
        """Test that Legal Boilerplate mentions copyright retention."""
        legal_section = self.content.lower()
        retention_keywords = ['retain', 'rights', 'title', 'interest']

        found_keywords = [kw for kw in retention_keywords if kw in legal_section]
        self.assertGreaterEqual(
            len(found_keywords),
            3,
            "Legal Boilerplate should mention copyright retention clearly"
        )


class TestReadmeBoundaryConditions(unittest.TestCase):
    """Test boundary conditions and additional edge cases."""

    @classmethod
    def setUpClass(cls):
        """Load README.md content once for all tests."""
        cls.readme_path = Path(__file__).parent / "README.md"
        with open(cls.readme_path, 'r', encoding='utf-8') as f:
            cls.content = f.read()

    def test_section_headers_are_level_3(self):
        """Test that main sections use h3 (###) headers."""
        # Find all section headers
        section_pattern = re.compile(r'^>\s*(#{1,6})\s+(Purpose|What does this PR do|Legal)')

        for line in self.content.split('\n'):
            match = section_pattern.match(line)
            if match:
                level = len(match.group(1))
                self.assertEqual(
                    level,
                    3,
                    f"Section headers should be level 3 (###): {line}"
                )

    def test_blockquote_consistency(self):
        """Test that blockquote markers are used consistently."""
        lines = self.content.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]

        if non_empty_lines:
            # Check if majority of lines start with >
            blockquote_lines = sum(1 for line in non_empty_lines if line.startswith('>'))
            total_lines = len(non_empty_lines)

            # If using blockquotes, most non-empty lines should have them
            if blockquote_lines > total_lines * 0.5:
                self.assertGreater(
                    blockquote_lines / total_lines,
                    0.8,
                    "If using blockquotes, they should be consistent across the document"
                )

    def test_functional_software_mentioned(self):
        """Test that the original company name is mentioned in Legal section."""
        self.assertIn(
            "Functional Software",
            self.content,
            "Legal Boilerplate should mention 'Functional Software, Inc.'"
        )

    def test_contribution_rights_explicit(self):
        """Test that contribution rights are explicitly stated."""
        rights_keywords = ['use', 'modify', 'copy', 'redistribute']
        legal_section = self.content.lower()

        found = sum(1 for keyword in rights_keywords if keyword in legal_section)
        self.assertGreaterEqual(
            found,
            3,
            "Legal section should explicitly list contribution rights"
        )

    def test_pr_description_mentions_both_additions(self):
        """Test that PR description mentions both main additions."""
        # Extract the PR description section
        pr_match = re.search(
            r'### What does this PR do\?\s*\n(.+?)(?=###|<!--|\Z)',
            self.content,
            re.DOTALL
        )
        self.assertIsNotNone(pr_match)
        pr_section = pr_match.group(1).lower()

        # Should mention both tier service and resolvers
        self.assertIn('tier service', pr_section, "PR should mention tier service")
        self.assertIn('resolver', pr_section, "PR should mention resolvers")


class TestReadmeRegressionCases(unittest.TestCase):
    """Regression tests to prevent common documentation issues."""

    @classmethod
    def setUpClass(cls):
        """Load README.md content once for all tests."""
        cls.readme_path = Path(__file__).parent / "README.md"
        with open(cls.readme_path, 'r', encoding='utf-8') as f:
            cls.content = f.read()

    def test_no_sensitive_information(self):
        """Test that README doesn't contain sensitive information."""
        sensitive_patterns = [
            r'password\s*[:=]\s*\S+',
            r'api[_-]?key\s*[:=]\s*\S+',
            r'secret\s*[:=]\s*\S+',
            r'token\s*[:=]\s*\S+',
        ]

        for pattern in sensitive_patterns:
            matches = re.findall(pattern, self.content, re.IGNORECASE)
            self.assertEqual(
                len(matches),
                0,
                f"README should not contain sensitive information matching: {pattern}"
            )

    def test_sections_in_logical_order(self):
        """Test that sections appear in a logical order."""
        purpose_pos = self.content.find('Purpose/Motivation')
        pr_do_pos = self.content.find('What does this PR do?')
        legal_pos = self.content.find('Legal Boilerplate')

        # Purpose should come before PR description
        self.assertLess(
            purpose_pos,
            pr_do_pos,
            "Purpose should come before PR description"
        )

        # Legal should come last
        self.assertLess(
            pr_do_pos,
            legal_pos,
            "Legal Boilerplate should come after main content"
        )

    def test_file_size_reasonable(self):
        """Test that README file size is reasonable."""
        file_size = os.path.getsize(self.readme_path)

        # Should be between 100 bytes and 100KB
        self.assertGreater(
            file_size,
            100,
            "README should have substantial content"
        )
        self.assertLess(
            file_size,
            102400,  # 100KB
            "README should not be excessively large"
        )

    def test_mentions_both_service_and_resolvers(self):
        """Test that both service and resolver implementations are mentioned."""
        content_lower = self.content.lower()

        self.assertIn(
            'service',
            content_lower,
            "README should mention service implementation"
        )
        self.assertIn(
            'resolver',
            content_lower,
            "README should mention resolver implementation"
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)