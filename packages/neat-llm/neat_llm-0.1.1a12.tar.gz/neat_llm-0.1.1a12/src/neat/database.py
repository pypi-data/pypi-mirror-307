import sqlite3
from contextlib import contextmanager
from typing import Generator

from loguru import logger

from neat.config import settings
from neat.models import ExecutionData, PromptData


@contextmanager
def db_connection() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(settings.db_file)
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    with db_connection() as conn:
        cursor = conn.cursor()

        # Check if prompts table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='prompts'")
        if not cursor.fetchone():
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                func_name TEXT,
                version INTEGER,
                hash TEXT,
                model TEXT,
                temperature REAL,
                prompt TEXT,
                environment TEXT,
                UNIQUE(func_name, version)
            )
            """)
            logger.debug("Created prompts table")

        # Check if executions table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='executions'")
        if not cursor.fetchone():
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                version_id INTEGER,
                prompt_tokens INTEGER,
                completion_tokens INTEGER,
                execution_time REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (version_id) REFERENCES prompts (id)
            )
            """)
            logger.debug("Created executions table")

        conn.commit()
    logger.debug("Database initialization complete")


def load_prompt(func_name: str, version: int | None = None) -> PromptData | None:
    with db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if version is None:
            cursor.execute(
                "SELECT * FROM prompts WHERE func_name = ? ORDER BY version DESC LIMIT 1",
                (func_name,),
            )
        else:
            cursor.execute(
                "SELECT * FROM prompts WHERE func_name = ? AND version = ?",
                (func_name, version),
            )
        result = cursor.fetchone()
    if result:
        logger.debug(f"Loaded prompt for {func_name}")
        return PromptData(**result)
    logger.debug(f"No prompt found for {func_name}")
    return None


def save_prompt(prompt_data: PromptData) -> int:
    with db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO prompts
                (func_name, version, hash, model, temperature, prompt, environment)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    prompt_data.func_name,
                    prompt_data.version,
                    prompt_data.hash,
                    prompt_data.model,
                    prompt_data.temperature,
                    prompt_data.prompt,
                    prompt_data.environment,
                ),
            )
        except sqlite3.IntegrityError:
            prompt_data.version += 1
            return save_prompt(prompt_data)

        prompt_id = cursor.lastrowid
        conn.commit()
    logger.debug(f"Saved prompt version {prompt_data.version} for {prompt_data.func_name}")
    return prompt_id


def save_execution(execution_data: ExecutionData) -> None:
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO executions
            (version_id, prompt_tokens, completion_tokens, execution_time)
            VALUES (?, ?, ?, ?)
            """,
            (
                execution_data.version_id,
                execution_data.prompt_tokens,
                execution_data.completion_tokens,
                execution_data.execution_time,
            ),
        )
        conn.commit()
    logger.debug(f"Saved execution for version_id {execution_data.version_id}")


init_db()
