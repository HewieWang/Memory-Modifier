import tkinter as tk
from ctypes import windll, byref, c_int, c_char_p, create_string_buffer, sizeof
from tkinter import messagebox

class MemoryModifierGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Modifier")

        self.process_id_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.value_var = tk.StringVar()
        self.current_value_var = tk.StringVar()

        # 创建控件
        process_id_label = tk.Label(root, text="Process ID:")
        process_id_entry = tk.Entry(root, textvariable=self.process_id_var)
        address_label = tk.Label(root, text="Memory Address:")
        address_entry = tk.Entry(root, textvariable=self.address_var)
        current_value_label = tk.Label(root, text="Current Value:")
        current_value_entry = tk.Entry(root, textvariable=self.current_value_var, state="readonly")
        value_label = tk.Label(root, text="New Value:")
        value_entry = tk.Entry(root, textvariable=self.value_var)
        read_button = tk.Button(root, text="Read Memory", command=self.read_memory)
        modify_button = tk.Button(root, text="Modify Memory", command=self.modify_memory)

        # 布局设置
        process_id_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        process_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        address_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        address_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        current_value_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        current_value_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        value_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        value_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        read_button.grid(row=4, column=0, columnspan=2, pady=5)
        modify_button.grid(row=5, column=0, columnspan=2, pady=10)

    def read_memory(self):
        try:
            process_id = int(self.process_id_var.get())
            address = int(self.address_var.get(), 16)

            process = windll.kernel32.OpenProcess(0x1F0FFF, False, process_id)
            if process:
                buffer = c_int()
                windll.kernel32.ReadProcessMemory(process, address, byref(buffer), sizeof(buffer), None)
                windll.kernel32.CloseHandle(process)

                # 显示当前内存值
                self.current_value_var.set(hex(buffer.value))
            else:
                tk.messagebox.showerror("Error", f"Unable to open process with ID {process_id}.")
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")

    def modify_memory(self):
        try:
            process_id = int(self.process_id_var.get())
            address = int(self.address_var.get(), 16)
            new_value = int(self.value_var.get(), 16)

            process = windll.kernel32.OpenProcess(0x1F0FFF, False, process_id)
            if process:
                windll.kernel32.WriteProcessMemory(process, address, byref(new_value), sizeof(new_value), None)
                windll.kernel32.CloseHandle(process)
                tk.messagebox.showinfo("Success", "Memory modified successfully.")
            else:
                tk.messagebox.showerror("Error", f"Unable to open process with ID {process_id}.")
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryModifierGUI(root)
    root.mainloop()
