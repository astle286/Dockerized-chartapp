import os
import datetime
import socket
import psutil
import pandas as pd
import plotly.express as px
import plotly.subplots as sp

from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

# Prometheus integration
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, Gauge

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Prometheus metrics setup
metrics = PrometheusMetrics(app)

# Custom metrics
uploads_total = Counter("chartapp_uploads_total", "Total uploaded files")
active_sessions = Gauge("chartapp_active_sessions", "Active user sessions")


@app.route("/", methods=["GET", "POST"])
def index():
    chart_html_a, chart_html_b = None, None
    columns, preview_html, full_html = [], None, None

    if request.method == "POST":
        # Reset dataset
        if "reset" in request.form:
            session.pop("last_file", None)
            active_sessions.dec()  # reduce active session count
            return redirect(url_for("index"))

        # Upload file (only once per session)
        file = request.files.get("datafile")
        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            session["last_file"] = filepath
            uploads_total.inc()  # increment uploads counter
            active_sessions.inc()  # increment active session count

        # Chart A config
        chart_type_a = request.form.get("charttype_a")
        xcol_a = request.form.get("xcol_a")
        ycols_a = request.form.getlist("ycol_a")

        # Chart B config
        chart_type_b = request.form.get("charttype_b")
        xcol_b = request.form.get("xcol_b")
        ycols_b = request.form.getlist("ycol_b")

        # Theme toggle
        theme = request.form.get("theme") or "plotly"

        # If dataset exists
        if "last_file" in session:
            try:
                df = pd.read_csv(session["last_file"])
            except Exception as e:
                return f"Error reading CSV: {e}", 400

            columns = df.columns.tolist()

            # Limited preview (10 rows × 10 columns)
            limited_df = df.iloc[:10, :10]
            preview_html = limited_df.to_html(
                classes="table table-striped table-bordered table-sm",
                index=False,
                table_id="previewTableLimited",
            )

            # Full dataset table
            full_html = df.to_html(
                classes="table table-striped table-bordered table-sm",
                index=False,
                table_id="previewTableFull",
            )

            # Chart A
            if chart_type_a and xcol_a and ycols_a:
                fig_a = None
                if chart_type_a == "line":
                    fig_a = px.line(df, x=xcol_a, y=ycols_a, title="Chart A - Line", template=theme)
                elif chart_type_a == "bar":
                    fig_a = px.bar(df, x=xcol_a, y=ycols_a, title="Chart A - Bar", template=theme)
                elif chart_type_a == "scatter":
                    fig_a = px.scatter(df, x=xcol_a, y=ycols_a[0], title="Chart A - Scatter", template=theme)
                    for y in ycols_a[1:]:
                        extra = px.scatter(df, x=xcol_a, y=y, title=f"{y} vs {xcol_a}", template=theme)
                        for trace in extra.data:
                            fig_a.add_trace(trace)
                elif chart_type_a == "pie":
                    fig_a = sp.make_subplots(rows=1, cols=len(ycols_a), specs=[[{"type": "domain"}] * len(ycols_a)])
                    for i, y in enumerate(ycols_a):
                        pie = px.pie(df, names=xcol_a, values=y, title=f"{y} by {xcol_a}", template=theme)
                        for trace in pie.data:
                            fig_a.add_trace(trace, row=1, col=i + 1)
                if fig_a:
                    chart_html_a = fig_a.to_html(full_html=False, include_plotlyjs="cdn")

            # Chart B
            if chart_type_b and xcol_b and ycols_b:
                fig_b = None
                if chart_type_b == "line":
                    fig_b = px.line(df, x=xcol_b, y=ycols_b, title="Chart B - Line", template=theme)
                elif chart_type_b == "bar":
                    fig_b = px.bar(df, x=xcol_b, y=ycols_b, title="Chart B - Bar", template=theme)
                elif chart_type_b == "scatter":
                    fig_b = px.scatter(df, x=xcol_b, y=ycols_b[0], title="Chart B - Scatter", template=theme)
                    for y in ycols_b[1:]:
                        extra = px.scatter(df, x=xcol_b, y=y, title=f"{y} vs {xcol_b}", template=theme)
                        for trace in extra.data:
                            fig_b.add_trace(trace)
                elif chart_type_b == "pie":
                    fig_b = sp.make_subplots(rows=1, cols=len(ycols_b), specs=[[{"type": "domain"}] * len(ycols_b)])
                    for i, y in enumerate(ycols_b):
                        pie = px.pie(df, names=xcol_b, values=y, title=f"{y} by {xcol_b}", template=theme)
                        for trace in pie.data:
                            fig_b.add_trace(trace, row=1, col=i + 1)
                if fig_b:
                    chart_html_b = fig_b.to_html(full_html=False, include_plotlyjs="cdn")

    return render_template(
        "index.html",
        chart_a=chart_html_a,
        chart_b=chart_html_b,
        columns=columns,
        preview=preview_html,
        full_table=full_html,
    )


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for dashboard monitoring"""
    status = {
        "app": "ChartApp",
        "status": "running",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "host": socket.gethostname(),
        "cpu_percent": psutil.cpu_percent(interval=0.5),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
        "debug": app.debug,
    }
    return jsonify(status), 200


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    # Debug mode ON for development, switch OFF in production
    app.run(host="0.0.0.0", port=8000, debug=True)
