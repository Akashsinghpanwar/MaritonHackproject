from __future__ import annotations

import shutil
from pathlib import Path
import gradio as gr
import sys

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from sami.app.rag import add_files, query, clear_index
    from sami.app.settings import UPLOAD_DIR, DATA_DIR
else:
    from .rag import add_files, query, clear_index
    from .settings import UPLOAD_DIR, DATA_DIR

def load_samples():
    sample_dir = DATA_DIR / "sample"
    files = []
    for name in ("CP.md", "SOF.md"):
        p = sample_dir / name
        if p.exists():
            dst = UPLOAD_DIR / p.name
            shutil.copyfile(p, dst)
            files.append(str(dst))
    add_files(files)
    return f"Ingested samples: {', '.join(Path(f).name for f in files)}"

def ingest(files):
    paths = []
    if files:
        for f in files:
            src = getattr(f, "name", None) or f
            paths.append(src)
    n, copied = add_files(paths)
    return f"Ingested {n} file(s): {', '.join(Path(p).name for p in copied)}"

def ask(q):
    if not q or not q.strip():
        return "Please type a question.", ""
    ans, cites = query(q.strip())
    cite_str = ", ".join(cites) if cites else ""
    return ans, cite_str

def reset_index():
    clear_index(delete_uploads=False)
    return "Index cleared. Upload or load samples again."

with gr.Blocks(title="Maritime Virtual Assistant") as demo:
    gr.Markdown("# Maritime Virtual Assistant (RAG + Azure DI)")

    with gr.Tab("Chat"):
        with gr.Row():
            question = gr.Textbox(label="Ask a question", placeholder="e.g., Summarize laytime terms and demurrage...")
        with gr.Row():
            ask_btn = gr.Button("Ask", variant="primary")
            reset_btn = gr.Button("Clear Index")
        with gr.Row():
            answer = gr.Textbox(label="Answer", lines=12)
        with gr.Row():
            citations = gr.Textbox(label="Citations (filenames)")

    with gr.Tab("Docs"):
        with gr.Row():
            upload = gr.Files(label="Upload PDFs/Images/Markdown", file_count="multiple")
        with gr.Row():
            ingest_btn = gr.Button("Ingest Uploads", variant="primary")
            samples_btn = gr.Button("Load Samples")
        with gr.Row():
            status = gr.Textbox(label="Status")

    with gr.Tab("Tools"):
        gr.Markdown("### Distance / ETA (Simple)")
        with gr.Row():
            from_port = gr.Textbox(label="From (lat,lon)", value="1.3521,103.8198  # Singapore")
            to_port = gr.Textbox(label="To (lat,lon)", value="25.1288,56.3265   # Fujairah")
            speed = gr.Number(label="Speed (kn)", value=13.0)
        with gr.Row():
            calc_btn = gr.Button("Compute Distance/ETA")
            dist_nm = gr.Textbox(label="Distance (NM)")
            days = gr.Textbox(label="Days")
        gr.Markdown("*(Integrate to a richer port DB as needed.)*")

        def compute_dist_eta(a, b, v):
            try:
                alat, alon = [float(x.strip()) for x in a.split(",")]
                blat, blon = [float(x.strip()) for x in b.split(",")]
                R = 3440.065  # NM
                from math import radians, sin, cos, asin, sqrt
                dlat = radians(blat - alat)
                dlon = radians(blon - alon)
                lat1 = radians(alat); lat2 = radians(blat)
                h = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
                d = 2*R*asin(sqrt(h))
                tdays = d / (24.0 * float(v))
                return f"{d:.1f}", f"{tdays:.2f}"
            except Exception as e:
                return f"Error: {e}", ""

        calc_btn.click(compute_dist_eta, inputs=[from_port, to_port, speed], outputs=[dist_nm, days])

    ask_btn.click(ask, inputs=[question], outputs=[answer, citations])
    reset_btn.click(reset_index, outputs=[status])
    ingest_btn.click(ingest, inputs=[upload], outputs=[status])
    samples_btn.click(load_samples, outputs=[status])

if __name__ == "__main__":
    demo.launch()
