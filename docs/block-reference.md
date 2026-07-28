# PyMason Block Reference

**Product version:** 1.5.0  

Practical map of toolbox categories → common blocks → Python they generate. Hover any block in the app for a full tooltip with import notes. For exact generator output, place a block and use **right-click → Show Python**, or read the live code panel.

Use header **Show all** (or **Unlock all toolbox**) to see every category. **Core** mode hides advanced packs during assessments.

---

## Imports

| Block | Python |
|-------|--------|
| import *module* | `import os` |
| from *module* import *name* | `from os import path` |
| import *module* as *alias* | `import json as js` |

Dropdown presets include: `os`, `sys`, `math`, `random`, `json`, `datetime`, `re`, `collections`, `itertools`, `functools`, `pathlib`, `time`, `csv`, and more. Choose **custom…** for other module names.

Many stdlib blocks below **require** a matching import (tooltips say so). Pair with **Imports**.

## I/O

| Block | Python |
|-------|--------|
| print | `print(...)` |
| print (advanced) | `print(..., end=..., sep=...)` |
| input | `input("prompt")` |
| input + cast | `int(input(...))` etc. |
| comment | `# text` |
| open / read / write | file I/O statements |

## Variables & Assign

Built-in Blockly variable create / set / get → `x = ...` and `x`.

Also: augmented assign (`+=`, `-=`, …), multi-assign / unpack, `del`.

## Text

Literals, f-strings, multiline `"""..."""`, raw strings, `.split` / `.strip` / `.replace` / `.join` / `.format`, case transforms, `startswith`/`endswith`, `count`, `find`, padding, `isdigit`/`isalpha`/….

## Text+ (1.5)

| Block | Python shape |
|-------|----------------|
| partition / rpartition | `s.partition(sep)` |
| zfill | `s.zfill(n)` |
| removeprefix / removesuffix | `s.removeprefix(...)` |
| expandtabs | `s.expandtabs()` |
| translate (simple) | `s.translate(table)` |
| chr / ord | `chr(n)` / `ord(c)` |
| string × n | `s * n` |
| center | `s.center(width)` |
| f-string expr | `f"{expr:fmt}"` style sketch |

## Convert

`int`, `str`, `float`, `bool`, `list`, `None`, collection casts (`tuple`, `set`, `frozenset`, `dict`), `isinstance`, `type`, introspection helpers.

## Math

Numbers, arithmetic (`+ - * / **`), floor `//`, `abs`, `min`/`max`, `range`, `sum`, `len`, math module funcs/constants. (Some random helpers also live under **Random**.)

## Stats (1.5)

| Block | Python shape |
|-------|----------------|
| mean / median / mode / stdev | `statistics.mean(data)` … |
| floor / ceil | `math.floor` / `math.ceil` |
| sqrt / log / trig | `math.sqrt` / `log` / `sin`… |
| degrees / radians | conversion |
| clamp | nested `min`/`max` |

Requires: `import statistics` / `import math` as noted on tooltips.

## Logic

`if` / `elif` / `else`, comparisons, `and`/`or`/`not`, booleans, ternary `a if c else b`, `in`/`not in`, `is`/`is not`, `assert`, `pass`, `with`, `match`/`case`, walrus `:=`.

## Loops

`repeat`, `while`/`until`, `for range`, `for each`, `break`/`continue`, `for/else`, `while/else`, `enumerate`, `zip`, comprehensions, `sorted`/`reversed`/`any`/`all`/`map`/`filter`.

## Lists / Dicts / Sets / Tuples

Create, index, slice, mutate (append/insert/remove/pop/sort/…), dict get/set/keys/values/items/get-default/update/pop/setdefault, set ops, comprehensions, `sorted`/`reversed`/`any`/`all`/`map`/`filter`.

## Errors

`try/except`, `try/except Type as e`, `try/finally`, full try/else/finally, `raise`, bare `raise`.

## Time (1.4)

| Block | Python shape |
|-------|----------------|
| sleep | `time.sleep(s)` |
| time.time | `time.time()` |
| datetime.now | `datetime.datetime.now()` |
| strftime / strptime | format / parse |

## Random (1.4)

`seed`, `random()`, `randint`, `choice`, `sample`, `shuffle`, `uniform`.

## Path & OS (1.4)

`getcwd`, `listdir`, `os.path.join` / `exists` / `basename`, `makedirs`, `pathlib.Path`.

## Regex (1.4)

`re.search`, `re.match`, `re.findall`, `re.sub`, `re.split`.

## Bitwise (1.4)

`& | ^ << >>`, `~`, `pow`, `round`, `divmod`.

## Advanced (1.4)

getitem/setitem/delitem, bool ops, `is None`, hasattr/getattr, next/iter, copy/deepcopy, encode/decode, dict merge, list repeat, async for/with, `@staticmethod` / `@classmethod` / `@property`, breakpoint, repr/id/hash.

## Collections (1.5)

| Block | Python shape |
|-------|----------------|
| Counter | `Counter(seq)` |
| defaultdict | `defaultdict(list)` etc. |
| deque | `deque(seq)` |
| namedtuple | `namedtuple('Point', 'x y')` |
| heappush / heappop | `heapq.heappush` / `heappop` |
| bisect.insort | `bisect.insort(a, x)` |

Requires matching `collections` / `heapq` / `bisect` imports.

## Encode (1.5)

base64 encode/decode, JSON pretty + load/dump file, CSV reader/writerow, `urllib.parse.quote` / `parse_qs`, `hashlib` digest, `uuid.uuid4()`, `secrets` token.

## Itertools (1.5)

`chain`, `cycle`, `repeat`, `count`, `islice`, `product`, `combinations`, `permutations`, `groupby`, plus `functools.reduce` / `partial`.

## Web sketch (1.5) — teaching scaffold

**Intentional sketch category.** Browser Pyodide is not a full HTTP client stack.

| Block | Behavior |
|-------|----------|
| HTTP GET sketch | Emits `print("GET", url)  # sketch…` — replace with `requests` on desktop |
| urljoin | Real `urllib.parse.urljoin` shape |
| html.escape | Real escape helper shape |
| query build / User-Agent | Header / query string sketches |

Use for **API client career templates** and mental models, not production fetches inside the sandbox.

## Concurrency (1.5) — teaching scaffold

**Intentional sketch category.** Blocks emit real-shaped `threading` / `queue` / `asyncio` Python for reading and portfolio transfer. True multi-thread/async behavior in the browser runner is limited; prefer desktop CPython for real concurrency labs.

| Block | Python shape |
|-------|----------------|
| Thread | `threading.Thread(target=…)` |
| start / join | `.start()` / `.join()` |
| Queue / put / get | `queue.Queue`, `.put`, `.get` |
| asyncio.run / gather / sleep | `asyncio.run`, `gather`, `await asyncio.sleep` |

## Stage

Turtle forward/turn/goto/pen/color, plot list, stage text/circle/fill/clear — draw on the in-app Stage canvas.

## Tests

`assert` true / equal / raises — used with the **Tests** panel harness.

## Functions

Blockly procedures (define/call) plus **Func Tools**: `return`, `global`/`nonlocal`, `lambda`, decorator, `yield`/`yield from`, `async def`, `await`, starred `*`/`**`.

## Classes

`class` (+ parent), `__init__`, methods, `self` get/set/call, `super()`, instantiate, attribute/method access, dunder methods.

## File I/O & JSON

`open` / read / write / `with`; `json.dumps` / `json.loads` (and Encode-category file helpers).

## Pattern matching

`match` / `case` (Python 3.10+) — also under Advanced.

## Favorites

Custom category filled from blocks you star (runtime).

---

### Import reminder

Stdlib-flavored blocks generate **calls**, not automatic imports. Drag the matching **import** / **from import** block (or type Free Python imports) before Run.

### Counts (approx., v1.5.0)

~252 custom `py_*` block definitions, ~250 generators (mutator-only tuple helpers excluded), ~32 toolbox categories.
