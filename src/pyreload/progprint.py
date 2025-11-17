"""
Simple progress printer without external dependencies.
"""

import sys


class ProgressPrinter:
    """Simple progress printer that displays (current%/total%)"""
    
    def __init__(self, total, width = 50, show_percentage = True):
        """
        Initialize progress printer.
        
        Args:
            total: Total number of items
            width: Width of the progress bar (default: 50)
            show_percentage: Whether to show percentage (default: True)
        """
        self.total = total
        self.current = 0
        self.width = width
        self.show_percentage = show_percentage
        
    def update(self, n=1):
        """
        Update progress by n steps.
        
        Args:
            n: Number of steps to increment (default: 1)
        """
        self.current += n
        self._print_progress()
        
    def set_progress(self, current):
        """
        Set progress to a specific value.
        
        Args:
            current: Current progress value
        """
        self.current = current
        self._print_progress()
        
    def _print_progress(self):
        """Print the progress bar to stdout."""
        if self.total == 0:
            percentage = 100
        else:
            percentage = min(100, (self.current / self.total) * 100)
        
        filled_width = int(self.width * self.current / self.total) if self.total > 0 else self.width
        filled_width = min(filled_width, self.width)
        
        bar = '█' * filled_width + '░' * (self.width - filled_width)
        
        if self.show_percentage:
            progress_text = f'\r[{bar}] ({self.current}/{self.total}) {percentage:.1f}%'
        else:
            progress_text = f'\r[{bar}] ({self.current}/{self.total})'
        
        sys.stdout.write(progress_text)
        sys.stdout.flush()
        
        if self.current >= self.total:
            sys.stdout.write('\n')
            sys.stdout.flush()
    
    def finish(self):
        """Mark progress as complete."""
        self.current = self.total
        self._print_progress()


def print_progress(current, total):
    """
    Simple function to print progress in (current/total) format.
    
    Args:
        current: Current progress value
        total: Total value
    
    Example:
        >>> for i in range(1, 101):
        >>>     print_progress(i, 100)
        >>>     time.sleep(0.01)
    """
    percentage = (current / total * 100) if total > 0 else 100
    sys.stdout.write(f'\r({current}/{total}) {percentage:.1f}%')
    sys.stdout.flush()
    
    if current >= total:
        sys.stdout.write('\n')
        sys.stdout.flush()


if __name__ == "__main__":
    import time
    
    print("Example 1: Simple function")
    for i in range(1, 101):
        print_progress(i, 100)
        time.sleep(0.01)
    
    print("\nExample 2: Progress bar class")
    progress = ProgressPrinter(total=100, width=40)
    for i in range(100):
        time.sleep(0.01)
        progress.update(1)
    
    print("\nExample 3: Without percentage")
    progress = ProgressPrinter(total=50, width=30, show_percentage=False)
    for i in range(50):
        time.sleep(0.02)
        progress.update(1)
