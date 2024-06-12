import tkinter as tk
from tkinter import ttk
import sv_ttk
from tkinter import messagebox, simpledialog, filedialog
from queue_manager import upload_queue, save_queue, load_queue, delete_video
from video import Video
from schedule import start_scheduler
import threading
import json

class VideoSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Scheduler")
        self.root.minsize(500, 500)  # Set the minimum window size

        # Create Frame for Organization
        self.frame = ttk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Frame for Video Queue Section
        self.video_frame = ttk.Frame(self.frame, borderwidth=2, relief="groove")
        self.video_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.listBoxLabel = ttk.Label(self.video_frame, text="Video Queue")
        self.listBoxLabel.pack(padx=25, pady=10)

        self.listbox = tk.Listbox(self.video_frame, selectmode=tk.SINGLE, bg='#333333', fg='#ffffff', selectbackground='#666666', font=('Helvetica', 12))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=25, pady=10)

        self.scrollbar = ttk.Scrollbar(self.video_frame, command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # Frame for Schedule Section
        self.schedule_frame = ttk.Frame(self.frame, borderwidth=2, relief="groove")
        self.schedule_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.scheduleLabel = ttk.Label(self.schedule_frame, text="Schedule")
        self.scheduleLabel.pack(side=tk.TOP, padx=25, pady=10)

        self.tree_frame = ttk.Frame(self.schedule_frame)
        self.tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=25, pady=10)

        self.tree = ttk.Treeview(self.tree_frame, columns=("Day", "Time"), show="headings")
        self.tree.heading("Day", text="Day")
        self.tree.heading("Time", text="Time")
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.scrollbar_tree = ttk.Scrollbar(self.tree_frame, command=self.tree.yview)
        self.scrollbar_tree.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=self.scrollbar_tree.set)

        self.input_frame = ttk.Frame(self.schedule_frame)
        self.input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=25, pady=10)

        self.day_label = ttk.Label(self.input_frame, text="Day")
        self.day_label.pack(pady=5)
        self.day_var = tk.StringVar()
        self.day_combobox = ttk.Combobox(self.input_frame, textvariable=self.day_var)
        self.day_combobox['values'] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.day_combobox.pack(pady=5)

        self.hour_label = ttk.Label(self.input_frame, text="Hour")
        self.hour_label.pack(pady=5)
        self.hour_var = tk.StringVar()
        self.hour_entry = ttk.Entry(self.input_frame, textvariable=self.hour_var)
        self.hour_entry.pack(pady=5)

        self.minute_label = ttk.Label(self.input_frame, text="Minute")
        self.minute_label.pack(pady=5)
        self.minute_var = tk.StringVar()
        self.minute_entry = ttk.Entry(self.input_frame, textvariable=self.minute_var)
        self.minute_entry.pack(pady=5)

        self.add_time_button = ttk.Button(self.input_frame, text="Add Time", command=self.add_time)
        self.add_time_button.pack(pady=5)

        self.remove_time_button = ttk.Button(self.input_frame, text="Remove Time", command=self.remove_time)
        self.remove_time_button.pack(pady=5)

        self.load_schedule()

        # Frame for Buttons Section
        self.button_frame = ttk.Frame(self.frame)
        self.button_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.add_button = ttk.Button(self.button_frame, text="Add Video", command=self.add_video)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = ttk.Button(self.button_frame, text="Edit Video", command=self.edit_video)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ttk.Button(self.button_frame, text="Delete Video", command=self.delete_video)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.load_queue()

        # Add drag-and-drop support
        self.listbox.bind("<Button-1>", self.on_start_drag)
        self.listbox.bind("<B1-Motion>", self.on_drag_motion)
        self.listbox.bind("<ButtonRelease-1>", self.on_drop)

        self.drag_data = {"index": None}

    def load_queue(self):
        load_queue()
        self.refresh_listbox()

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        queue_list = list(upload_queue.queue)
        for video in queue_list:
            self.listbox.insert(tk.END, video.title)

    def add_video(self):
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=(("Video Files", "*.mp4;*.avi;*.mov"), ("All Files", "*.*"))
        )
        if not file_path:
            return

        title = simpledialog.askstring("Input", "Enter the video title:")
        if not title:
            messagebox.showerror("Error", "Video title is required.")
            return

        tags = simpledialog.askstring("Input", "Enter the video tags (comma-separated):")
        if tags is not None:
            tags = tags.split(',')
        else:
            messagebox.showerror("Error", "Video tags are required.")
            return

        description = simpledialog.askstring("Input", "Enter the video description:")
        if not description:
            messagebox.showerror("Error", "Video description is required.")
            return
        
        video = Video(file_path, title, tags, description)
        upload_queue.put(video)
        save_queue()
        self.refresh_listbox()
        messagebox.showinfo("Video Added", "This video has been added to the queue.")

    def edit_video(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No video selected.")
            return

        index = selected_index[0]
        queue_list = list(upload_queue.queue)
        video = queue_list[index]

        file_path = simpledialog.askstring("Input", "Edit the video file path:", initialvalue=video.file_path)
        title = simpledialog.askstring("Input", "Edit the video title:", initialvalue=video.title)
        tags = simpledialog.askstring("Input", "Edit the video tags (comma-separated):", initialvalue=','.join(video.tags)).split(',')
        description = simpledialog.askstring("Input", "Edit the video description:", initialvalue=video.description)

        if file_path and title and tags and description:
            video.file_path = file_path
            video.title = title
            video.tags = tags
            video.description = description

            upload_queue.queue.clear()
            for vid in queue_list:
                upload_queue.put(vid)
            save_queue()
            self.refresh_listbox()
        else:
            messagebox.showerror("Error", "All fields must be filled out.")
        messagebox.showinfo("Video Edited", "This video has been edited in the queue.")

    def delete_video(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No video selected.")
            return

        index = selected_index[0]
        delete_video(index)
        self.refresh_listbox()
        messagebox.showinfo("Video Deleted", "This video has been removed from the queue.")

    def add_time(self):
        day = self.day_var.get()
        hour = self.hour_var.get()
        minute = self.minute_var.get()
        if not day or not hour or not minute:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        time = f"{hour.zfill(2)}:{minute.zfill(2)}"
        self.tree.insert('', 'end', values=(day, time))
        self.save_schedule()

    def remove_time(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
            self.save_schedule()
        else:
            messagebox.showerror("Error", "No time selected.")

    def save_schedule(self):
        schedule = {}
        for row in self.tree.get_children():
            day, time = self.tree.item(row)['values']
            if day not in schedule:
                schedule[day] = []
            schedule[day].append(time)
        
        with open("schedule.json", "w") as f:
            json.dump(schedule, f, indent=4)

    def load_schedule(self):
        try:
            with open("schedule.json", "r") as f:
                schedule = json.load(f)
                for day, times in schedule.items():
                    for time in times:
                        self.tree.insert('', 'end', values=(day, time))
        except FileNotFoundError:
            pass

    def update_scheduler(self):
        # Notify the scheduler thread to update
        self.scheduler_event.set()

    def on_start_drag(self, event):
        self.drag_data["index"] = self.listbox.index("@%s,%s" % (event.x, event.y))

    def on_drag_motion(self, event):
        new_index = self.listbox.index("@%s,%s" % (event.x, event.y))
        if new_index != self.drag_data["index"]:
            self.swap_items(self.drag_data["index"], new_index)
            self.drag_data["index"] = new_index

    def on_drop(self, event):
        self.drag_data["index"] = None
        self.save_queue_order()

    def swap_items(self, index1, index2):
        if index1 < 0 or index2 < 0:
            return

        queue_list = list(upload_queue.queue)
        queue_list[index1], queue_list[index2] = queue_list[index2], queue_list[index1]

        self.listbox.delete(index1)
        self.listbox.insert(index1, queue_list[index1].title)
        self.listbox.delete(index2)
        self.listbox.insert(index2, queue_list[index2].title)

        upload_queue.queue.clear()
        for video in queue_list:
            upload_queue.put(video)

    def save_queue_order(self):
        save_queue()

    def refresh_listbox_threadsafe(self):
        # Use the Tkinter after method to refresh the listbox from the main thread
        self.root.after(0, self.refresh_listbox)

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoSchedulerApp(root)
    sv_ttk.set_theme("dark")

    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=start_scheduler, args=(app,))
    scheduler_thread.daemon = True  # This ensures the thread will exit when the main program exits
    scheduler_thread.start()
    print("Starting Scheduler...")

    root.mainloop()
