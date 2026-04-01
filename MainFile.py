# code executed by Faizal Nujumudeen
# Presidency University, Bengaluru

import os
import cv2
import numpy as np
import hashlib
import matplotlib.pyplot as plt
import pandas as pd
import time
from scipy.stats import entropy
from skimage.metrics import structural_similarity as ssim

# ======================================================
# Create results folder
# ======================================================

def create_output_folder(image_path):
    name = os.path.splitext(os.path.basename(image_path))[0]
    folder = name
    os.makedirs(folder, exist_ok=True)
    return folder


# ======================================================
# Key generation
# ======================================================

def generate_key(seed):
    h = hashlib.sha256(seed.encode()).hexdigest()
    return int(h, 16)


# ======================================================
# ECC-like pseudo random sequence generator
# ======================================================

def ecc_sequence(key, n):

    seq = []
    x = key % 257
    y = (key >> 8) % 257

    for i in range(n):

        x = (x*x + y + i) % 257
        y = (y*y + x + i) % 257

        seq.append((x ^ y) % 256)

    return np.array(seq, dtype=np.uint8)


# ======================================================
# SBOX generation
# ======================================================

def generate_sbox(key):

    seq = ecc_sequence(key, 256)

    sbox = np.argsort(seq)

    inv = np.zeros_like(sbox)

    for i, v in enumerate(sbox):
        inv[v] = i

    return sbox.astype(np.uint8), inv.astype(np.uint8)


# ======================================================
# Substitution
# ======================================================

def substitute(img, sbox):

    flat = img.flatten()

    sub = sbox[flat]

    return sub.reshape(img.shape)


def inverse_substitute(img, inv):

    flat = img.flatten()

    sub = inv[flat]

    return sub.reshape(img.shape)


# ======================================================
# Diffusion (Reversible)
# ======================================================

def diffusion(img, key):

    flat = img.flatten()

    ks = ecc_sequence(key, len(flat))

    cipher = np.bitwise_xor(flat, ks)

    return cipher.reshape(img.shape), ks


# ======================================================
# Permutation
# ======================================================

def permute(img, key):

    flat = img.flatten()

    seq = ecc_sequence(key, len(flat))

    perm = np.argsort(seq)

    permuted = flat[perm]

    return permuted.reshape(img.shape), perm


def inverse_permute(img, perm):

    flat = img.flatten()

    inv = np.zeros_like(flat)

    inv[perm] = flat

    return inv.reshape(img.shape)


# ======================================================
# Encryption
# ======================================================

def encrypt(img, key):

    sbox, inv_sbox = generate_sbox(key)

    sub = substitute(img, sbox)

    diff, ks = diffusion(sub, key)

    perm_img, perm = permute(diff, key)

    return perm_img, sbox, inv_sbox, perm, ks


# ======================================================
# Decryption
# ======================================================

def decrypt(cipher, inv_sbox, perm, key, ks):

    invperm = inverse_permute(cipher, perm)

    flat = invperm.flatten()

    plain = np.bitwise_xor(flat, ks)

    plain = plain.reshape(invperm.shape)

    dec = inverse_substitute(plain, inv_sbox)

    return dec


# ======================================================
# Security Metrics
# ======================================================

def image_entropy(img):

    hist, _ = np.histogram(img.flatten(), 256, [0,256])
    p = hist / np.sum(hist)

    return entropy(p, base=2)


def correlation(img):

    x = img[:,:-1].flatten()
    y = img[:,1:].flatten()

    return np.corrcoef(x, y)[0,1]


def NPCR(img1, img2):

    diff = img1 != img2

    return np.sum(diff) / diff.size * 100


def UACI(img1, img2):

    return np.mean(np.abs(img1.astype(int) - img2.astype(int)) / 255) * 100


# ======================================================
# Histogram plot
# ======================================================

def histogram_plot(img, title, path):

    plt.figure()

    plt.hist(img.flatten(), 256)

    plt.title(title)

    plt.savefig(path)

    plt.close()


# ======================================================
# Comparative analysis plot
# ======================================================

def comparative_plot(results, path):

    df = pd.DataFrame(results)

    df.plot(kind='bar')

    plt.title("Comparative Security Metrics")

    plt.savefig(path)

    plt.close()


# ======================================================
# MAIN PIPELINE
# ======================================================

def run(image_path):

    folder = create_output_folder(image_path)

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError("Image not found")

    cv2.imwrite(folder + "/input.png", img)

    key = generate_key(image_path)

    start = time.time()

    cipher, sbox, inv_sbox, perm, ks = encrypt(img, key)

    end = time.time()

    cv2.imwrite(folder + "/encrypted.png", cipher)

    dec = decrypt(cipher, inv_sbox, perm, key, ks)

    cv2.imwrite(folder + "/decrypted.png", dec)

    print("Decryption correct:", np.array_equal(img, dec))


    # ==================================================
    # Security analysis
    # ==================================================

    ent = image_entropy(cipher)

    corr = correlation(cipher)

    npcr = NPCR(img, cipher)

    uaci = UACI(img, cipher)

    metrics = {

        "Entropy":[ent],
        "Correlation":[corr],
        "NPCR":[npcr],
        "UACI":[uaci]

    }

    pd.DataFrame(metrics).to_csv(folder + "/security_metrics.csv")


    # ==================================================
    # Lightweight analysis
    # ==================================================

    runtime = end - start

    memory = img.nbytes / 1024

    lw = {

        "Runtime_sec":[runtime],
        "Memory_KB":[memory]

    }

    pd.DataFrame(lw).to_csv(folder + "/lightweight_metrics.csv")


    # ==================================================
    # Histogram plots
    # ==================================================

    histogram_plot(img, "Input Histogram", folder + "/input_hist.png")
    histogram_plot(cipher, "Histogram - Encrypted Image", folder + "/cipher_hist.png")
    histogram_plot(dec, "Histogram - Decrypted Image", folder + "/decry_hist.png")

    # ==================================================
    # Comparative analysis
    # ==================================================

    comp = {

        "Metric":["Entropy","Correlation","NPCR","UACI"],

        "Proposed":[ent,corr,npcr,uaci],

        "AES":[7.98,0.01,99.5,33.1],

        "Chaos":[7.99,0.009,99.6,33.3]

    }

    df = pd.DataFrame(comp)

    df.set_index("Metric").plot(kind='bar')

    plt.savefig(folder + "/comparative.png")

    plt.close()

    print("Results saved in:", folder)


# ======================================================

if __name__ == "__main__":

    run("Eiffel.jpg")

# "If you want to shine like a sun, first burn like a sun" - Dr. APJ Abdul Kalam.
# Success is a continuous process