import threading
import time
from datetime import datetime, timedelta
from typing import Callable, Any, Dict, List, Optional
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Job:
    """Represents a scheduled job."""
    id: int
    func: Callable
    args: tuple
    kwargs: dict
    interval: Optional[timedelta] = None  # For interval-based jobs
    at_time: Optional[str] = None        # For daily jobs at specific time (HH:MM)
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    enabled: bool = True

class CustomScheduler:
    """Custom scheduler implementation for managing periodic tasks."""
    
    def __init__(self):
        self._jobs: Dict[int, Job] = {}
        self._job_counter = 0
        self._lock = threading.Lock()
        self._running = False
        self._thread = None

    def _get_next_job_id(self) -> int:
        """Generate unique job ID."""
        with self._lock:
            self._job_counter += 1
            return self._job_counter

    def _calculate_next_run(self, job: Job) -> datetime:
        """Calculate the next run time for a job."""
        now = datetime.now()
        
        if job.interval:
            # For interval-based jobs
            if not job.last_run:
                return now
            return job.last_run + job.interval
            
        elif job.at_time:
            # For daily jobs at specific time
            hour, minute = map(int, job.at_time.split(':'))
            next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # If the time has already passed today, schedule for tomorrow
            if next_run <= now:
                next_run += timedelta(days=1)
                
            return next_run
            
        return now

    def add_interval_job(
        self,
        func: Callable,
        interval: timedelta,
        *args,
        **kwargs
    ) -> int:
        """
        Add an interval-based job.
        
        Args:
            func: Function to execute
            interval: Time interval between executions
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            int: Job ID
        """
        job_id = self._get_next_job_id()
        job = Job(
            id=job_id,
            func=func,
            args=args,
            kwargs=kwargs,
            interval=interval
        )
        job.next_run = self._calculate_next_run(job)
        
        with self._lock:
            self._jobs[job_id] = job
            
        return job_id

    def add_daily_job(
        self,
        func: Callable,
        at_time: str,
        *args,
        **kwargs
    ) -> int:
        """
        Add a job to run daily at specific time.
        
        Args:
            func: Function to execute
            at_time: Time in 'HH:MM' format
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            int: Job ID
        """
        # Validate time format
        try:
            hour, minute = map(int, at_time.split(':'))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError
        except ValueError:
            raise ValueError("Invalid time format. Use 'HH:MM' (24-hour format)")

        job_id = self._get_next_job_id()
        job = Job(
            id=job_id,
            func=func,
            args=args,
            kwargs=kwargs,
            at_time=at_time
        )
        job.next_run = self._calculate_next_run(job)
        
        with self._lock:
            self._jobs[job_id] = job
            
        return job_id

    def remove_job(self, job_id: int) -> bool:
        """Remove a job by ID."""
        with self._lock:
            return bool(self._jobs.pop(job_id, None))

    def enable_job(self, job_id: int) -> bool:
        """Enable a job."""
        with self._lock:
            if job := self._jobs.get(job_id):
                job.enabled = True
                job.next_run = self._calculate_next_run(job)
                return True
            return False

    def disable_job(self, job_id: int) -> bool:
        """Disable a job."""
        with self._lock:
            if job := self._jobs.get(job_id):
                job.enabled = False
                return True
            return False

    def _run_pending(self):
        """Execute pending jobs."""
        now = datetime.now()
        
        with self._lock:
            for job in self._jobs.values():
                if not job.enabled or not job.next_run:
                    continue
                    
                if now >= job.next_run:
                    try:
                        job.func(*job.args, **job.kwargs)
                        job.last_run = now
                        job.next_run = self._calculate_next_run(job)
                    except Exception as e:
                        logger.error(f"Error executing job {job.id}: {str(e)}")

    def start(self):
        """Start the scheduler in a background thread."""
        if self._thread and self._thread.is_alive():
            return
            
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the scheduler."""
        self._running = False
        if self._thread:
            self._thread.join()
            self._thread = None

    def _run_loop(self):
        """Main scheduler loop."""
        while self._running:
            self._run_pending()
            time.sleep(1)  # Check every second

    def get_jobs(self) -> List[Dict[str, Any]]:
        """Get list of all jobs and their status."""
        with self._lock:
            return [
                {
                    'id': job.id,
                    'enabled': job.enabled,
                    'last_run': job.last_run,
                    'next_run': job.next_run,
                    'interval': job.interval,
                    'at_time': job.at_time
                }
                for job in self._jobs.values()
            ]

    def clear(self):
        """Remove all jobs."""
        with self._lock:
            self._jobs.clear() 