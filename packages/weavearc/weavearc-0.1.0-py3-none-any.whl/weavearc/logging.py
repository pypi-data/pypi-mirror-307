"""Módulo de configuração de logging do app"""

from loguru import logger as loguru_logger
from rich.console import Console
from rich.theme import Theme
from rich.traceback import install as install_rich_traceback

# Install rich traceback handling
install_rich_traceback(show_locals=False)

# Create a custom theme for our logs
custom_theme = Theme(
    {
        "debug": "dim cyan",
        "info": "bold cyan",
        "success": "bold green",
        "warning": "bold yellow",
        "error": "bold red",
        "critical": "bold white on red",
    }
)

# Create a Rich console with our custom theme
console = Console(theme=custom_theme)

# Define a base log format for Loguru
LOGURU_FORMAT = "<level>{level: <8}</level> | <cyan>{time:YYYY-MM-DD HH:mm:ss}</cyan> | <level>{message}</level>"


# Custom sink function to use Rich for output
def rich_sink(message) -> None:  # type: ignore
    record = message.record
    level_name = record["level"].name.lower()
    level_color = level_name

    log_message = (
        f"[{level_color}]{level_name.upper():<8}[/{level_color}] | "
        f"[cyan]{record['time'].strftime('%Y-%m-%d %H:%M:%S')}[/cyan] | "
        f"[{level_color}]{record['message']}[/{level_color}]"
    )

    console.print(log_message, markup=True)

    # Print the exception traceback for logger.exception calls
    if record["exception"]:
        console.print_exception(
            show_locals=False, width=100, extra_lines=3, word_wrap=True
        )


# Function to get the configured logger
def get_logger():  # type: ignore
    # Remove the default logger
    loguru_logger.remove()

    # Add our custom Rich sink
    loguru_logger.add(
        rich_sink,
        level="DEBUG",  # Changed to DEBUG to allow all levels
        colorize=False,
        format=LOGURU_FORMAT,
        backtrace=True,
        diagnose=True,
        catch=True,
    )

    return loguru_logger


# Use this logger in your application
logger = get_logger()
