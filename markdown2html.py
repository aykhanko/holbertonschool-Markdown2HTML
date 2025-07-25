#!/usr/bin/python3
"""Converts a Markdown file to an HTML file."""

import sys
import os
import re
import hashlib


def validate_arguments():
    """Validate command-line arguments and input file existence."""
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(input_path):
        print(f"Missing {input_path}", file=sys.stderr)
        sys.exit(1)

    return input_path, output_path


def apply_inline_formatting(text):
    """Apply inline Markdown formatting: bold, italic, md5, remove 'c' or 'C'."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)       # Bold
    text = re.sub(r'__(.+?)__', r'<em>\1</em>', text)         # Italic

    text = re.sub(r'\[\[(.+?)\]\]', lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), text)

    text = re.sub(r'\(\((.+?)\)\)', lambda m: re.sub(r'[cC]', '', m.group(1)), text)

    return text


def parse_heading(line):
    """Parse Markdown heading (#) line and return HTML string."""
    level = len(line) - len(line.lstrip('#'))
    if 1 <= level <= 6 and line[level:level+1] == ' ':
        content = apply_inline_formatting(line[level+1:].strip())
        return f"<h{level}>{content}</h{level}>"
    return None


def parse_unordered(line, state):
    """Handle unordered list items starting with '- '."""
    if line.startswith("- "):
        if not state["in_ul"]:
            state["buffer"].append("<ul>")
            state["in_ul"] = True
        content = apply_inline_formatting(line[2:].strip())
        state["buffer"].append(f"<li>{content}</li>")
        return True
    elif state["in_ul"]:
        state["buffer"].append("</ul>")
        state["in_ul"] = False
    return False


def parse_ordered(line, state):
    """Handle ordered list items starting with '* '."""
    if line.startswith("* "):
        if not state["in_ol"]:
            state["buffer"].append("<ol>")
            state["in_ol"] = True
        content = apply_inline_formatting(line[2:].strip())
        state["buffer"].append(f"<li>{content}</li>")
        return True
    elif state["in_ol"]:
        state["buffer"].append("</ol>")
        state["in_ol"] = False
    return False


def parse_paragraph(line, state):
    """Collect paragraph lines to group later."""
    state["paragraph_lines"].append(line)
    return True


def close_open_blocks(state):
    """Close any open list or paragraph blocks."""
    if state["in_ul"]:
        state["buffer"].append("</ul>")
        state["in_ul"] = False
    if state["in_ol"]:
        state["buffer"].append("</ol>")
        state["in_ol"] = False
    if state["paragraph_lines"]:
        formatted_lines = [apply_inline_formatting(line.strip()) for line in state["paragraph_lines"]]
        joined = "<br/>\n    ".join(formatted_lines)
        state["buffer"].append(f"<p>\n    {joined}\n</p>")
        state["paragraph_lines"] = []


def parse_line(line, state):
    """Parse a single line of Markdown and append corresponding HTML."""
    stripped = line.strip()

    if not stripped:
        close_open_blocks(state)
        return

    heading = parse_heading(stripped)
    if heading:
        close_open_blocks(state)
        state["buffer"].append(heading)
        return

    if parse_unordered(stripped, state) or parse_ordered(stripped, state):
        close_open_blocks(state)
        return

    parse_paragraph(stripped, state)


def convert_markdown(input_path, output_path):
    """Main conversion function from Markdown to HTML."""
    state = {
        "in_ul": False,
        "in_ol": False,
        "paragraph_lines": [],
        "buffer": []
    }

    with open(input_path, 'r', encoding='utf-8') as md_file:
        for line in md_file:
            parse_line(line, state)

    close_open_blocks(state)

    with open(output_path, 'w', encoding='utf-8') as html_file:
        html_file.write('\n'.join(state["buffer"]) + '\n')


if __name__ == "__main__":
    input_path, output_path = validate_arguments()
    convert_markdown(input_path, output_path)
