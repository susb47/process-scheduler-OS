class SJFScheduler:
    def __init__(self):
        self.current_time = 0
        self.total_waiting_time = 0
        self.total_turnaround_time = 0
        self.process_schedule = []  # To store (start_time, end_time, process_name)

    def schedule(self, processes):
        if not processes:
            return "No processes to schedule"

        # Sort processes initially by arrival time (to process them in order of arrival)
        processes.sort(key=lambda x: x.arrival_time)
        completed_processes = []  # To track completed processes
        
        scheduling_output = "Process ID\tArrival Time\tBurst Time\tWaiting Time\tTurnaround Time\n"
        
        while len(completed_processes) < len(processes):
            # Get processes that have arrived by the current time
            ready_queue = [p for p in processes if p.arrival_time <= self.current_time and p not in completed_processes]
            
            if not ready_queue:
                # If no process is ready, increment the current time to the next process arrival
                self.current_time = min(p.arrival_time for p in processes if p not in completed_processes)
                continue

            # Select the process with the shortest burst time
            shortest_job = min(ready_queue, key=lambda p: p.burst_time)
            
            # Calculate times
            start_time = self.current_time
            waiting_time = start_time - shortest_job.arrival_time
            self.total_waiting_time += waiting_time

            turnaround_time = waiting_time + shortest_job.burst_time
            self.total_turnaround_time += turnaround_time

            # Update the schedule and current time
            end_time = start_time + shortest_job.burst_time
            self.process_schedule.append((start_time, end_time, shortest_job.name))
            self.current_time = end_time

            # Add the completed process to the completed list
            completed_processes.append(shortest_job)

            # Update output
            scheduling_output += f"{shortest_job.name}\t\t{shortest_job.arrival_time}\t\t{shortest_job.burst_time}\t\t{waiting_time}\t\t{turnaround_time}\n"

        # Calculate average times
        avg_waiting_time = self.total_waiting_time / len(processes)
        avg_turnaround_time = self.total_turnaround_time / len(processes)

        scheduling_output += f"\nAverage Waiting Time: {avg_waiting_time:.2f}\n"
        scheduling_output += f"Average Turnaround Time: {avg_turnaround_time:.2f}\n"
        
        return scheduling_output

    def plot_gantt_chart(self):
        import matplotlib.pyplot as plt
        import numpy as np
        
        if not self.process_schedule:
            print("No processes scheduled. Run the scheduler first.")
            return

        fig, ax = plt.subplots()
        cmap = plt.get_cmap('tab10')
        colors = cmap(np.linspace(0, 1, len(self.process_schedule)))

        # Plot each process as a bar in the Gantt chart
        for i, (start_time, end_time, process_name) in enumerate(self.process_schedule):
            ax.barh(i, end_time - start_time, left=start_time, color=colors[i], label=f'{process_name}')

        # Format the chart
        ax.set_xlabel('Time')
        ax.set_ylabel('Processes')
        ax.set_title('Gantt Chart')
        ax.set_yticks(np.arange(len(self.process_schedule)))
        ax.set_yticklabels([f'{name}' for _, _, name in self.process_schedule])
        ax.legend(loc='upper right')
        ax.grid(True)
        plt.tight_layout()
        plt.show()
