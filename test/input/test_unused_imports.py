import unitest.mock.patch, unittest.mock.patch as p1
import unitest.mock.patch, unittest.mock.patch as p2
import unittest as t, unittest as t2
import unitest.mock.patch as p
import os
import pandas as pd, numpy as np
from collections.abc import defaultdict, OrderedDict
from itertools import filterfalse as _filterfalse
from collections.abc import x, y

p2.mock() # use p2
t.mock() # use t
y.mock() # use y


test_unused_imports.py:1: [C0410(multiple-imports), ] Multiple imports on one line (unitest.mock.patch, unittest.mock.patch)
test_unused_imports.py:1: [E0401(import-error), ] Unable to import 'unitest.mock.patch'
test_unused_imports.py:1: [E0401(import-error), ] Unable to import 'unittest.mock.patch'
test_unused_imports.py:2: [W0404(reimported), ] Reimport 'unitest.mock.patch' (imported line 1)
test_unused_imports.py:2: [W0404(reimported), ] Reimport 'unittest.mock.patch' (imported line 1)
test_unused_imports.py:2: [C0410(multiple-imports), ] Multiple imports on one line (unitest.mock.patch, unittest.mock.patch)
test_unused_imports.py:2: [E0401(import-error), ] Unable to import 'unitest.mock.patch'
test_unused_imports.py:2: [E0401(import-error), ] Unable to import 'unittest.mock.patch'
test_unused_imports.py:3: [C0410(multiple-imports), ] Multiple imports on one line (unittest, unittest)
test_unused_imports.py:4: [W0404(reimported), ] Reimport 'unitest.mock.patch' (imported line 1)
test_unused_imports.py:4: [E0401(import-error), ] Unable to import 'unitest.mock.patch'
test_unused_imports.py:6: [C0410(multiple-imports), ] Multiple imports on one line (pandas, numpy)
test_unused_imports.py:7: [E0611(no-name-in-module), ] No name 'defaultdict' in module 'collections.abc'
test_unused_imports.py:7: [E0611(no-name-in-module), ] No name 'OrderedDict' in module 'collections.abc'
test_unused_imports.py:9: [E0611(no-name-in-module), ] No name 'x' in module 'collections.abc'
test_unused_imports.py:9: [E0611(no-name-in-module), ] No name 'y' in module 'collections.abc'
test_unused_imports.py:1: [W0611(unused-import), ] Unused import unitest.mock.patch
test_unused_imports.py:1: [W0611(unused-import), ] Unused unittest.mock.patch imported as p1
test_unused_imports.py:3: [W0611(unused-import), ] Unused unittest imported as t
test_unused_imports.py:5: [W0611(unused-import), ] Unused import os
test_unused_imports.py:6: [W0611(unused-import), ] Unused pandas imported as pd
test_unused_imports.py:6: [W0611(unused-import), ] Unused numpy imported as np
test_unused_imports.py:7: [W0611(unused-import), ] Unused defaultdict imported from collections.abc
test_unused_imports.py:7: [W0611(unused-import), ] Unused OrderedDict imported from collections.abc
test_unused_imports.py:8: [W0611(unused-import), ] Unused filterfalse imported from itertools as _filterfalse
test_unused_imports.py:9: [W0611(unused-import), ] Unused x imported from collections.abc
test_unused_imports.py:3: [C0411(wrong-import-order), ] standard import "import unittest as t, unittest as t2" should be placed before "import unitest.mock.patch, unittest.mock.patch as p1"
test_unused_imports.py:3: [C0411(wrong-import-order), ] standard import "import unittest as t, unittest as t2" should be placed before "import unitest.mock.patch, unittest.mock.patch as p1"
test_unused_imports.py:5: [C0411(wrong-import-order), ] standard import "import os" should be placed before "import unitest.mock.patch, unittest.mock.patch as p1"
test_unused_imports.py:6: [C0411(wrong-import-order), ] third party import "import pandas as pd, numpy as np" should be placed before "import unitest.mock.patch, unittest.mock.patch as p1"
test_unused_imports.py:6: [C0411(wrong-import-order), ] third party import "import pandas as pd, numpy as np" should be placed before "import unitest.mock.patch, unittest.mock.patch as p1"
test_unused_imports.py:7: [C0411(wrong-import-order), ] standard import "from collections.abc import defaultdict, OrderedDict" should be placed before "import pandas as pd, numpy as np"
test_unused_imports.py:8: [C0411(wrong-import-order), ] standard import "from itertools import filterfalse as _filterfalse" should be placed before "import pandas as pd, numpy as np"
test_unused_imports.py:9: [C0411(wrong-import-order), ] standard import "from collections.abc import x, y" should be placed before "import pandas as pd, numpy as np"
test_unused_imports.py:9: [C0412(ungrouped-imports), ] Imports from package collections are not grouped
