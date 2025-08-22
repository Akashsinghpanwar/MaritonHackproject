from __future__ import annotations

import shutil
from pathlib import Path
import gradio as gr

from app.rag import add_files, query, clear_index
from app.settings import UPLOAD_DIR, DATA_DIR
from app.tools.distance import distance_nm, eta_days
from app.tools.laytime import compute_laytime, CP, Event
from app.tools.weather import forecast_latlon
import json
from datetime import datetime

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
    gr.Markdown("# Maritime Virtual Assistant (RAG + LlamaParse)")

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
        with gr.Accordion("Distance / ETA", open=True):
            gr.Markdown("### Distance / ETA (Simple)")
            with gr.Row():
                from_port = gr.Textbox(label="From (lat,lon)", value="1.3521,103.8198  # Singapore")
                to_port = gr.Textbox(label="To (lat,lon)", value="25.1288,56.3265   # Fujairah")
                speed = gr.Number(label="Speed (kn)", value=13.0)
            with gr.Row():
                dist_calc_btn = gr.Button("Compute Distance/ETA")
                dist_nm_out = gr.Textbox(label="Distance (NM)")
                days_out = gr.Textbox(label="Days")
            gr.Markdown("*(Integrate to a richer port DB as needed.)*")

        with gr.Accordion("Laytime Calculator", open=False):
            gr.Markdown("### Laytime Calculator")
            with gr.Row():
                laytime_hours_in = gr.Number(label="Laytime (hours)", value=72)
                demurrage_in = gr.Number(label="Demurrage ($/day)", value=15000)
                despatch_in = gr.Number(label="Despatch ($/day)", value=7500)
            with gr.Row():
                events_in = gr.Textbox(label="Events (JSON list of [start, end, reason, excepted])", lines=5, value='[["2024-01-01 09:00", "2024-01-03 12:00", "Cargo Ops", false]]')
            with gr.Row():
                laytime_calc_btn = gr.Button("Calculate Laytime")
                used_hours_out = gr.Textbox(label="Used Hours")
                demurrage_out = gr.Textbox(label="Demurrage ($)")
                despatch_out = gr.Textbox(label="Despatch ($)")

        with gr.Accordion("Weather Forecast", open=False):
            gr.Markdown("### Weather Forecast (OpenWeather)")
            with gr.Row():
                weather_lat_in = gr.Textbox(label="Latitude", value="25.1288")
                weather_lon_in = gr.Textbox(label="Longitude", value="56.3265")
            with gr.Row():
                weather_btn = gr.Button("Get Forecast")
                weather_out = gr.JSON(label="Forecast")

        def compute_dist_eta_ui(a, b, v):
            try:
                alat, alon = [float(x.strip()) for x in a.split(",")]
                blat, blon = [float(x.strip()) for x in b.split(",")]
                dist = distance_nm(alat, alon, blat, blon)
                tdays = eta_days(dist, float(v))
                return f"{dist:.1f}", f"{tdays:.2f}"
            except Exception as e:
                return f"Error: {e}", ""

        def compute_laytime_ui(laytime_h, demurrage, despatch, events_str):
            try:
                cp = CP(laytime_hours=laytime_h, demurrage_per_day=demurrage, despatch_per_day=despatch)
                events_data = json.loads(events_str)
                events = [Event(start=datetime.fromisoformat(e[0]), end=datetime.fromisoformat(e[1]), reason=e[2], excepted=e[3]) for e in events_data]
                used_h, dem, desp = compute_laytime(cp, events)
                return f"{used_h:.2f}", f"{dem:.2f}", f"{desp:.2f}"
            except Exception as e:
                return f"Error: {e}", "", ""

        def get_weather_ui(lat, lon):
            try:
                lat, lon = float(lat), float(lon)
                forecast = forecast_latlon(lat, lon)
                return forecast
            except Exception as e:
                return {"error": str(e)}

        dist_calc_btn.click(compute_dist_eta_ui, inputs=[from_port, to_port, speed], outputs=[dist_nm_out, days_out])
        laytime_calc_btn.click(compute_laytime_ui, inputs=[laytime_hours_in, demurrage_in, despatch_in, events_in], outputs=[used_hours_out, demurrage_out, despatch_out])
        weather_btn.click(get_weather_ui, inputs=[weather_lat_in, weather_lon_in], outputs=[weather_out])

    ask_btn.click(ask, inputs=[question], outputs=[answer, citations])
    reset_btn.click(reset_index, outputs=[status])
    ingest_btn.click(ingest, inputs=[upload], outputs=[status])
    samples_btn.click(load_samples, outputs=[status])

if __name__ == "__main__":
    demo.launch()
