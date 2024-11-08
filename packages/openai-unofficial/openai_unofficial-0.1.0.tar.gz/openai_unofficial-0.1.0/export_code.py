import os
from pathlib import Path

def get_file_extension(file_path):
    """Get the file extension without the dot"""
    return os.path.splitext(file_path)[1][1:]

def create_code_block(content, file_extension):
    """Create a markdown code block with language specification"""
    return f"```{file_extension}\n{content}\n```\n\n"

def process_path(path, markdown_content):
    """Process a file or directory and return markdown content"""
    path = Path(path)
    
    if path.is_file():
        # Handle file
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
                extension = get_file_extension(path)
                markdown_content.append(f"## File: {path}\n\n")
                markdown_content.append(create_code_block(content, extension))
        except Exception as e:
            markdown_content.append(f"Error reading file {path}: {str(e)}\n\n")
    
    elif path.is_dir():
        # Handle directory
        markdown_content.append(f"# Directory: {path}\n\n")
        try:
            for item in path.iterdir():
                process_path(item, markdown_content)
        except Exception as e:
            markdown_content.append(f"Error accessing directory {path}: {str(e)}\n\n")
    
    return markdown_content

def create_markdown_documentation(input_paths, output_file):
    """Create markdown documentation from a list of paths"""
    markdown_content = []
    markdown_content.append("# Code Documentation\n\n")
    
    for path in input_paths:
        process_path(Path(path), markdown_content)
    
    # Write to markdown file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(''.join(markdown_content))
        print(f"Successfully created markdown documentation at {output_file}")
    except Exception as e:
        print(f"Error writing to output file: {str(e)}")

# Example usage
if __name__ == "__main__":
    # List of paths to process (can be files or directories)
    paths_to_process = [
        "LINENCE",
        "pyproject.toml",
        "CHANGELOG.md",
        "src",
        ".github"
    ]
    
    output_markdown_file = "directory_content.md"
    create_markdown_documentation(paths_to_process, output_markdown_file)