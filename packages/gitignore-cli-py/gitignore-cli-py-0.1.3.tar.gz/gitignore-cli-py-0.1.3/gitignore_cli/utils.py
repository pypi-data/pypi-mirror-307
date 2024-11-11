import os


def list_available_templates(template_dir=None):
    """Lists all .gitignore templates available in the given templates directory."""
    if template_dir is None:
        template_dir = os.path.join(os.path.dirname(__file__), 'gitignore', 'templates')

    templates = []
    if os.path.exists(template_dir):
        for file in os.listdir(template_dir):
            if file.endswith(".gitignore"):
                templates.append(os.path.splitext(file)[0])

    return sorted(templates)
