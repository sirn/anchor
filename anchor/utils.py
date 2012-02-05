def rensure(items, count):
    """Make sure there are `count` number of items in the list otherwise
    just fill in `None` from the beginning until it reaches `count` items."""
    fills = count - len(items)
    if fills >= 1:
        return [None] * fills + items
    return items

def rrsplit(string, separator=None, maxsplit=-1):
    """Works just like rsplit but always return `maxsplit+1` items."""
    return rensure(string.rsplit(separator, maxsplit), maxsplit+1)
