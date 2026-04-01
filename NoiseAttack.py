# code executed by Faizal Nujumudeen
# Presidency University, Bengaluru

import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("encrypted.png",0)

# Salt and pepper noise
noise = img.copy()
prob = 0.05
rand = np.random.rand(*img.shape)

noise[rand < prob] = 0
noise[rand > 1-prob] = 255

# Example decrypted image (replace with real decryption)
decrypted = cv2.imread("decrypted.png",0) #noise

plt.figure()
plt.imshow(img,cmap='gray')
plt.title("Encrypted Image")
plt.savefig("encrypted_Img.png")
plt.close()


plt.figure()
plt.imshow(noise,cmap='gray')
plt.title("Encrypted Image with Noise")
plt.savefig("encrypted_Noise.png")
plt.close()


plt.figure()
plt.imshow(decrypted,cmap='gray')
plt.title("Decrypted Image After Noise Attack")
plt.savefig("decrypted_Noise.png")
plt.close()

#plt.show()

# "If you want to shine like a sun, first burn like a sun" - Dr. APJ Abdul Kalam.
# Success is a continuous process