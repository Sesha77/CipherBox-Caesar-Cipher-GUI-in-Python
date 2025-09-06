import tkinter as tk
from tkinter import messagebox

# ---------- Caesar Cipher Logic ----------
def encrypt(text: str, shift: int) -> str:
    shift = shift % 26
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)

def decrypt(text: str, shift: int) -> str:
    # normalize and invert shift, then reuse encrypt
    shift = shift % 26
    return encrypt(text, -shift)


# ---------- GUI helper functions ----------
def get_shift():
    try:
        s = int(key_entry.get())
        return s
    except ValueError:
        messagebox.showerror("Invalid key", "Shift key must be an integer.")
        return None

def show_output(text):
    output_text.config(state='normal')
    output_text.delete("1.0", tk.END)
    output_text.insert("1.0", text)
    output_text.config(state='disabled')

def do_encrypt():
    s = get_shift()
    if s is None: return
    plain = input_text.get("1.0", "end-1c")
    if not plain:
        messagebox.showinfo("Empty", "Please type the message to encrypt in the Input box.")
        return
    show_output(encrypt(plain, s))

def do_decrypt():
    s = get_shift()
    if s is None: return
    cipher = input_text.get("1.0", "end-1c")
    if not cipher:
        messagebox.showinfo("Empty", "Please paste the ENCRYPTED message into the Input box before decrypting.")
        return
    show_output(decrypt(cipher, s))

def clear_all():
    input_text.delete("1.0", tk.END)
    key_entry.delete(0, tk.END)
    show_output("")

def copy_output():
    out = output_text.get("1.0", "end-1c")
    if out.strip() == "":
        messagebox.showinfo("Nothing to copy", "Output is empty.")
        return
    root.clipboard_clear()
    root.clipboard_append(out)
    messagebox.showinfo("Copied", "Output copied to clipboard.")

def use_output_as_input():
    out = output_text.get("1.0", "end-1c")
    input_text.delete("1.0", tk.END)
    input_text.insert("1.0", out)
    show_output("")

def fill_example():
    input_text.delete("1.0", tk.END)
    input_text.insert("1.0", "Hello, World!")
    key_entry.delete(0, tk.END)
    key_entry.insert(0, "3")
    show_output("")

# ---------- Tkinter UI ----------
root = tk.Tk()
root.title("Caesar Cipher — Encrypt / Decrypt")
root.geometry("640x420")
root.resizable(False, False)
root.config(bg="#f7fafc")

title = tk.Label(root, text="Caesar Cipher (A ↔ Z) — Enter text and a numeric key", font=("Segoe UI", 13, "bold"), bg="#f7fafc")
title.pack(pady=10)

frame = tk.Frame(root, bg="#f7fafc")
frame.pack(padx=12, pady=6, fill="both", expand=False)

# Input text (multi-line)
tk.Label(frame, text="Input (type plain text or paste encrypted text here):", bg="#f7fafc").grid(row=0, column=0, sticky="w")
input_text = tk.Text(frame, height=5, width=72, wrap="word", font=("Arial", 11))
input_text.grid(row=1, column=0, columnspan=6, pady=(4,8))

# Key entry
tk.Label(frame, text="Shift key (integer):", bg="#f7fafc").grid(row=2, column=0, sticky="w")
key_entry = tk.Entry(frame, width=8, font=("Arial", 11))
key_entry.grid(row=2, column=1, sticky="w", padx=(6,20))

# Buttons
btn_encrypt = tk.Button(frame, text="Encrypt →", width=12, command=do_encrypt)
btn_encrypt.grid(row=2, column=2, padx=6)

btn_decrypt = tk.Button(frame, text="← Decrypt", width=12, command=do_decrypt)
btn_decrypt.grid(row=2, column=3, padx=6)

btn_clear = tk.Button(frame, text="Clear", width=10, command=clear_all)
btn_clear.grid(row=2, column=4, padx=6)

btn_example = tk.Button(frame, text="Fill Example", width=12, command=fill_example)
btn_example.grid(row=2, column=5, padx=6)

# Output
tk.Label(frame, text="Output:", bg="#f7fafc").grid(row=3, column=0, sticky="w", pady=(12,0))
output_text = tk.Text(frame, height=5, width=72, wrap="word", font=("Arial", 11), state='disabled')
output_text.grid(row=4, column=0, columnspan=6, pady=(4,8))

# Small helper buttons under output
helper_frame = tk.Frame(frame, bg="#f7fafc")
helper_frame.grid(row=5, column=0, columnspan=6, pady=(4,0))

tk.Button(helper_frame, text="Copy Output", width=14, command=copy_output).grid(row=0, column=0, padx=6)
tk.Button(helper_frame, text="Use Output as Input", width=18, command=use_output_as_input).grid(row=0, column=1, padx=6)
tk.Label(helper_frame, text="(To decrypt: paste encrypted text in Input and press '← Decrypt' with same key)", bg="#f7fafc").grid(row=0, column=2, padx=10)

# Footer / quick test
footer = tk.Label(root, text="Quick test: Hello + key 3 → Encrypt = Khoor. To decrypt, paste Khoor and key=3 then press Decrypt.", bg="#f7fafc", fg="#333")
footer.pack(pady=8)

root.mainloop()
