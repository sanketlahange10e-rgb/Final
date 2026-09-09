import random

def traffic_randomizer(edge_length, min_length=50, max_length=500, inflation_factor=2.0):
    """
    Simulate traffic by returning a traffic multiplier for a road segment.
    Args:
        edge_length (float): Length of the road segment (meters).
        min_length (float): Minimum length (meters) to consider as 'small'.
        max_length (float): Maximum length (meters) for inflation effect.
        inflation_factor (float): Maximum multiplier for traffic on smallest roads.
    Returns:
    inflation_factor = 1.2
    """
    if edge_length <= min_length:
        
        return inflation_factor * random.uniform(1.1, 1.5)
    elif edge_length < max_length:
     
        scale = (max_length - edge_length) / (max_length - min_length)
        factor = 1.0 + (inflation_factor - 1.0) * scale * random.uniform(1.0, 1.3)
        return factor
    else:

        return random.uniform(0.95, 1.05)