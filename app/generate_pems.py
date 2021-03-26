from eeManager import write_keys_to_file, generate_private_public_keys
import os


def main():
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    new_dir = "secrets"
    path = os.path.join(parent_dir, new_dir)

    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)
        write_keys_to_file(path=path, private_key_name='private_key.pem', public_key_name='public_key.pem')
    else:
        write_keys_to_file(path=path, private_key_name='private_key.pem', public_key_name='public_key.pem')


if __name__ == "__main__":
    main()
