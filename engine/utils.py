def safe_div(a, b):
    return a / b if b != 0 else 0

def distance(a, b):
    return ((a.x - b.x)**2 + (a.y - b.y)**2)**0.5

def clamp_rect(rect, width, height):
    rect.x = max(0, min(rect.x, width - rect.width))
    rect.y = max(0, min(rect.y, height - rect.height))
    return rect