import inputwhile

if __name__ == "__main__":
        r = inputwhile.listRegex(
                "Enter a list separated by commas:",
                error_prompt="Invalid input. Please enter a list:",
                doStripElements=True
        )
        # r = inputwhile.integerInput(
        #         prompt="Enter an integer between 1 and 100:",
        #         min=1,
        #         max=100,
        # )
        print(r)
