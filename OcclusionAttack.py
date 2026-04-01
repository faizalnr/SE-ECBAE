# code executed by Faizal Nujumudeen
# Presidency University, Bengaluru

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from Pgm2 import *

# ======================================
# File paths
# ======================================

input_image_path = "input.png"
encrypted_image_path = "encrypted.png"

output_folder = "Occlusion_Attack"
os.makedirs(output_folder, exist_ok=True)

# ======================================
# Read images
# ======================================

input_img = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
encrypted_img = cv2.imread(encrypted_image_path, cv2.IMREAD_GRAYSCALE)

# ======================================
# Occlusion Attack
# ======================================

def occlusion_attack(image, percent=0.2):

    img = image.copy()

    h, w = img.shape

    occ_h = int(h * percent)
    occ_w = int(w * percent)

    start_x = h // 2 - occ_h // 2
    start_y = w // 2 - occ_w // 2

    img[start_x:start_x+occ_h, start_y:start_y+occ_w] = 0

    return img

occluded_img = occlusion_attack(encrypted_img, percent=0.25)
occluded_img = occlusion_attack(input_img, percent=0.25)

# ======================================
# Save occluded encrypted image
# ======================================

cv2.imwrite(os.path.join(output_folder,"occluded_encrypted.png"), occluded_img)
cv2.imwrite(os.path.join(output_folder,"occluded_decrypted.png"), occluded_img)


# ======================================
# Decryption (Replace with your algorithm)
# ======================================

# def decrypt_image(cipher_img):
    
#     # Replace this with your real decryption function
    
#     decrypted = cipher_img.copy()
    
#     return decrypted

# decrypted_img = decrypt(occluded_img)

# cv2.imwrite(os.path.join(output_folder,"decrypted_after_occlusion.png"), decrypted_img)

# ======================================
# Display results
# ======================================

# plt.figure(figsize=(12,4))

# plt.subplot(1,3,1)
# plt.imshow(encrypted_img,cmap='gray')
# plt.title("Encrypted Image")
# plt.axis("off")

# plt.subplot(1,3,2)
# plt.imshow(occluded_img,cmap='gray')
# plt.title("Occluded Encrypted Image")
# plt.axis("off")

# plt.subplot(1,3,3)
# plt.imshow(decrypted_img,cmap='gray')
# plt.title("Decrypted Image After Occlusion")
# plt.axis("off")

# plt.show()

# print("Occlusion attack experiment completed.")
# print("Results saved in folder:", output_folder)

# "If you want to shine like a sun, first burn like a sun" - Dr. APJ Abdul Kalam.
# Success is a continuous process