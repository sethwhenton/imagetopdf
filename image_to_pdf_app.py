import os
from tkinter import Tk, Button, filedialog, messagebox, Label, StringVar, LEFT, RIGHT, TOP, BOTTOM, BOTH
from PIL import Image, ImageTk

class ImageToPdfConverter:
    tk_image = None  # Class variable to retain the image reference

    def __init__(self, master):
        self.master = master
        master.title("Image to PDF Converter")

        # Set color scheme
        primary_color = "#990F02"  # Red
        secondary_color = "#FFFFFF"  # White
        tertiary_color = "#000000"  # Black

        # Center the window
        window_width = 400
        window_height = 500  # Increased height to accommodate the preview label
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        master.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Preview label for the selected image
        self.preview_label = Label(master, bg=secondary_color, fg=tertiary_color)
        self.preview_label.pack(side=TOP, fill=BOTH, expand=True, padx=20, pady=20)

        # Middle side (single button)
        self.single_button = Button(master, text="Upload Image", command=self.upload_or_choose_or_convert, bg=primary_color, fg=secondary_color, width=20, height=4)
        self.single_button.pack(padx=10, pady=10)

        # Bottom side (file details)
        self.file_details_var = StringVar()
        self.file_details_label = Label(master, textvariable=self.file_details_var, anchor="w", justify=LEFT, bg=secondary_color, fg=tertiary_color)
        self.file_details_label.pack(side=BOTTOM, expand=True, padx=20, pady=20)

        

        

        # Step variables
        self.image_uploaded = False
        self.destination_selected = False

    def upload_or_choose_or_convert(self):
        if not self.image_uploaded:
            self.upload_image()
        elif not self.destination_selected:
            self.choose_destination()
        else:
            self.convert_to_pdf()

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

        if file_path:
            self.image_path = file_path
            self.original_filename = os.path.basename(file_path)
            self.update_file_details()
            self.update_preview()
            self.image_uploaded = True
            self.destination_selected = False
            self.single_button.config(text="Select Destination")

    def update_file_details(self):
        if self.image_path:
            file_name = f"File Name: {self.original_filename}\n"
            file_size = f"File Size: {os.path.getsize(self.image_path) / 1024:.2f} KB\n"
            file_type = f"File Type: {self.image_path.split('.')[-1]}\n"
            file_location = f"File Location: {os.path.dirname(self.image_path)}"
            self.file_details_var.set(file_name + file_size + file_type + file_location)

    def update_preview(self):
        if self.image_path:
            image = Image.open(self.image_path)
            image.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(image)
            self.preview_label.configure(image=photo)
            self.preview_label.image = photo

    def choose_destination(self):
        self.destination_directory = filedialog.askdirectory(title="Select Destination Directory")

        if self.destination_directory:
            self.destination_selected = True
            self.single_button.config(text="Convert to PDF")

    def convert_to_pdf(self):
        if not self.image_uploaded:
            messagebox.showerror("Error", "Please upload an image first.")
            return

        if not self.destination_selected:
            messagebox.showerror("Error", "Please choose a destination directory first.")
            return

        try:
            pdf_filename = self.original_filename.replace('.', '_converted.') + ".pdf"
            pdf_path = os.path.join(self.destination_directory, pdf_filename)

            # Create PDF
            with Image.open(self.image_path) as img:
                img.save(pdf_path, "PDF", resolution=100.0, save_all=True)

            self.show_conversion_notification(pdf_path)
            self.reset_program()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during conversion: {str(e)}")

    def show_conversion_notification(self, pdf_path):
        messagebox.showinfo("Conversion Complete", f"Image has been converted to PDF and saved in:\n{pdf_path}")

    def reset_program(self):
        # Reset all variables
        self.image_path = None
        self.original_filename = None
        self.image_uploaded = False
        self.destination_selected = False

        # Clear file information display
        self.file_details_var.set("")
        self.preview_label.configure(image="")
        self.single_button.config(text="Upload Image")

if __name__ == "__main__":
    root = Tk()
    app = ImageToPdfConverter(root)
    root.mainloop()
