from pathlib import Path


def execute_return_rsa():
    this_dir = Path(__file__).parent
    with open(this_dir/'secrets/public_key.pem', "rb") as key_file:
        public_key = key_file.read()

    return public_key


if __name__ == "__main__":
    print(execute_return_rsa())
