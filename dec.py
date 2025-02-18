import os

def decode_lua_data(encrypted_data):
    # header check
    if encrypted_data[:4] != b'abcd':
        raise ValueError("En-tête invalide")

    # Table 
    hex_table = b'0123456789abcdef'

    # key extraction
    key = 0
    for i in range(4):
        byte = encrypted_data[4 + i]
        high_nibble = hex_table[byte >> 4]  
        low_nibble = hex_table[byte & 0xF]  

        
        high_val = int(chr(high_nibble), 16)
        low_val = int(chr(low_nibble), 16)

        #here im bulding the key
        key = (key << 8) | (high_val << 4) | low_val

    # the game use a cyclic key 
    key -= 2048
    cyclic_key = [
        (key >> 24) & 0xFF,
        (key >> 16) & 0xFF,
        (key >> 8) & 0xFF,
        key & 0xFF
    ]

    # just a basic xor 
    decrypted_data = bytearray()
    for i in range(8, len(encrypted_data)):
        decrypted_byte = encrypted_data[i] ^ cyclic_key[(i - 8) % 4]
        decrypted_data.append(decrypted_byte)

    return decrypted_data

def decrypt_lua_file(input_path):
 
    with open(input_path, 'rb') as f:
        encrypted_data = f.read()

    try:
        decrypted_data = decode_lua_data(encrypted_data)
        
       
        output_path = input_path.replace('.lua64', '.lua')
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
    
        os.remove(input_path)
        print(f"File decrypted and removed : {output_path}")

    except ValueError as e:
        print(f"An error occured with {input_path}: {e}")

def delete_non_lua_files(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for file_name in files:
            if not file_name.endswith('.lua'):
                file_path = os.path.join(root, file_name)
                os.remove(file_path)
                print(f"Removed : {file_path}")

def decrypt_files_in_folder(folder_path):

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.lua64'): 
                input_file = os.path.join(root, file_name)
                decrypt_lua_file(input_file)

    delete_non_lua_files(folder_path)

folder_path = ''  # Remplace with your actual lua folder
decrypt_files_in_folder(folder_path)
