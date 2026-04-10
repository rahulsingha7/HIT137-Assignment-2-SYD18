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
    if 'a' <= ch <= 'm':
        shift = shift1 * shift2
        return chr((ord(ch) - ord('a') - shift) % 26 + ord('a'))
    elif 'n' <= ch <= 'z':
        shift = shift1 + shift2
        return chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
    return ch


def shift_uppercase_decrypt(ch, shift1, shift2):
    if 'A' <= ch <= 'M':
        shift = shift1
        return chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
    elif 'N' <= ch <= 'Z':
        shift = shift2 ** 2
        return chr((ord(ch) - ord('A') - shift) % 26 + ord('A'))
    return ch


def encrypt_text(text, shift1, shift2):
    encrypted = []

    for ch in text:
        if ch.islower():
            encrypted.append(shift_lowercase_encrypt(ch, shift1, shift2))
        elif ch.isupper():
            encrypted.append(shift_uppercase_encrypt(ch, shift1, shift2))
        else:
            encrypted.append(ch)

    return ''.join(encrypted)


def decrypt_text(text, shift1, shift2):
    decrypted = []

    for ch in text:
        if ch.islower():
            decrypted.append(shift_lowercase_decrypt(ch, shift1, shift2))
        elif ch.isupper():
            decrypted.append(shift_uppercase_decrypt(ch, shift1, shift2))
        else:
            decrypted.append(ch)

    return ''.join(decrypted)


def read_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def write_file(filename, content):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)


def verify_files(original_file, decrypted_file):
    original_text = read_file(original_file)
    decrypted_text = read_file(decrypted_file)
    return original_text == decrypted_text


def main():
    try:
        shift1 = int(input("Enter shift1: "))
        shift2 = int(input("Enter shift2: "))

        raw_text = read_file("raw_text.txt")

        encrypted_text = encrypt_text(raw_text, shift1, shift2)
        write_file("encrypted_text.txt", encrypted_text)

        decrypted_text = decrypt_text(encrypted_text, shift1, shift2)
        write_file("decrypted_text.txt", decrypted_text)

        if verify_files("raw_text.txt", "decrypted_text.txt"):
            print("Verification successful: decryption matches the original text.")
        else:
            print("Verification failed: decryption does not match the original text.")

    except FileNotFoundError:
        print("Error: raw_text.txt was not found.")
    except ValueError:
        print("Error: shift1 and shift2 must be integers.")


if __name__ == "__main__":
    main()