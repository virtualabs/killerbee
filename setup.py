# NOTE: See the README file for a list of dependencies to install.

from __future__ import print_function
import sys

try:
    from setuptools import setup, Extension
except ImportError:
    print("No setuptools found, attempting to use distutils instead.")
    from distutils.core import setup, Extension

# These dependency checks are advisory only. The runtime requirements are
# declared in install_requires below and installed by pip. Previously this
# script called sys.exit(1) when pyusb was missing, which breaks installation
# under PEP 517 build isolation (e.g. `pip install .`), where runtime deps are
# not present in the isolated build environment. We now only print hints and
# never abort the build.
warn = []
pip_pkgs = []

# pyUSB 1.x is preferred going forward.
try:
    import usb.core  # noqa: F401
except ImportError:
    warn.append("pyusb (1.x preferred) - needed at runtime to talk to USB radios")
    pip_pkgs.append("pyusb")

# TODO: Ideally we would detect missing python-dev and libgcrypt-dev to give better errors.

# Dot15d4 is a dep of some of the newer tools
try:
    from scapy.all import Dot15d4  # noqa: F401
except ImportError:
    warn.append("Scapy (with dot15d4 layer)")
    pip_pkgs.append("scapy")

if len(warn) > 0:
    print("""
Library recommendations not met. pip will install the runtime requirements
listed in install_requires; the following are noted for reference:

{}\n""".format('\n'.join(warn)), file=sys.stderr)
    if len(pip_pkgs) > 0:
        print("\tpip3 install {}".format(' '.join(pip_pkgs)), file=sys.stderr)

zigbee_crypt = Extension('zigbee_crypt',
                         sources = ['zigbee_crypt/zigbee_crypt.c'],
                         libraries = ['gcrypt'],
                         include_dirs = ['/usr/local/include', '/usr/include', '/sw/include/', 'zigbee_crypt'],
                         library_dirs = ['/usr/local/lib', '/usr/lib','/sw/var/lib/']
                         )

setup(name        = 'killerbee',
      version     = '3.0.0-beta.2',
      description = 'ZigBee and IEEE 802.15.4 Attack Framework and Tools',
      author = 'Joshua Wright, Ryan Speers',
      author_email = 'jwright@willhackforsushi.com, ryan@riverloopsecurity.com',
      license   = 'LICENSE.txt',
      packages  = ['killerbee'],
      scripts = ['tools/zbdump', 'tools/zbgoodfind', 'tools/zbid', 'tools/zbreplay',
                 'tools/zbconvert', 'tools/zbdsniff', 'tools/zbstumbler', 'tools/zbassocflood',
                 'tools/zbscapy', 'tools/zbwireshark', 'tools/zbkey',
                 'tools/zbwardrive', 'tools/zbopenear', 'tools/zbfakebeacon',
                 'tools/zborphannotify', 'tools/zbpanidconflictflood', 'tools/zbrealign', 'tools/zbcat',
                 'tools/zbjammer', 'tools/kbbootloader'],
      install_requires=['pyserial>=2.0', 'pyusb', 'pycryptodome', 'rangeparser', 'scapy'],
      # NOTE: pygtk doesn't install via distutils on non-Windows hosts
      ext_modules = [zigbee_crypt],
      )
