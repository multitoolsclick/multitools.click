import json
import os
from collections import defaultdict

# Load data
with open("tools-data.json") as f:
    tools = json.load(f)

# Load templates
with open("template.html") as f:
    tool_template = f.read()
with open("template_index.html") as f:
    index_template = f.read()

# Organize by category
categories = defaultdict(list)
for tool in tools:
    categories[tool["category"]].append(tool)

# 1. Generate Tool Pages (The Fix)
os.makedirs("tools", exist_ok=True)
for tool in tools:
    # Create specific paths based on category
    category_path = f"tools/{tool['category']}"
    os.makedirs(category_path, exist_ok=True)
    
    # Generate related tools list for SEO internal linking
    related_html = ""
    for related in categories[tool['category']][:5]: # Top 5 related
        if related['slug'] != tool['slug']:
            related_html += f'<li><a href="/{category_path}/{related["slug"]}.html">{related["name"]}</a></li>\n'

    html = tool_template.replace("{tool_name}", tool["name"])
    html = html.replace("{description}", tool["description"])
    html = html.replace("{related_tools}", related_html)
    
    # Important: Add the specific JS/Logic placeholder
    # html = html.replace("{tool_logic}", tool.get("logic_code", "")) 

    with open(f"{category_path}/{tool['slug']}.html", "w", encoding="utf-8") as f:
        f.write(html)

# 2. Generate Homepage (The Automation)
category_html = ""
for cat, items in categories.items():
    links = ""
    for item in items:
        # Correct relative path
        links += f'<li><a href="tools/{cat}/{item["slug"]}.html">{item["name"]}</a></li>\n'
    category_html += f"<h2>{cat.title()}</h2><ul>{links}</ul>"

index_html = index_template.replace("{categories_block}", category_html)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

print("Site generated successfully.")
