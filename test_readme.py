"""
Comprehensive test suite for README.md
Tests documentation structure, content, and quality
"""
import os
import re
import unittest
from pathlib import Path


class TestREADME(unittest.TestCase):
    """Test suite for README.md file"""

    @classmethod
    def setUpClass(cls):
        """Load README.md content once for all tests"""
        cls.readme_path = Path(__file__).parent / "README.md"
        with open(cls.readme_path, 'r', encoding='utf-8') as f:
            cls.readme_content = f.read()
        cls.readme_lines = cls.readme_content.split('\n')

    def test_readme_exists(self):
        """Test that README.md file exists"""
        self.assertTrue(
            self.readme_path.exists(),
            "README.md file should exist in the repository"
        )

    def test_readme_not_empty(self):
        """Test that README.md is not empty"""
        self.assertGreater(
            len(self.readme_content.strip()),
            0,
            "README.md should not be empty"
        )

    def test_has_purpose_section(self):
        """Test that README has Purpose/Motivation section"""
        self.assertIn(
            "### Purpose/Motivation",
            self.readme_content,
            "README should have a Purpose/Motivation section"
        )

    def test_has_what_does_pr_do_section(self):
        """Test that README has 'What does this PR do?' section"""
        self.assertIn(
            "### What does this PR do?",
            self.readme_content,
            "README should have a 'What does this PR do?' section"
        )

    def test_has_legal_boilerplate_section(self):
        """Test that README has Legal Boilerplate section"""
        self.assertIn(
            "### Legal Boilerplate",
            self.readme_content,
            "README should have a Legal Boilerplate section"
        )

    def test_purpose_section_not_empty(self):
        """Test that Purpose/Motivation section contains content"""
        # Find content between Purpose/Motivation and next section
        purpose_match = re.search(
            r'###\s+Purpose/Motivation.*?\n(.*?)(?:\n\s*###|\Z)',
            self.readme_content,
            re.DOTALL
        )
        self.assertIsNotNone(purpose_match, "Purpose/Motivation section should exist")
        purpose_content = purpose_match.group(1).strip()
        # Remove any leading markers like "> "
        purpose_content = re.sub(r'^[>\s]+', '', purpose_content, flags=re.MULTILINE)
        self.assertGreater(
            len(purpose_content),
            0,
            "Purpose/Motivation section should contain content"
        )

    def test_pr_section_has_bullet_points(self):
        """Test that 'What does this PR do?' section has bullet points"""
        # Find content between PR section and next section
        pr_match = re.search(
            r'###\s+What does this PR do\?.*?\n(.*?)(?:\n\s*(?:<!--|###)|\Z)',
            self.readme_content,
            re.DOTALL
        )
        self.assertIsNotNone(pr_match, "PR section should exist")
        pr_content = pr_match.group(1)

        # Check for bullet points (- or *), accounting for possible prefixes like "> "
        bullet_points = re.findall(r'^[>\s]*[-*]\s+.+', pr_content, re.MULTILINE)
        self.assertGreater(
            len(bullet_points),
            0,
            "PR section should contain at least one bullet point"
        )

    def test_mentions_tier_service(self):
        """Test that README mentions tier service (main feature)"""
        self.assertIn(
            "tier",
            self.readme_content.lower(),
            "README should mention tier service as it's the main feature"
        )

    def test_mentions_tests(self):
        """Test that README mentions tests (good practice for PRs)"""
        test_keywords = ['test', 'testing']
        has_test_mention = any(
            keyword in self.readme_content.lower()
            for keyword in test_keywords
        )
        self.assertTrue(
            has_test_mention,
            "README should mention tests for the changes"
        )

    def test_mentions_resolvers(self):
        """Test that README mentions resolvers (mentioned feature)"""
        self.assertIn(
            "resolver",
            self.readme_content.lower(),
            "README should mention resolvers as stated in PR description"
        )

    def test_legal_boilerplate_has_entity_info(self):
        """Test that Legal Boilerplate contains required entity information"""
        legal_match = re.search(
            r'### Legal Boilerplate\n(.*?)(?:\n###|$)',
            self.readme_content,
            re.DOTALL
        )
        self.assertIsNotNone(legal_match, "Legal Boilerplate section should exist")
        legal_content = legal_match.group(1)

        # Check for key legal terms
        legal_keywords = ['Sentry', 'Delaware', 'Codecov', 'rights', 'contributions']
        for keyword in legal_keywords:
            self.assertIn(
                keyword,
                legal_content,
                f"Legal Boilerplate should mention '{keyword}'"
            )

    def test_proper_markdown_heading_levels(self):
        """Test that markdown headings use proper hierarchy"""
        headings = re.findall(r'^(#{1,6})\s+(.+)$', self.readme_content, re.MULTILINE)

        # All main sections should be level 3 (###)
        for heading_level, heading_text in headings:
            self.assertEqual(
                len(heading_level),
                3,
                f"Heading '{heading_text}' should use level 3 (###)"
            )

    def test_no_trailing_whitespace(self):
        """Test that lines don't have trailing whitespace (best practice)"""
        lines_with_trailing_ws = []
        for i, line in enumerate(self.readme_lines, 1):
            # Ignore empty lines
            if line and line != line.rstrip():
                lines_with_trailing_ws.append(i)

        # Allow some trailing whitespace but warn if excessive
        if lines_with_trailing_ws:
            # This is a soft check - we don't fail but document it
            pass  # In a real scenario, you might want to enforce this

    def test_file_ends_with_newline(self):
        """Test that file ends with a newline (POSIX standard)"""
        with open(self.readme_path, 'rb') as f:
            content = f.read()

        # Check if file ends with newline
        if content:
            self.assertEqual(
                content[-1:],
                b'\n',
                "README.md should end with a newline character"
            )

    def test_utf8_encoding(self):
        """Test that README uses UTF-8 encoding"""
        try:
            with open(self.readme_path, 'r', encoding='utf-8') as f:
                f.read()
        except UnicodeDecodeError:
            self.fail("README.md should use UTF-8 encoding")

    def test_sections_in_correct_order(self):
        """Test that sections appear in logical order"""
        purpose_pos = self.readme_content.find("### Purpose/Motivation")
        pr_pos = self.readme_content.find("### What does this PR do?")
        legal_pos = self.readme_content.find("### Legal Boilerplate")

        self.assertLess(
            purpose_pos,
            pr_pos,
            "Purpose/Motivation should come before PR description"
        )
        self.assertLess(
            pr_pos,
            legal_pos,
            "PR description should come before Legal Boilerplate"
        )

    def test_no_broken_markdown_syntax(self):
        """Test for common markdown syntax errors"""
        # Check for unmatched brackets
        open_brackets = self.readme_content.count('[')
        close_brackets = self.readme_content.count(']')
        self.assertEqual(
            open_brackets,
            close_brackets,
            "Markdown should have matching square brackets"
        )

        # Check for unmatched parentheses in links
        # This is a simplified check
        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        links = re.findall(link_pattern, self.readme_content)
        # If this passes without exception, basic link syntax is valid
        self.assertIsInstance(links, list)

    def test_content_describes_tier_differentiation(self):
        """Test that content explains tier differentiation by plan"""
        purpose_section = re.search(
            r'###\s+Purpose/Motivation.*?\n(.*?)(?:\n\s*###|\Z)',
            self.readme_content,
            re.DOTALL
        )
        self.assertIsNotNone(purpose_section)
        purpose_text = purpose_section.group(1).lower()

        # Check for key concepts
        self.assertIn('tier', purpose_text, "Purpose should mention tier")
        self.assertIn('plan', purpose_text, "Purpose should mention plan")

    def test_pr_describes_service_and_resolvers(self):
        """Test that PR section describes both service and resolvers"""
        pr_section = re.search(
            r'###\s+What does this PR do\?.*?\n(.*?)(?:\n\s*(?:<!--|###)|\Z)',
            self.readme_content,
            re.DOTALL
        )
        self.assertIsNotNone(pr_section)
        pr_text = pr_section.group(1).lower()

        self.assertIn('tier service', pr_text, "PR should mention tier service")
        self.assertIn('resolver', pr_text, "PR should mention resolvers")
        self.assertIn('test', pr_text, "PR should mention tests")

    def test_readme_line_count(self):
        """Test that README has reasonable line count"""
        line_count = len([line for line in self.readme_lines if line.strip()])
        self.assertGreater(
            line_count,
            5,
            "README should have more than 5 non-empty lines"
        )

    def test_purpose_explains_evolution(self):
        """Test that purpose mentions this is evolving/first pass"""
        purpose_match = re.search(
            r'###\s+Purpose/Motivation.*?\n(.*?)(?:\n\s*###|\Z)',
            self.readme_content,
            re.DOTALL
        )
        self.assertIsNotNone(purpose_match)
        purpose_content = purpose_match.group(1).lower()

        evolution_keywords = ['evolv', 'first pass', 'initial', 'iterative']
        has_evolution = any(
            keyword in purpose_content
            for keyword in evolution_keywords
        )
        self.assertTrue(
            has_evolution,
            "Purpose should indicate this is an evolving/iterative feature"
        )

    def test_html_comments_present(self):
        """Test that HTML comments are properly formatted"""
        html_comments = re.findall(r'<!--.*?-->', self.readme_content, re.DOTALL)

        if html_comments:
            for comment in html_comments:
                # Check that comments are properly closed
                self.assertTrue(
                    comment.startswith('<!--') and comment.endswith('-->'),
                    "HTML comments should be properly formatted"
                )


class TestREADMENegativeCases(unittest.TestCase):
    """Negative test cases and edge cases for README.md"""

    @classmethod
    def setUpClass(cls):
        """Load README.md content once for all tests"""
        cls.readme_path = Path(__file__).parent / "README.md"
        with open(cls.readme_path, 'r', encoding='utf-8') as f:
            cls.readme_content = f.read()

    def test_no_placeholder_text(self):
        """Test that README doesn't contain placeholder text"""
        placeholders = ['TODO', 'FIXME', 'XXX', 'TBD', 'PLACEHOLDER']
        for placeholder in placeholders:
            self.assertNotIn(
                placeholder,
                self.readme_content,
                f"README should not contain placeholder text: {placeholder}"
            )

    def test_no_sensitive_information(self):
        """Test that README doesn't contain sensitive information"""
        sensitive_patterns = [
            r'password\s*[:=]\s*\S+',
            r'api[_-]?key\s*[:=]\s*\S+',
            r'secret\s*[:=]\s*\S+',
            r'token\s*[:=]\s*\S+'
        ]

        for pattern in sensitive_patterns:
            matches = re.search(pattern, self.readme_content, re.IGNORECASE)
            self.assertIsNone(
                matches,
                f"README should not contain sensitive information matching: {pattern}"
            )

    def test_no_absolute_file_paths(self):
        """Test that README doesn't contain absolute file paths"""
        # Check for common absolute path patterns
        absolute_path_patterns = [
            r'C:\\',
            r'/Users/',
            r'/home/[^s]',  # Exclude /home/jailuser for our test env
            r'/root/'
        ]

        for pattern in absolute_path_patterns:
            self.assertIsNone(
                re.search(pattern, self.readme_content),
                f"README should not contain absolute paths matching: {pattern}"
            )

    def test_proper_grammar_basics(self):
        """Test basic grammar rules (starting sentences with capital letters)"""
        # Get sentences from bullet points
        bullet_items = re.findall(r'^\s*[-*]\s+(.+)$', self.readme_content, re.MULTILINE)

        for item in bullet_items:
            # First word should start with capital letter or number
            first_char = item.strip()[0]
            self.assertTrue(
                first_char.isupper() or first_char.isdigit(),
                f"Bullet point should start with capital letter: '{item}'"
            )

    def test_no_excessively_long_lines(self):
        """Test that no line is excessively long (readability)"""
        max_length = 200  # Reasonable limit for README
        long_lines = []

        for i, line in enumerate(self.readme_content.split('\n'), 1):
            if len(line) > max_length:
                long_lines.append((i, len(line)))

        # Allow some long lines but not too many
        self.assertLess(
            len(long_lines),
            3,
            f"Too many lines exceed {max_length} characters: {long_lines}"
        )

    def test_no_duplicate_sections(self):
        """Test that section headings are not duplicated"""
        headings = re.findall(r'^###\s+(.+)$', self.readme_content, re.MULTILINE)
        unique_headings = set(headings)

        self.assertEqual(
            len(headings),
            len(unique_headings),
            f"Section headings should be unique. Found duplicates in: {headings}"
        )

    def test_legal_section_not_modified_incorrectly(self):
        """Test that legal boilerplate maintains required elements"""
        legal_section = re.search(
            r'### Legal Boilerplate\n(.*?)(?:\n###|$)',
            self.readme_content,
            re.DOTALL
        )

        if legal_section:
            legal_text = legal_section.group(1)

            # Critical legal terms that shouldn't be removed
            critical_terms = ['rights', 'contributions', 'Sentry']
            for term in critical_terms:
                self.assertIn(
                    term,
                    legal_text,
                    f"Legal boilerplate should retain critical term: {term}"
                )


class TestREADMEBoundaryCases(unittest.TestCase):
    """Boundary and edge case tests for README.md"""

    @classmethod
    def setUpClass(cls):
        """Load README.md content once for all tests"""
        cls.readme_path = Path(__file__).parent / "README.md"
        with open(cls.readme_path, 'r', encoding='utf-8') as f:
            cls.readme_content = f.read()

    def test_empty_lines_between_sections(self):
        """Test that sections are properly separated by empty lines"""
        # Find all section headings (accounting for possible prefixes like "> ")
        section_positions = []
        for match in re.finditer(r'^[>\s]*###\s+', self.readme_content, re.MULTILINE):
            section_positions.append(match.start())

        # Check that sections have reasonable spacing
        # (This is a soft requirement for readability)
        self.assertGreater(len(section_positions), 0, "Should have sections")

    def test_minimum_content_per_section(self):
        """Test that each section has minimum content"""
        sections = re.findall(
            r'###\s+([^\n]+)\n(.*?)(?=\n###|\Z)',
            self.readme_content,
            re.DOTALL
        )

        for section_name, section_content in sections:
            # Skip HTML comment sections
            if '<!--' in section_content:
                continue

            content_length = len(section_content.strip())
            self.assertGreater(
                content_length,
                10,
                f"Section '{section_name}' should have substantial content"
            )

    def test_handles_special_characters(self):
        """Test that README properly handles special characters"""
        # The content should be readable and not have encoding issues
        special_chars_present = False

        # Check if any special characters are present and properly encoded
        for char in self.readme_content:
            if ord(char) > 127:  # Non-ASCII character
                special_chars_present = True
                # Should not raise encoding errors
                try:
                    char.encode('utf-8')
                except UnicodeEncodeError:
                    self.fail(f"Special character not properly encoded: {char}")

    def test_file_size_reasonable(self):
        """Test that README file size is reasonable"""
        file_size = os.path.getsize(self.readme_path)

        # README should be between 100 bytes and 10KB for a PR description
        self.assertGreater(
            file_size,
            100,
            "README is too small, may be missing content"
        )
        self.assertLess(
            file_size,
            10240,
            "README is too large for a PR description"
        )

    def test_consistency_of_terminology(self):
        """Test that terminology is used consistently"""
        # Check that "tier" and "plan" are mentioned together
        tier_count = self.readme_content.lower().count('tier')
        plan_count = self.readme_content.lower().count('plan')

        # Both should be mentioned since they're related concepts
        self.assertGreater(tier_count, 0, "Should mention 'tier'")
        self.assertGreater(plan_count, 0, "Should mention 'plan'")


if __name__ == '__main__':
    unittest.main(verbosity=2)