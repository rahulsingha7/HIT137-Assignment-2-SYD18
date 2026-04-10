def shift_lowercase_encrypt(ch, shift1, shift2):
    if 'a' <= ch <= 'm':
        shift = shift1 * shift2
        return chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
    elif 'n' <= ch <= 'z':
        shift = shift1 + shift2
        return chr((ord(ch) - ord('a') - shift) % 26 + ord('a'))
    return ch


def shift_uppercase_encrypt(ch, shift1, shift2):
    if 'A' <= ch <= 'M':
        shift = shift1
        return chr((ord(ch) - ord('A') - shift) % 26 + ord('A'))
    elif 'N' <= ch <= 'Z':
        shift = shift2 ** 2
        return chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
    return ch


def shift_lowercase_decrypt(ch, shift1, shift2):
    pass


def shift_uppercase_decrypt(ch, shift1, shift2):
    pass


def encrypt_text(text, shift1, shift2):
    pass


def decrypt_text(text, shift1, shift2):
    pass


def read_file(filename):
    pass


def write_file(filename, content):
    pass


def verify_files(original_file, decrypted_file):
    pass


def main():
    pass


if __name__ == "__main__":
    main()