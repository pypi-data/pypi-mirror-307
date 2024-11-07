"""
    Set up icecream for an application.
    This will need to be called before other modules if
    'ic()' is used at the module level.

    Usage:

        from icecream_init import ic_init
        ic_init()

"""


def ic_init():
    try:
        from icecream import ic, install
        ic.configureOutput(includeContext=True)
        install()

    except ImportError:  # Graceful fallback if IceCream isn't installed.
        def get_ic(*args):
            if not args:
                return None
            if len(args) == 1:
                return args[0]
            return args
        # ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)
        ic = get_ic()
