# inputwhile

A simple but helpful package that allows you to create input while loops with different conditions.

## Explanation nobody cares about
Once, I was tired of writing:
```Python
value = input()
while not condition(value):
        value = input()
```
every time I wanted to check if a user entered the right value in a program.

So, I decided to make this package (my first one).
It has a bunch of functions with pre-defined condition functions, but you can make custom inputwhiles too.

## Installation
```
# Linux/macOS
python3 -m pip install inputwhile

# Windows
py -3 -m pip install inputwhile
```

## Quick examples
### Custom error messages
```Python
import inputwhile

# If input value is an empty string it will print "Enter your username:" again until input value is not empty
string = inputwhile.stringNotEmpty(
        "Enter your username:"
)

# If input value is an empty string it will print "You can't leave it empty. Please enter your username:" until input value is not empty.
string = inputwhile.stringNotEmpty(
        "Enter your username:",
        error_prompt="You can't leave it empty. Please enter your username:"
)

# error_prompt is optional, but is also in all package functions.
```
### Number inputwhiles
```Python
import inputwhile

integer = inputwhile.integer(
        "Enter a number:",
        error_prompt="Invalid number. Please enter a valid number:"
)

floatNumber = inputwhile.floatInput(
        "Enter a float:",
        min=0.0,
        max=1.0 # You can add ranges too.
)
```

### Custom types
```Python
import inputwhile
from myproject import BigInt

# Will request a value until it is parsable like: BigInt(value) and will return it with that type.
value = inputwhile.customTypeClass(
        "Enter the nuclear code:",
        typeClass=BigInt
)

```

### Boolean inputwhiles
```Python
import inputwhile

# Only matches "true" or "false"
boolean = inputwhile.boolean(
        "It is illegal to keep a guinea pig in Switzerland. True or false?:",
        "Prompt not recognized. Please enter 'true' or 'false':"
)

# Matches "true", "t", "yes", "y", "1", "si", "sí", "s" or "false", "f", "no", "n", "0", "nope" by default.
flexibleBoolean = inputwhile.booleanFlexible(
        "Do you want to continue? (y/n):",
        trueStrings={"continue"},
        falseStrings={"exit"},
        doUseCustomNDefaults=True # Makes trueStrings and falseStrings being added to the default ones instead of replacing them.
)

regexBoolean = inputwhile.booleanFlexibleRegex(
        "Do you like tacos?:",
        trueRegex=f"^(yes|true|you don't have an idea|definitely|yes,[\s]*[\w]+)$"
        falseRegex=f"^(no|definitely no|never|no,[\s]*[\w]+)$"
        error_prompt="Prompt not recognized. Try again:"
)
```

### Lists
```Python
import inputwhile

# List of strings
stringsList = inputwhile.listInput(
        "Enter the countries you have ever visited:",
        separator=",",
        error_prompt="Please, don't leave empty the input:",
        doStriptElements=True # Makes a element.strip() to every element in the list
)

# Can filter the list
from pathlib import Path
filteredList = inputwhile.listInput(
        "Enter the directories you want to scan:",
        separator=" ",
        error_prompt="Invalid directories. Please enter at least one directory:"
        filter_func=lambda x: Path(x).is_dir()
)

# Can map too
mappedList = inputwhile.listInput(
        "Enter the values of the Mexican peso per day in the last month:"
        error_prompt="Enter at least one value:"
        map_func=lambda x: int(x),
        filter_func=lambda x: inputwhile.utils.isParsable(x, int)
)

# Also sets available for unique values
setsToo = setInput(
        "Enter your social media urls:",
        separator=" ",
        error_prompt="Enter at least one url:"
        filter_func=lambda x: x.startswith("http")
)

# And of course regex
regexList = inputwhile.listRegex(
        "Enter your hobbies separated by commas:",
        regex_separator=r"[,]+",
        doStripElements=True
)

regexSet = inputwhile.setRegex(
        "Enter the file extensions you like the most:"
        regex_separator=r"[.,\s]+"
)
```

## Links
[Twitter](https://x.com/ElBenjas333)
[Github](https://github.com/Benjas333/inputwhile)
[PyPI](https://pypi.org/project/inputwhile/)
