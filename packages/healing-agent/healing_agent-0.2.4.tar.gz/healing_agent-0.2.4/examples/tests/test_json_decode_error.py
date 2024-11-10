import json
from unittest.mock import Mock
from healing_agent import healing_agent

# Mock JSON responses with various invalid formats
valid_json = '{"name": "John", "age": 30}'
missing_brace = '{"name": "John", "age": 30'
extra_comma = '{"name": "John", "age": 30,}'
invalid_quotes = "{'name': 'John', 'age': 30}"
invalid_json = 'not json at all'
unclosed_array = '[1,2,3'
null_json = None
empty_json = ''
invalid_boolean = '{"flag": True}'  # True should be lowercase true
trailing_chars = '{"name": "John"} extra stuff'

@healing_agent(AUTO_FIX=False)
def fetch_data(response_json):
    # Create a mock response object
    response = Mock()
    response.text = response_json
    
    # Attempt to parse the JSON
    data = json.loads(response.text)
    return data

def main():
    test_cases = [
        ("Valid JSON", valid_json),
        ("Missing Brace", missing_brace),
        ("Extra Comma", extra_comma), 
        ("Invalid Quotes", invalid_quotes),
        ("Invalid JSON", invalid_json),
        ("Unclosed Array", unclosed_array),
        ("Null JSON", null_json),
        ("Empty JSON", empty_json),
        ("Invalid Boolean", invalid_boolean),
        ("Trailing Characters", trailing_chars)
    ]

    for test_name, test_json in test_cases:
        print(f"\nTest Case - {test_name}:")
        try:
            result = fetch_data(test_json)
            print("Result:", result)
        except Exception as e:
            print("Error:", str(e))

if __name__ == "__main__":
    main()