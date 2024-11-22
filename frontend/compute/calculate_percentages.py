@lru_cache(maxsize=128)
def calculate_percentages(self, total, frequencies):
    """Cache percentage calculations for better performance"""
    return [(freq / total) * 100 for freq in frequencies]