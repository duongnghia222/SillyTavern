import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

class ConversationViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversation Viewer || Press 'q' to quit || 'L' to load conversation || Left arrow=previous || Right arrow=next")
        # get the screen width and height
        ws = self.root.winfo_screenwidth()  # width of the screen
        hs = self.root.winfo_screenheight()  # height of the screen
        # display full screen
        self.root.geometry(f"{ws}x{hs}+0+0")
        self.delete_button = tk.Button(self.root, text="Delete Conversation", command=self.delete_conversation,
                                       bg="red", fg="white")
        self.delete_button.pack(side=tk.TOP)  # Place the button at the top of the window

        # Create a button to load conversation
        self.load_button = tk.Button(self.root, text="Load Conversation", command=self.load_conversation)
        self.load_button.pack(side=tk.TOP)  # Place the button next to the delete button

        self.character_folder = ""
        self.conversations = []
        self.current_conversation_index = 0

        self.previous_button = tk.Button(self.root, text="Previous", command=self.show_previous_conversation)
        self.previous_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(self.root, text="Next", command=self.show_next_conversation)
        self.next_button.pack(side=tk.RIGHT)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.exit_button.pack(side=tk.BOTTOM)

        self.note_label = tk.Label(self.root)
        self.note_label.pack(side=tk.TOP)

        self.conversation_text = tk.Text(self.root, wrap=tk.WORD, font=("Arial", 12))  # Set font here
        self.conversation_text.pack(expand=True, fill=tk.BOTH)
        self.conversation_text.tag_configure("bold", font=("Arial", 12, "bold"))  # Define a tag for bold text

        # Add a scrollbar for the conversation Text widget
        scrollbar = tk.Scrollbar(self.root, command=self.conversation_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.conversation_text.config(yscrollcommand=scrollbar.set)

    def delete_conversation(self):
        # Prompt confirmation
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this conversation?")

        if confirm:
            # Delete conversation file
            conversation_file = self.conversations[self.current_conversation_index]["file"]
            os.remove(conversation_file)

            # Delete conversation data from the list
            del self.conversations[self.current_conversation_index]

            # Update GUI
            if self.conversations:
                self.current_conversation_index = max(0, self.current_conversation_index - 1)
                self.show_conversation(self.current_conversation_index)
            else:
                self.conversation_text.delete("1.0", tk.END)
                self.note_label.config(text="")

    def load_conversation(self):
        # Open a file dialog to choose the character folder default will be os.getcwd()/conversations
        self.character_folder = filedialog.askdirectory(initialdir=os.getcwd() + "/conversations", title="Select Character Folder")
        if self.character_folder:
            self.conversations = self.load_conversations_from_folder(self.character_folder)
            if self.conversations:
                self.load_note()
                self.show_conversation(self.current_conversation_index)

    def load_conversations_from_folder(self, folder):
        conversations = []

        # Iterate through files in the folder newest first
        files = sorted(os.listdir(folder), key=lambda x: os.path.getctime(os.path.join(folder, x)))
        # reverse the list to get the newest first
        files = files[::-1]
        for file in files:
            if file.endswith('.jsonl'):
                file_path = os.path.join(folder, file)
                conversation = []  # Initialize an empty list for each conversation
                with open(file_path, 'r', encoding='utf-8') as f:
                    # Read each line (each line represents a JSON object)
                    for line in f:
                        conversation_data = json.loads(line)
                        conversation.append(conversation_data)
                conversations.append({"file": file_path, "conversation": conversation})  # Append the conversation to the list of conversations
        return conversations

    def load_note(self):
        for filename in os.listdir(self.character_folder):
            if filename.endswith(".json"):
                note_file = os.path.join(self.character_folder, filename)
                break

        if note_file is not None:
            with open(note_file, 'r', encoding='utf-8') as f:
                note_data = json.load(f)
                description = note_data.get("description", "")
                self.note_label.config(text=description, wraplength=1000, justify="left")  # Align text to the left (west)

    def show_conversation(self, index):
        conversation_data = self.conversations[index]

        # Clear previous conversation text
        self.conversation_text.delete("1.0", tk.END)
        meta_data = conversation_data["conversation"][0]
        self.conversation_text.insert(tk.END, f"Created at: {meta_data['create_date']} \n", "bold")
        skip = True
        for message in conversation_data["conversation"]:
            if skip:
                skip = False
                continue
            if isinstance(message, dict):  # Check if message is a dictionary
                sender = message.get('name', 'Unknown')  # Use get() to safely access dictionary keys
                text = message.get('mes', 'No message')
                self.conversation_text.insert(tk.END, f"{sender}: ", "bold")
                self.conversation_text.insert(tk.END, f"{text}\n")
            else:
                self.conversation_text.insert(tk.END, f"{message}\n")  # Handle non-dictionary messages

        # Scroll to the end of the conversation
        self.conversation_text.see(tk.END)

    def show_previous_conversation(self):
        if self.current_conversation_index > 0:
            self.current_conversation_index -= 1
            self.show_conversation(self.current_conversation_index)

    def show_next_conversation(self):
        if self.current_conversation_index < len(self.conversations) - 1:
            self.current_conversation_index += 1
            self.show_conversation(self.current_conversation_index)

if __name__ == "__main__":
    root = tk.Tk()
    app = ConversationViewer(root)
    root.bind('q', lambda event: root.quit())
    # L to load conversation
    root.bind('l', lambda event: app.load_conversation())
    root.bind('<Left>', lambda event: app.show_previous_conversation())

    # Bind right arrow key to show the next conversation
    root.bind('<Right>', lambda event: app.show_next_conversation())
    root.mainloop()
