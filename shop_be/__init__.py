try:
    import pkg_resources

    __version__ = pkg_resources.get_distribution('shop_be').version

except Exception:
    __version__ = 'unknown'
