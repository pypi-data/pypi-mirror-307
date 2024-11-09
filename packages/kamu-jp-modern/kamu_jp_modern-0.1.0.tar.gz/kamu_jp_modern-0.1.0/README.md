# Modern

Modern is a simple package for logging and progress bar and More!

## Installation

```bash
pip install Modern
```

## Usage

```python
from Modern import Modern
```

### Logging

```python
logger = Modern.Modern().modernLogging(process_name="main")
logger.log("This is a test message", "INFO")
```

### Progress Bar

```python
progress_bar = Modern.Modern().modernProgressBar(total=100, process_name="Task 1", process_color=32)
progress_bar.start()
```
