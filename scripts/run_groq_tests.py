import httpx
import os

URL = os.getenv("TEST_URL", "http://127.0.0.1:8002/chat")
messages = [
    "Hello",
    "Hola, ¿cómo estás?",
    "안녕하세요, 잘 지내세요?",
]

def main():
    for m in messages:
        try:
            r = httpx.post(URL, json={"message": m}, timeout=60.0)
            print("MESSAGE:", m)
            print("STATUS:", r.status_code)
            print("BODY:", r.text)
            print("---")
        except Exception as e:
            print("EXCEPTION for message:", m)
            print(e)

if __name__ == '__main__':
    main()
