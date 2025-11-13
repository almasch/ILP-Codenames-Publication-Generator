from invoke import task

import logging
from rich.logging import RichHandler

# noinspection PyUnresolvedReferences
from task_modules.allow_noise import allow_noise

# noinspection PyUnresolvedReferences
from task_modules.normal import normal

# noinspection PyUnresolvedReferences
from task_modules.combined_knowledge_tree import combined_knowledge_tree

# noinspection PyUnresolvedReferences
from task_modules.reset import reset

# noinspection PyUnresolvedReferences
from task_modules.induce import induce

# noinspection PyUnresolvedReferences
from task_modules.clean import clean


# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,  # Globaler Level: DEBUG, INFO, WARNING, ERROR
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("generator")

@task(default=True)
def all(ctx):
    """
    Resets all workspaces, generates all aleph experiments and runs the induction.
    """
    ctx.run("invoke reset")
    ctx.run("invoke normal")
    ctx.run("invoke allow_noise")
    ctx.run("invoke combined")
    ctx.run("invoke induce")
