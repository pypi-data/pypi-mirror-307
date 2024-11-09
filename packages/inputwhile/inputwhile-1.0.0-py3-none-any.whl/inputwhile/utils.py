from typing import Type, Any

def isParsable(
        variable: Any,
        classType: Type[Any]
) -> bool:
        try:
                classType(variable)
                return True
        except ValueError:
                return False
