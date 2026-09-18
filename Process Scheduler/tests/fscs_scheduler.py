
class FCFSScheduler:
    def __init__(self):
        self.current_time = 0
        self.total_waiting_time = 0
        self.total_turnaround_time = 0
        self.process_schedule = []  # Stores (start_time, end_time, process_name) for Gantt chart

    def schedule(self, processes):
        if not processes:
            return "No processes to schedule"  # Return a message if there are no processes

        processes.sort(key=lambda x: x.arrival_time)  # Sort processes by arrival time
        
        scheduling_output = "Process ID\t\tArrival Time\t\tBurst Time\t\tWaiting Time\t\tTurnaround Time\n"
        
        for process in processes:
            # Calculate waiting time and turnaround time
            start_time = max(self.current_time, process.arrival_time)  # Start time after previous process or arrival
            waiting_time = start_time - process.arrival_time
            self.total_waiting_time += waiting_time

            turnaround_time = waiting_time + process.burst_time
            self.total_turnaround_time += turnaround_time

            # Update current time and save schedule data for Gantt chart
            end_time = start_time + process.burst_time
            self.process_schedule.append((start_time, end_time, process.name))
            self.current_time = end_time

            # Update scheduling output
            scheduling_output += f"{process.name}\t\t{process.arrival_time}\t\t{process.burst_time}\t\t{waiting_time}\t\t{turnaround_time}\n"
        
        avg_waiting_time = self.total_waiting_time / len(processes)
        avg_turnaround_time = self.total_turnaround_time / len(processes)
        
        scheduling_output += f"\nAverage Waiting Time: {avg_waiting_time:.2f}\n"
        scheduling_output += f"Average Turnaround Time: {avg_turnaround_time:.2f}\n"
        
        return scheduling_output  # Return the scheduling output as a string

    def get_process_schedule(self):
        return self.process_schedule