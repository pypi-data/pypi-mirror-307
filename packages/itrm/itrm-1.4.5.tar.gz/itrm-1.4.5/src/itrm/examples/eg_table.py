"""
This example shows how tables look with ASCII characters and then again with
Unicode characters. See figures/eg_table.png.
"""

import numpy as np
import itrm

x = np.random.rand(5, 3)
names = ['apples', 'bananas', 'pears', 'oranges', 'grapes']
headers = ['Set 1', 'Set 2', 'Set 3']
itrm.table(x, left=names, head=headers, uni=False)
print()
itrm.table(x, left=names, head=headers, uni=True)
