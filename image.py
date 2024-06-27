import os
import time
import json
import random
from PIL import Image
import numpy as np

def en_mode_m1(img_path, output_img_name, key):
    with Image.open(img_path) as img:
        img = img.convert("RGB")
        pixels = img.load()

        for i in range(img.width):
            for j in range(img.height):
                r, g, b = pixels[i, j]
                r = r ^ key
                g = g ^ key
                b = b ^ key
                pixels[i, j] = (r, g, b)
        img.save(output_img_name)

def en_mode_m2(img_path, output_image_name, key):
    with Image.open(img_path) as img:
        img = img.convert("RGB")
        np_img = np.array(img)
        
        np_img = np_img ^ key

        encrypted_img = Image.fromarray(np_img)
        encrypted_img.save(output_image_name)

def dc_mode_1(img_path, output_image_name, key):
    with Image.open(img_path) as img:
        img = img.convert("RGB")
        pixels = img.load()
        
        for i in range(img.width):
            for j in range(img.height):
                r, g, b = pixels[i, j]
                # Apply decryption using XOR with the key
                r = r ^ key
                g = g ^ key
                b = b ^ key
                pixels[i, j] = (r, g, b)
        img.save(output_image_name)

def dc_mode_2(img_path, output_image_name, key):
    with Image.open(img_path) as img:
        img = img.convert("RGB")
        np_img = np.array(img)
        
        np_img = np_img ^ key

        decrypted_img = Image.fromarray(np_img)
        decrypted_img.save(output_image_name)

def generate_enc_key():
    key = random.randint(0, 255)
    return key

def save_enc_key(key, key_path):
    with open(key_path, 'w') as key_file:
        json.dump(key, key_file)

def load_enc_key(key_path):
    with open(key_path, 'r') as key_file:
        key = json.load(key_file)
    return key

def reset_function():
    for _ in range(5):
        print(".", end="", flush=True)
        time.sleep(0.5)

def check_img_extension(img_path):
    valid_extensions = ('.png', '.jpg', '.jpeg')
    return img_path.lower().endswith(valid_extensions)

def check_enc_key_extension(key_path):
    extension = 'json'
    return key_path.lower().endswith(extension)

def encrypt(img_path, en_mode):
    while True:
        if len(img_path) == 0 or len(en_mode) == 0:
            print("\nERROR: Empty fields detected. Resetting")
            reset_function()
            break
        if en_mode != 'm2' and en_mode != 'm1':
            print("\nERROR: Only m1 and m2 modes are supported.")
            reset_function()
            break
        if not check_img_extension(img_path):
            print("\nERROR: Only PNG and JPG images are allowed.")
            reset_function()
            break
        if not os.path.exists(img_path):
            print(f"\nERROR: The file {img_path} does not exist.")
            reset_function()
            break

        os.system('cls' if os.name == 'nt' else 'clear')
        print("----- ENCRYPTION MODE -----\n")

        key = generate_enc_key()

        img_file_name = os.path.splitext(os.path.basename(img_path))[0]
        key_path = f'encryption_key_{img_file_name}.json'
        save_enc_key(key, key_path)
        img_extension = os.path.splitext(img_path)[1]
        output_image_name = f'encrypted_{img_file_name}{img_extension}'

        if(en_mode == 'm1'):
            en_mode_m1(img_path, output_image_name, key)
        else:
            en_mode_m2(img_path, output_image_name, key)
        
        print(f"\nImage encrypted successfully! Encryption key saved at: /{key_path}")
        break

def decrypt(img_path, en_mode, key_path):
    while True:
        if len(img_path) == 0 or len(en_mode) == 0:
            print("\nERROR: Empty fields detected. Resetting")
            reset_function()
            break
        if en_mode != 'm2' and en_mode != 'm1':
            print("\nERROR: Only m1 and m2 modes are supported.")
            reset_function()
            break
        if not os.path.exists(img_path):
            print(f"\nERROR: The file {img_path} does not exist.")
            reset_function()
            break
        if not os.path.exists(key_path):
            print(f"\nThe file {key_path} does not exist.")
            reset_function()
            break
        if not check_img_extension(img_path):
            print("\nOnly PNG and JPG images are allowed.")
            reset_function()
            break
        if not check_enc_key_extension(key_path):
            print("\nThe encryption key should only be JSON file generated at the time of encryption.")
            reset_function()
            break

        os.system('cls' if os.name == 'nt' else 'clear')
        print("----- DECRYPTION MODE -----\n")

        key = load_enc_key(key_path)

        img_file_name = os.path.splitext(os.path.basename(img_path))[0]
        img_extension = os.path.splitext(img_path)[1]
        output_image_name = f'decrypted_{img_file_name}.{img_extension}'

        if en_mode == 'm1':
            dc_mode_1(img_path, output_image_name,key)
        else:
            dc_mode_2(img_path, output_image_name,key)
        
        print("Image decrypted successfully!")
        break
        

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("----- PIXEL MANIPULATOR W/ ENCRYPTION AND DECRYPTION -----\n" + 
              "Guide:\n\t1. Encrypt Image\n\t2. Decrypt Image\n\t3. Enter 0 to exit the program")

        action = str(input("\nDo you want to encrypt or decrypt the image? (enter 'encrypt' or 'decrypt'): ")).strip().lower()

        if action == 'encrypt':
            print("\n\nGuide:\n\t1. Program will not accept any empty fields/values" + 
                  "\n\t2. An encryption key will be generated which could be usef for decrypting this image using this program.\n\n")
            
            img_path = input("Enter the path of the image to encrypt (e.g. /Desktop/img.png): ").strip()
            en_mode = str(input("Enter Mode of Encryption (m1 or m2): ")).strip().lower()

            try:
                encrypt(img_path, en_mode)
            except (FileNotFoundError, ValueError) as e:
                print(e)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        elif action == 'decrypt':
            print("\n\nGuide:\n\t1. Program will not accept any empty fields/values" + 
                  "\n\t2. Make sure you properly enter the path and the name of the image that needs to be decrypted" + 
                  "\n\t3. Also ensure you enter the correct path to the encryption key." + 
                  "\n\t4. Currently, the program necessitates the user's specification of the encryption mode (m1/m2) used for the encryption of image as it cannot automatically detect. (Considering that this program was used for encryption)\n\n")

            img_path = input("Enter the path of the image to decrypt (e.g. /Desktop/img.png): ").strip()
            en_mode = str(input("Enter Mode of Encryption (m1 or m2) which was used to encrypt the image: ")).strip().lower()
            key_path = input("Enter the path to the encryption key JSON: ").strip()

            try:
                decrypt(img_path, en_mode, key_path)
            except (FileNotFoundError, ValueError) as e:
                print(e)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        elif action == '0':
            break
        else:
            print("Invalid action. Enter either 'encrypt' or 'decrypt'.")

        input("\nPress any key to continue...")

if __name__ == "__main__":
    main()