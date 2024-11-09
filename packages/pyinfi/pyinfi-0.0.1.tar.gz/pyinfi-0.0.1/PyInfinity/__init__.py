"""Framework PyInfinity.
Megagolab, 2024.

Special thanks:
    """

__version__ = '0.0.1'
__author__ = 'Matvei Kostenko'
__license__ = 'Use allowed with software mention only.'
__copyright__ = '© 2024 Matvei Kostenko. All rights reserved.'
__contributors__ = [
    'Matvei K. : Lead Developer',
    'Nikita M. : Helper',
    'Denis  G. : Helper'
]

def getContributors() -> str:
    """Return contributors."""
    return '\n'.join(__contributors__)

def getAuthor() -> str:
    """Return author."""
    return __author__

def getLicense() -> str:
    """Return license."""
    return __license__

def getCopyright() -> str:
    """Return copyright."""
    return __copyright__

def getVersion() -> str:
    """Return version."""
    return __version__