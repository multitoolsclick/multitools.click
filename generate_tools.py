import json
import os
from collections import defaultdict

# load data
with open("tools-data.json") as f:
    tools = json.load(f)

# load template
with open("template.html") as f:
    template = f.read()

# create category grouping
categories = defaultdict(list)

for tool in tools:
    categories[tool["category"]].append(tool)

# ensure tools folder exists
os.makedirs("tools", exist_ok=True)

for category, items in categories.items():

    category_path = f"tools/{category}"
    os.makedirs(category_path, exist_ok=True)

    for tool in items:

        related_html = ""

        for related in items[:5]:
            related_html += f'<li><a href="/tools/{category}/{related["slug"]}.html">{related["name"]}</a></li>'

        html = template.replace("{tool_name}", tool["name"])
        html = html.replace("{description}", tool["description"])
        html = html.replace("{related_tools}", related_html)

        filename = f"{category_path}/{tool['slug']}.html"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)

        print("Created:", filename)

# create category index pages
for category, items in categories.items():

    links = ""

    for tool in items:
        links += f'<li><a href="/tools/{category}/{tool["slug"]}.html">{tool["name"]}</a></li>'

    category_page = f"""
<!DOCTYPE html>
<html>
<head>
<title>{category.title()} Tools - Multitools.click</title>
</head>
<body>

<h1>{category.title()} Tools</h1>

<ul>
{links}
</ul>

<a href="/">Back to Home</a>

</body>
</html>
"""

    with open(f"tools/{category}/index.html", "w") as f:
        f.write(category_page)

    print("Created category page:", category)