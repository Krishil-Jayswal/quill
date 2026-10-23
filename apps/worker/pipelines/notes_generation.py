import os
import json
from config import settings
from natsort import natsorted
from schemas import Transcript
from rich.table import Table
from rich.console import Console
from prompts import notes_generation_system_prompt
from ollama import Client, Options, Message, ChatResponse

console = Console()


def notes_generation_pipeline(
    base_dir: str, transcript_file: str, ocr_artifacts_dir: str
):
    notes_artifacts_dir = os.path.join(base_dir, "notes")
    notes_file = os.path.join(notes_artifacts_dir, "notes.md")
    content_file = os.path.join(notes_artifacts_dir, "content.md")
    os.makedirs(notes_artifacts_dir, exist_ok=True)
    ocr_artifacts = natsorted(os.listdir(ocr_artifacts_dir))
    with open(transcript_file, encoding="utf-8") as f:
        transcript = Transcript(**json.load(f))

    content = ""
    transcript_idx = 0
    total_segments = len(transcript.segments)
    model = "gpt-oss:120b"
    options = Options(num_ctx=131072, num_predict=65536)

    console.rule("[bold green] Starting Notes Generation Pipeline")
    console.print(f"Model: [magenta]{model}")

    for frame in ocr_artifacts:
        timestamp = int(frame.split(".")[0].split("_")[-1])
        content += "# Transcript \n"
        while (
            transcript_idx < total_segments
            and transcript.segments[transcript_idx].end <= timestamp
        ):
            content += transcript.segments[transcript_idx].text
            transcript_idx += 1
        content += "\n# OCR \n"
        with open(os.path.join(ocr_artifacts_dir, frame), encoding="utf-8") as f:
            content += f"{f.read()}\n"

    ollama = Client(
        host="https://ollama.com",
        headers={"Authorization": f"Bearer {settings.OLLAMA_API_KEY}"},
    )
    res: ChatResponse = ollama.chat(
        model=model,
        messages=[
            Message(role="system", content=notes_generation_system_prompt),
            Message(role="user", content=content),
        ],
        options=options,
    )

    with open(content_file, "w", encoding="utf-8") as f:
        f.write(content)
    with open(notes_file, "w", encoding="utf-8") as f:
        f.write(res.message.content or "")

    console.rule("[bold blue] Notes Generation Summary")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right")

    table.add_row("Content File", content_file)
    table.add_row("Notes File", notes_file)
    console.print(table)

    console.rule("[bold green] Notes Generation Pipeline Completed\n\n")

    return notes_artifacts_dir
