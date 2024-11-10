import inputwhile
from pathlib import Path

if __name__ == "__main__":
        # r = inputwhile.listRegex(
        #         "Enter a list separated by commas:",
        #         error_prompt="Invalid input. Please enter a list:",
        #         doStripElements=True
        # )
        r:Path = inputwhile.customFunction(
                prompt="Enter the full path to the directory to analyze:",
                error_prompt=f"Invalid directory. Please enter a valid directory:",
                condition_func=lambda x: Path(x) if x != '' and Path(x).is_dir() else None,
                returnValueFromConditionFunc=True
        )
        # r = inputwhile.integerInput(
        #         prompt="Enter an integer between 1 and 100:",
        #         min=1,
        #         max=100,
        # )
        print(r.parent)
