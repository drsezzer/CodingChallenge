
Results


| Name (*) | Exception (a) | Exception (b) | b1 result | b2 result | b3 result | c4 result | d0 result | attempts | bugs/comments |
|----------|-----|---|----------|----------|----|---|---|---|---|
| Star Trek's Dr Beverly Crusher           |   |   |   |   |   |   |   | 1 |
| The Big Bang Theory's Penny              |   |   |   |   |   |   |   | 1 |
| Bill Gates                               | 1 |   |   |   |   |   |   | 2 |
| The Big Bang Theory's Raj Koothrappali   | 1 |   |   |   |   |   |   | 2 |
| Star Trek's Deanna Troi                  |   | 1 |   |   |   |   |   | 2 |
| Sherlock Holmes                          | 1 | 1 |   |   |   |   |   | 4 |
| Star Trek's Will Riker                   | 1 | 1 |   | 1 |   |   |   | 4 |
| The Big Bang Theory's Leonard Hofstadter | 2 |   |   |   | 1 |   |   | 4 | 
| The Big Bang Theory's Howard Wolowitz    | 2 |   |   |   |   | 1 |   | 4 |
| Star Trek's Wesley Crusher               | 1 | 2 |   | 1 |   |   |   | 5 |
| The Big Bang Tehory's Amy Farray Fowler  | 2 |   |   | 1 |   | 1 |   | 5 | 2nd attempt this time using gpt4o this used gpt4o. |
| Dame Judy Dench                          |   | 1 | 1 | 4 |   |   |   | 7 |
| Jean Luc Picard                          | 1 | 1 |   | 1 |   |   |   | 7 | Bug: Missing variable (param) |
| The Big Bang Theory's Sheldon Cooper     |   |   |   | 6 |   |   | 1 | 8 | Used networkx package, asked and used debug feedback. |
| Star Trek's Commander Data               | 2 | 3 |   | 5 |   |   |   | 11 |

(*) exactly as given in the prompt.

(a) Dictionary Changed exception, redirect = this code throws a Dictionary Changed exception

(b) Dictionary Changed exception, redirect = this code throws a Dictionary Changed exception at line 'for ...