from app.main import run_trace

if __name__ == "__main__":
    data = input("Enter email or phone: ")
    input_type = "email" if "@" in data else "phone"
    result = run_trace(input_type, data)
    print(result)
