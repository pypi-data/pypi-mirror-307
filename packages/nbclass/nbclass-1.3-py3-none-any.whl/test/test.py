# -*- coding: utf-8 -*-
"""
@ Created on 2024-09-04 15:48
---------
@summary: 
---------
@author: XiaoBai
"""

from nbclass import tools

import pyotp

key = '6ZKWQI4LZFBN27S7MHLYY5M3O3HZU4Z3'
totp = pyotp.TOTP(key)
print(totp.now())
"""
打包 python setup.py sdist bdist_wheel
发布 twine upload dist/*
pypi-AgEIcHlwaS5vcmcCJDU2MDQ3NDFmLTU3MGYtNGNmOS1iNmU2LWNlZjk5Yzc5MTlkMAACKlszLCI5YWZhZjA2NS1kYmIxLTQ3YzAtYmRlOC05ZmVhZjY3NWFiY2UiXQAABiDugVzbaZnLT5RvF_fPWklC7D4WMtGoBUSZnxICYz_2Rw  nbclass
pypi-AgEIcHlwaS5vcmcCJDQ2YTI4Y2MwLWY4NTQtNGViMy04M2FmLWE5ZDc1NTBjMDkwOAACKlszLCI5YWZhZjA2NS1kYmIxLTQ3YzAtYmRlOC05ZmVhZjY3NWFiY2UiXQAABiB-P4o-OTZY4NJAwa8kVLiDii7ZIbY9OJB_WHS9tNoSFA  geocoding
"""
