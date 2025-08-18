from jinja2 import Template
from pathlib import Path
import pandas as pd

TEMPLATE = """# ADC Optimizer Report

Top {{n}} designs:

| rank | glass1 | glass2 | chromatic_rms_arcsec | pupil_wobble_arcsec | throughput_loss |
|---:|---|---|---:|---:|---:|
{% for i,row in rows.iterrows() %}
| {{loop.index}} | {{row.glass1}} | {{row.glass2}} | {{'%.3f' % row.chromatic_residual}} | {{'%.3f' % row.pupil_wobble}} | {{'%.3g' % row.throughput_loss}} |
{% endfor %}
"""

def save_markdown(df: pd.DataFrame, out_path: str, topn: int = 20):
    rows = df.head(topn).reset_index(drop=True)
    md = Template(TEMPLATE).render(n=topn, rows=rows)
    Path(out_path).write_text(md)
