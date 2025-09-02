# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring,
# pylint: disable=missing-module-docstring
# pylint: disable=broad-exception-caught
# pylint: disable=missing-class-docstring

def extract_json(json_str: str) -> str | None:
    start = json_str.find('{')
    if start == -1:
        return None
    count = 0
    for i, ch in enumerate(json_str[start:], start=start):
        if ch == '{':
            count += 1
        elif ch == '}':
            count -= 1
            if count == 0:
                return json_str[start:i+1]
    return None


if __name__ == "__main__":
    text = " ```json \n \
      { \n \
      \"action\": 0, \n \
      \"reason\": \"My hand is not strong enough to bid for the landlord role. I have several broken sequences and pairs, no bombs, and only one 2. Becoming the landlord with this hand would be very risky.\" \n \
      } \n \
      ``` "
    print(extract_json(text))
