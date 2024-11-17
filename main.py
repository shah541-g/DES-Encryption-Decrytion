import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from Encryption import DES_EncryptionCypher
from PDFHandler import PDFHandler
import os

class DESApp(tk.Tk): 
    def __init__(self):
        super().__init__()  
        self.title("Encryption and Decryption (DES)")
        self.geometry("500x650")  
        self.config(padx=20, pady=20, bg="#27A58C")  

       
        heading = tk.Label(self, text="DES Encryption and Decryption", font=("Times New Roman", 20, "bold"), bg="#27A58C")
        heading.pack(pady=20)

        self.boolean_var = tk.BooleanVar(value=False)  
        self.file_name = None
        self.text_content = ""

        
        self.option_frame = tk.Frame(self)
        self.option_frame.pack(pady=10)

        
        tk.Radiobutton(self.option_frame, text="Encryption", font=("Arial", 12, "bold"), width=10, height=4, variable=self.boolean_var, value=True, relief="flat", command=self.update_mode, bg="#27A58C").pack(side="left")
        tk.Radiobutton(self.option_frame, text="Decryption", font=("Arial", 12, "bold"), width=10, height=4, variable=self.boolean_var, value=False, relief="flat", command=self.update_mode, bg="#27A58C").pack(side="left")

       
        self.upload_button = tk.Button(self, text="Upload PDF", command=self.upload_file, bg="#1B8314", fg="white", width=20, height=2)
        self.upload_button.pack(pady=10)

       
        self.text_area = ScrolledText(self, wrap="word", height=15)
        self.text_area.pack(fill="both", expand=True, padx=10, pady=10)

        
        self.action_button = tk.Button(self, text="Encrypt/Decrypt and Save", bg="#092768", fg="white", command=self.process_text, width=30, height=2)
        self.action_button.pack(pady=25, padx=10)

    def update_mode(self):
        
        if self.boolean_var.get():
            self.action_button.config(text="Encrypt and Save")
        else:
            self.action_button.config(text="Decrypt and Save")

    def upload_file(self):
       
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.file_name = file_path.split('/')[-1]
            self.text_content = PDFHandler.readPdf(file_path).replace("’", "'")
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, self.text_content)

    def process_text(self):
        
        edited_text = self.text_area.get("1.0", tk.END).strip()
        key = "AHMADALI"
        des = DES_EncryptionCypher()

        save_file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile="encryptedFile.pdf" if self.boolean_var.get() else "decryptedFile.pdf",
            title="Save as"
        )

        if save_file_path:
            try:
                if self.boolean_var.get():
                    encrypted_text = des.desEncrypt(plainText=edited_text, key=key)
                    print(f"Saving encrypted PDF to: {save_file_path}")
                    PDFHandler.writePdf(save_file_path, encrypted_text)

                else:
                    decrypted_text = des.desDecrypt(edited_text, key=key)
                    print(f"Saving decrypted PDF to: {save_file_path}")
                    PDFHandler.writePdf(save_file_path, decrypted_text)

                if os.path.exists(save_file_path):
                    messagebox.showinfo("Success", f"File saved successfully at '{save_file_path}'.")
                else:
                    raise Exception("File not saved; attempting direct write.")

            except Exception as e:
                print(f"Error with PDFHandler, attempting direct write: {e}")
                with open(save_file_path, "w", encoding="utf-8") as file:
                    if self.boolean_var.get():
                        file.write(encrypted_text)
                    else:
                        file.write(decrypted_text)
                messagebox.showinfo("Success", f"File saved at '{save_file_path}' via direct write.")

if __name__ == "__main__":
    app = DESApp()
    app.mainloop()
