import tkinter as tk
from tkinter import ttk

import numpy as np
from src.process import Process
#from src.fcfs_scheduler import FCFSScheduler
from src.rr_scheduler import RRScheduler
#from src.sjf_scheduler import SJFScheduler
from tests.sjf_scheduler import SJFScheduler
#from src.priority_scheduler import PriorityScheduler
from tests.priority_scheduler import PriorityScheduler
from tests.fscs_scheduler import FCFSScheduler
from tests.rr_schedulerplot import RRSchedulerplot
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SchedulerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Scheduler")
        
        self.processes = []
        self.selected_algorithm = tk.StringVar(value="Round Robin")
        
        self.create_widgets()
      
    def create_widgets(self):
        # Create a custom style for the Combobox
        style = ttk.Style()
        style.configure("TFrame", background="#353457")
        style.configure("TLabel", background="#353457", foreground="#cdccd5", font=("Century Gothic", 12, "bold"))
        style.configure("TButton", background="#686781", foreground="#03012d", font=("Century Gothic", 10, "bold"))
        style.configure("TCombobox",
                        fieldbackground="darkblue",
                        background="lightblue",
                        foreground="white",
                        selectbackground="lightgray",
                        selectforeground="black",
                        padding=5)

        self.process_frame = ttk.Frame(self.master, style="TFrame")
        self.process_frame.pack(padx=10, pady=10)
        
        self.process_label = ttk.Label(self.process_frame, text="Processes:", style="TLabel")
        self.process_label.grid(row=0, column=0, sticky=tk.W)
        
        self.process_listbox = tk.Listbox(self.process_frame, 
            height=5, 
            bg="#1e2627",  # Background color
            fg="white",     # Text color
            selectbackground="lightblue",
            selectforeground="black",
            font=("Century Gothic", 10))
        self.process_listbox.grid(row=1, column=0, columnspan=5, padx=5, pady=5)
        self.process_listbox.bind('<<ListboxSelect>>', self.on_process_selected)
        
        self.remove_button = ttk.Button(self.process_frame, text="Remove Process", command=self.remove_process)
        self.remove_button.grid(row=2, column=0, padx=5, pady=5)
        
        self.edit_button = ttk.Button(self.process_frame, text="Edit Process", command=self.edit_process)
        self.edit_button.grid(row=2, column=1, padx=5, pady=5)
        
        self.process_name_label = ttk.Label(self.process_frame, text="Process ID")
        self.process_name_label.grid(row=3, column=0, padx=5, pady=5)
        self.process_arrival_label = ttk.Label(self.process_frame, text="Arrival Time")
        self.process_arrival_label.grid(row=3, column=1, padx=5, pady=5)
        self.process_burst_label = ttk.Label(self.process_frame, text="Burst Time")
        self.process_burst_label.grid(row=3, column=2, padx=5, pady=5)
        self.process_priority_label = ttk.Label(self.process_frame, text="Priority")
        self.process_priority_label.grid(row=3, column=3, padx=5, pady=5)
        
        self.process_name_entry = ttk.Entry(self.process_frame)
        self.process_name_entry.grid(row=4, column=0, padx=5, pady=5)
        self.process_arrival_entry = ttk.Entry(self.process_frame)
        self.process_arrival_entry.grid(row=4, column=1, padx=5, pady=5)
        self.process_burst_entry = ttk.Entry(self.process_frame)
        self.process_burst_entry.grid(row=4, column=2, padx=5, pady=5)
        self.process_priority_entry = ttk.Entry(self.process_frame)
        self.process_priority_entry.grid(row=4, column=3, padx=5, pady=5)
        
        self.add_button = ttk.Button(self.process_frame, text="Add Process", command=self.add_process)
        self.add_button.grid(row=4, column=4, padx=5, pady=5)
        
        self.algorithm_frame = ttk.Frame(self.master, style="TFrame")
        self.algorithm_frame.pack(padx=10, pady=10)
        
        self.algorithm_label = ttk.Label(self.algorithm_frame, text="Select Algorithm:", style="TLabel")
        self.algorithm_label.grid(row=0, column=0, sticky=tk.W)
        
        self.algorithm_combo = ttk.Combobox(self.algorithm_frame, 
                                            values=["FCFS", "Round Robin", "SJF", "Priority"], 
                                            textvariable=self.selected_algorithm,
                                            style="TCombobox")
        self.algorithm_combo.grid(row=0, column=1, padx=5, pady=5)
        self.algorithm_combo.bind("<<ComboboxSelected>>", self.on_algorithm_selected)
        
        self.schedule_button = ttk.Button(self.master, text="Schedule", command=self.schedule_processes)
        self.schedule_button.pack(padx=10, pady=10)
        
        self.output_frame = ttk.Frame(self.master, style="TFrame")
        self.output_frame.pack(padx=10, pady=10)
        
        self.output_label = ttk.Label(self.output_frame, text="Output:", style="TLabel")
        self.output_label.grid(row=0, column=0, sticky=tk.W)
        
        self.output_text = tk.Text(self.output_frame, width=90, height=10)
        self.output_text.grid(row=1, column=0, padx=5, pady=5)
        self.output_text.configure(state="disabled")
        
        self.gantt_frame = ttk.Frame(self.master, style="TFrame")
        self.gantt_frame.pack(padx=10, pady=10)
        
    def add_process(self):
        name = self.process_name_entry.get()
        arrival_time = int(self.process_arrival_entry.get())
        burst_time = int(self.process_burst_entry.get())
        priority = int(self.process_priority_entry.get())
        process = Process(name, arrival_time, burst_time, priority)
        self.processes.append(process)
        self.update_process_listbox()
        self.process_name_entry.delete(0, tk.END)
        self.process_arrival_entry.delete(0, tk.END)
        self.process_burst_entry.delete(0, tk.END)
        self.process_priority_entry.delete(0, tk.END)
        self.process_name_entry.focus_set()
        
    def remove_process(self):
        selected_index = self.process_listbox.curselection()
        if selected_index:
            del self.processes[selected_index[0]]
            self.update_process_listbox()
        
    def edit_process(self):
        selected_index = self.process_listbox.curselection()
        if selected_index:
            process = self.processes[selected_index[0]]
            process.name = self.process_name_entry.get()
            process.arrival_time = int(self.process_arrival_entry.get())
            process.burst_time = int(self.process_burst_entry.get())
            process.priority = int(self.process_priority_entry.get())
            self.update_process_listbox()
        
    def update_process_listbox(self):
        self.process_listbox.delete(0, tk.END)
        for i, process in enumerate(self.processes, start=1):
            self.process_listbox.insert(tk.END, f"Process {i}: {process.name}")
        
    def on_process_selected(self, event):
        selected_index = self.process_listbox.curselection()
        if selected_index:
            process = self.processes[selected_index[0]]
            self.process_name_entry.delete(0, tk.END)
            self.process_name_entry.insert(0, process.name)
            self.process_arrival_entry.delete(0, tk.END)
            self.process_arrival_entry.insert(0, str(process.arrival_time))
            self.process_burst_entry.delete(0, tk.END)
            self.process_burst_entry.insert(0, str(process.burst_time))
            self.process_priority_entry.delete(0, tk.END)
            self.process_priority_entry.insert(0, str(process.priority))
        
    def on_algorithm_selected(self, event):
        algorithm = self.selected_algorithm.get()
        print(f"Algorithm selected: {algorithm}")

    def schedule_processes(self):
        algorithm = self.selected_algorithm.get()
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", tk.END)  # Clearing the text widget
        if algorithm == "Round Robin":
            scheduler = RRScheduler()
        elif algorithm == "FCFS":
            scheduler = FCFSScheduler()
        elif algorithm == "SJF":
            scheduler = SJFScheduler()
        elif algorithm == "Priority":
            scheduler = PriorityScheduler()
        scheduling_output = scheduler.schedule(self.processes)
        self.output_text.insert(tk.END, scheduling_output)
        self.output_text.configure(state="disabled")
        self.plot_gantt_chart(scheduler)

    def plot_gantt_chart(self, scheduler):
        fig, ax = plt.subplots()
        cmap = plt.get_cmap('tab10')
        prc_sch = scheduler.get_process_schedule()
        colors = cmap(np.linspace(0, 1, len(prc_sch)))

        # Plot each process as a bar in the Gantt chart
        for i, (start_time, end_time, process_name) in enumerate(prc_sch):
            ax.barh(i, end_time - start_time, left=start_time, color=colors[i], label=f'{process_name}')

        # Format the chart
        ax.set_xlabel('Time')
        ax.set_ylabel('Processes')
        ax.set_title('Gantt Chart')
        ax.set_yticks(np.arange(len(prc_sch)))
        ax.set_yticklabels([f'{process_name}' for _, _, process_name in prc_sch])
        ax.legend(loc='upper right')
        ax.grid(True)
        plt.tight_layout()

        for widget in self.gantt_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.gantt_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
