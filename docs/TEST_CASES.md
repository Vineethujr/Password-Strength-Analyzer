# Test Case Matrix (30+)

Use synthetic inputs only.

| ID | Scenario | Synthetic input | Expected | Automated result |
|---:|---|---|---|---|
| TC01 | Empty | `""` | VERY WEAK / validation signal | PASS (pytest) |
| TC02 | One character | `A` | VERY WEAK | PASS (pytest) |
| TC03 | Short numeric | `1234` | VERY WEAK | PASS (pytest) |
| TC04 | Common password | `password` | VERY WEAK | PASS (pytest) |
| TC05 | Long repeated | `aaaaaaaaaaaaaaaa` | WEAK | PASS (pytest) |
| TC06 | Lowercase only | `simplelowercase` | Low diversity finding possible | PASS (pytest) |
| TC07 | Uppercase only | `SIMPLEUPPERCASE` | Low diversity finding possible | PASS (pytest) |
| TC08 | Numbers only | `83746291827364` | Sequence/low diversity signals | PASS (pytest) |
| TC09 | Symbols only | `!@#$%^&*()_+` | Diversity signal | PASS (pytest) |
| TC10 | Mixed | `Mosaic!River7Glass` | Higher score | PASS (pytest) |
| TC11 | Ascending numbers | `abcd1234xyz` | Sequence detected | PASS (pytest) |
| TC12 | Descending numbers | `9876Alpha` | Sequence detected | PASS (pytest) |
| TC13 | Ascending letters | `abcdRIVER!` | Sequence detected | PASS (pytest) |
| TC14 | Keyboard | `qwertyZX9` | Keyboard detected | PASS (pytest) |
| TC15 | Repeated chars | `AAAAAA123!` | Repetition detected | PASS (pytest) |
| TC16 | Repeated substring | `abcabcabc!` | Repetition detected | PASS (pytest) |
| TC17 | Word + number | `welcome123` | Dictionary/predictable structure | PASS (pytest) |
| TC18 | Word + year | `summer2026!` | Predictable structure | PASS (pytest) |
| TC19 | Personal name | `Rahul@123456789` | Name overlap | PASS (pytest) |
| TC20 | Birth year | `BlueRiver2001!` | Year overlap | PASS (pytest) |
| TC21 | Long passphrase | `velvet-galaxy-harbor-orchid-raven-meadow` | Very strong in project heuristic | PASS (pytest) |
| TC22 | Unicode | `Δελτα-رود-森林-7!` | Unicode accepted | PASS (pytest) |
| TC23 | Spaces | `velvet galaxy harbor orchid` | Spaces accepted | PASS (pytest) |
| TC24 | Max length | `A` × 128 | Accepted | PASS (pytest) |
| TC25 | Score boundary | 0/20/21/40/41/60/61/80/81/100 | Correct classification bands | PASS (pytest) |
| TC26 | Suggestion generation | `qwerty123` | Actionable tips | PASS (pytest) |
| TC27 | Complex generator | generated 20 chars | Required character sets present | PASS (pytest) |
| TC28 | Passphrase generator | 6 generated words | 6 words returned | PASS (pytest) |
| TC29 | DB privacy | synthetic secret | No password column | PASS (pytest) |
| TC30 | Log privacy | synthetic secret | Secret absent from logs | PASS (pytest) |
| TC31 | API privacy | synthetic secret | Secret absent from response | PASS (pytest) |
| TC32 | Local breach | `123456` | Demo breach flag | PASS (pytest) |
| TC33 | Policy separation | long predictable demo | score and policy returned separately | PASS (pytest) |
| TC34 | Schema contract | DB schema | no password column | PASS (pytest) |
