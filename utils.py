import json
from PIL import Image

def make_empty_grid(rows, cols):
    return [[{'plant': None} for _ in range(cols)] for _ in range(rows)]

def analyze_image(uploaded_file):
    # lightweight image analysis placeholder — returns a friendly suggestion.
    try:
        img = Image.open(uploaded_file)
        w,h = img.size
        # naive heuristic: if mostly green, likely healthy leaf; else maybe pest
        pixels = img.convert('RGB').getdata()
        greens = sum(1 for (r,g,b) in pixels if g > r and g > b)
        total = len(pixels)
        ratio = greens/total if total else 0
        if ratio > 0.35:
            return 'Leaf appears mostly green — likely healthy. Check for small brown spots and treat with neem spray if needed.'
        else:
            return 'Leaf has low green coverage — may indicate nutrient deficiency or pest damage. Consider soil test and local remedies.'
    except Exception as e:
        return f'Could not analyze image: {e}'

def rule_based_reply(prompt):
    p = prompt.lower()
    if 'pest' in p or 'hole' in p or 'yellow' in p:
        return 'Common pests: aphids, caterpillars, fungal infections. Try neem oil spray, manual removal, and ensure good airflow.'
    if 'fert' in p or 'nitrogen' in p or 'fertil' in p:
        return 'General fertilizer advice: use NPK balanced fertilizer; apply during active growth; organic compost improves soil long-term.'
    if 'season' in p or 'plant' in p:
        return 'Seasonal suggestion: plant quick-growing leafy greens in short rainy seasons; choose drought-tolerant varieties in hot months.'
    return 'For best results, describe the crop, symptoms, and local climate. You can also upload a photo in Urban mode for quick analysis.'

def save_layout_json(grid):
    # returns JSON string
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    layout = {'rows':rows,'cols':cols,'cells':grid}
    return json.dumps(layout, indent=2)
