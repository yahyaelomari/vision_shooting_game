import math

def check_collision(shot_pos, shapes):
    """
    Check if a shot hits any shape.
    Returns the hit shape or None.
    """
    if not shot_pos:
        return None
        
    x, y = shot_pos
    
    # Iterate through shapes (reverse order to hit top-most first if overlapping)
    for shape in reversed(shapes):
        # Use simple distance check for all objects for now, as they are roughly circular/compact
        # Or check if they have a 'radius' or 'size'
        
        # All GameObjects have 'size' (diameter or width)
        radius = shape.size / 2
        dist = math.sqrt((x - shape.x)**2 + (y - shape.y)**2)
        
        if dist <= radius:
            return shape
            
    return None
