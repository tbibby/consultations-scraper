import re
# this script goes through a collection of public consultation html from Cork County Council
# and tries to extract dates from them
# used for testing some hoary date regexps

# Define the patterns for full month names, abbreviated month names, and date formats
date_patterns = re.compile(
    r'(?<!\w)(January|February|March|April|May|June|July|August|September|October|November|December|'  # Full month names
    r'Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(?!\w)|'  # Abbreviated month names
    r'(?<!\w)(\d{1,2}/\d{1,2}/\d{2,4}|\d{1,2}/\d{1,2}/\d{4})(?!\w)'  # Date in dd/mm/yy or dd/mm/yyyy format
)

# Open the file and read its content
with open('cork-county-fragments.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Split the content by the separator
sections = content.split('-----')
counter = 0

# Loop through each section
for section in sections:
    counter += 1
    print(f"*** Section {counter} ***")
    
    # Find all matches in the section
    matches = date_patterns.finditer(section)
    
    for match in matches:
        start = match.start()
        end = match.end()
        
        # Get the surrounding text
        surrounding_text = section[max(0, start - 20):min(len(section), end + 20)]
        # Surround the matched text with ^
        highlighted_text = (surrounding_text[:start - max(0, start - 20)] + '^' + match.group() + '^' + surrounding_text[end - max(0, start - 20):])
        print(f"§ {highlighted_text}\n")
