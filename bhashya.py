import tkinter as tk
import speech_recognition as sr
from tkinter import filedialog

# Create main window
root = tk.Tk()
root.title("Speech to Text Converter")
root.geometry("600x400")
root.resizable(False, False)
root.configure(bg="light blue")

recognizer = sr.Recognizer()
is_recording = False

def record_audio():
    global is_recording
    is_recording = True
    text_area.delete("1.0", tk.END)
    status_label.config(text="Listening...", fg="green")
    root.update()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=10)
            text = recognizer.recognize_google(audio)
            text_area.insert(tk.END, text)
            status_label.config(text="Recording Stopped!", fg="blue")
        except sr.UnknownValueError:
            status_label.config(text="Could not understand audio", fg="red")
        except sr.RequestError:
            status_label.config(text="Error with speech recognition", fg="red")
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}", fg="red")
    
    is_recording = False  # Stop recording

def stop_recording():
    global is_recording
    if is_recording:
        is_recording = False
        status_label.config(text="Stopped manually!", fg="orange")

def save_text():
    text = text_area.get("1.0", tk.END).strip()
    if not text:
        status_label.config(text="No text to save!", fg="red")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"),
                                                        ("All files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text)
        status_label.config(text="Text Saved Successfully!", fg="green")

# UI Components
tk.Label(root, text="Speech to Text Converter", font="Arial 20 bold", bg="light blue").pack(pady=10)

status_label = tk.Label(root, text="", font="Arial 14", bg="light blue")
status_label.pack()

text_area = tk.Text(root, font="Arial 14", height=6, width=50, wrap=tk.WORD)
text_area.pack(pady=10)

button_frame = tk.Frame(root, bg="light blue")
button_frame.pack(pady=10)

record_btn = tk.Button(button_frame, text="Start Recording", font="Arial 12 bold", bg="white", command=record_audio)
record_btn.grid(row=0, column=0, padx=10)

stop_btn = tk.Button(button_frame, text="Stop", font="Arial 12 bold", bg="white", command=stop_recording)
stop_btn.grid(row=0, column=1, padx=10)

save_btn = tk.Button(button_frame, text="Save", font="Arial 12 bold", bg="white", command=save_text)
save_btn.grid(row=0, column=2, padx=10)

root.mainloop()
