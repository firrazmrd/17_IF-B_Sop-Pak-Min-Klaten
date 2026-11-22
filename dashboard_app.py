"""Dashboard baca-saja untuk dataset dan hasil Projek.ipynb."""

import base64
import hashlib
import html
import json
import re
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

ROOT = Path(__file__).resolve().parent
RAW_PATH = ROOT / "data/raw/faostat_rice_producer_prices.csv"
NOTEBOOK_PATH = ROOT / "Projek.ipynb"
RESULTS_PATH = ROOT / "data/results/dashboard_results.json"
PRICE = "Producer Price (LCU/tonne)"
ORANGE = "#bf4e16"
PEACH = "#ffe1cd"
INK = "#282322"
GRAY = "#687078"
LABELS = {0: "Tidak naik", 1: "Naik"}
MODEL = "Random Forest"
BASELINE = "Baseline persistensi arah"

CSS = """
<style>
.stMainBlockContainer {max-width: 1380px; padding-top: 3.8rem; padding-bottom: 3rem;}
[data-testid="stSidebar"] {border-right: 1px solid #eaded4;}
[data-testid="stSidebar"] [role="radiogroup"] {gap: .25rem;}
[data-testid="stSidebar"] [role="radiogroup"] label {
    padding: .42rem .5rem; border-radius: .55rem; width: 100%;
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: #ffe7d8; font-weight: 650;
}
.dash-hero {
    background: linear-gradient(112deg, #fffdfa 30%, #ffe6d4);
    border: 1px solid #efd8c7; border-radius: 1.15rem;
    padding: 1.4rem 1.55rem; margin-bottom: .55rem;
    display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: .75rem;
}
.dash-hero h1 {font-size: clamp(1.85rem, 3vw, 2.65rem); line-height: 1.12; margin: 0 0 .3rem;}
.dash-hero p {margin: 0; color: #625550;}
.dash-period {
    border: 1px solid #edccb6; background: #fff8f1; color: #8e3610;
    border-radius: 999px; padding: .32rem .68rem; font-size: .88rem; font-weight: 650;
}
.dash-metric {
    background: #fffdfb; border: 1px solid #eaded4; border-radius: .85rem;
    padding: .82rem .9rem; min-height: 6rem;
}
.dash-metric p {margin: .18rem 0; color: #655952; font-size: .88rem;}
.dash-metric strong {font-size: clamp(1.3rem, 2.3vw, 1.8rem); color: #a63e12;}
.notebook-table {overflow-x: auto; margin: .5rem 0 1rem;}
.notebook-table table {width: max-content; min-width: 100%; border-collapse: collapse; font-size: .86rem;}
.notebook-table th, .notebook-table td {padding: .38rem .58rem; border-bottom: 1px solid #eee0d6;}
.notebook-table thead {background: #fff0e4;}
</style>
"""


@st.cache_data(show_spinner=False)
def load_data(file_versions: tuple[int, ...]):
    """Load results only when the notebook, export, or CSV changes on disk."""
    csv_bytes = RAW_PATH.read_bytes()
    raw = pd.read_csv(RAW_PATH, dtype={"faostat": "string", "M49 Code": "string", "Item Code": "string"})
    raw["date"] = pd.to_datetime(raw["date"], format="%Y-%m-%d")
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    saved = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    sources = ["".join(cell["source"]) for cell in notebook["cells"] if cell["cell_type"] == "code"]
    if saved["notebook_code_sha256"] != hashlib.sha256(json.dumps(sources, ensure_ascii=False).encode()).hexdigest():
        raise ValueError("Kode notebook sudah berubah. Gunakan ekspor prediksi dari notebook yang sesuai.")
    if saved["dataset_sha256"] != hashlib.sha256(csv_bytes).hexdigest():
        raise ValueError("CSV yang dipakai tidak cocok dengan snapshot hasil klasifikasi.")

    predictions = pd.DataFrame(saved["predictions"])
    predictions["Tahun sasaran"] = pd.to_datetime(predictions["Bulan sasaran"]).dt.year
    project = raw.loc[
        raw["M49 Code"].str.zfill(3).isin(f"{code:03d}" for code in saved["scope"])
        & raw["Item"].eq("Rice")
        & raw["Item Code"].eq("27")
        & raw["Frequency"].eq("Monthly")
        & raw[f"{PRICE} flag"].eq("A")
    ]
    return raw, project, predictions, saved["models"], notebook["cells"]


def format_number(value, digits=0):
    return f"{value:,.{digits}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def cards(values):
    for column, (label, value, detail) in zip(st.columns(len(values)), values):
        column.html(
            '<div class="dash-metric">'
            f'<p>{html.escape(label)}</p><strong>{html.escape(str(value))}</strong>'
            f'<p>{html.escape(detail)}</p></div>'
        )


def draw(chart, height=280):
    st.altair_chart(
        chart.properties(height=height)
        .configure_view(stroke=None)
        .configure_axis(
            labelColor=GRAY, titleColor=INK, gridColor="#eee6df", domain=False, tickColor="#eee6df"
        )
        .configure_legend(labelColor=INK, titleColor=INK),
        theme=None,
        width="stretch",
    )


def table(frame, key, height=350):
    st.dataframe(frame, hide_index=True, width="stretch", height=height)
    st.download_button(
        "Unduh CSV", frame.to_csv(index=False).encode("utf-8-sig"),
        file_name=f"{key}.csv", mime="text/csv", key=key, on_click="ignore",
    )


def year_slice(raw, year):
    return raw.loc[raw["date"].dt.year.eq(year)]


def price_chart(rows, key):
    st.subheader("Pergerakan harga bulanan")
    available = rows.dropna(subset=[PRICE])
    if available.empty:
        st.info("Harga produsen tidak tersedia untuk pilihan ini.")
        return
    countries = sorted(available["Country"].unique())
    country = st.selectbox(
        "Negara untuk grafik harga", countries,
        index=countries.index("Indonesia") if "Indonesia" in countries else 0, key=key,
    )
    series = available.loc[available["Country"].eq(country), ["date", PRICE]].sort_values("date")
    series = series.rename(columns={"date": "Bulan", PRICE: "Harga"})
    # Preserve blank months so the line cannot imply observations across gaps.
    calendar = pd.date_range(series["Bulan"].min(), series["Bulan"].max(), freq="MS")
    series = series.drop_duplicates("Bulan").set_index("Bulan").reindex(calendar)
    series = series.rename_axis("Bulan").reset_index()
    base = alt.Chart(series).encode(
        x=alt.X("Bulan:T", title=None, axis=alt.Axis(format="%b")),
        y=alt.Y("Harga:Q", title="Harga (LCU per ton)", scale=alt.Scale(zero=False)),
        tooltip=[alt.Tooltip("Bulan:T", format="%Y-%m"), alt.Tooltip("Harga:Q", format=",.2f")],
    )
    draw(base.mark_line(color=ORANGE, strokeWidth=2.6, point=True, invalid="break-paths-show-domains"))
    st.caption("LCU adalah mata uang lokal. Bulan kosong menandakan harga tidak tercatat.")


def class_donut(result):
    st.subheader("Arah harga aktual")
    if result.empty:
        st.info("Tidak ada label aktual dari notebook untuk tahun ini.")
        return
    count = result["Aktual"].map(LABELS).value_counts().rename_axis("Arah").reset_index(name="Jumlah")
    chart = alt.Chart(count).mark_arc(innerRadius=64, outerRadius=99, cornerRadius=4).encode(
        theta="Jumlah:Q",
        color=alt.Color("Arah:N", scale=alt.Scale(domain=["Naik", "Tidak naik"], range=[ORANGE, PEACH]),
                        legend=alt.Legend(orient="bottom", title=None)),
        tooltip=["Arah:N", "Jumlah:Q"],
    )
    draw(chart, 272)
    st.caption(f"{len(result)} contoh dengan label aktual.")


def macro(actual, predicted):
    return f1_score(actual, predicted, labels=[0, 1], average="macro", zero_division=0)


def readable_predictions(frame):
    display = frame.drop(columns="Tahun sasaran", errors="ignore").copy()
    for column in display.columns.difference(["Negara", "Bulan acuan", "Bulan sasaran", "Bagian"]):
        display[column] = display[column].map(LABELS)
    display["Status data"] = "Tersedia"
    return display


def overview(prices, result, year):
    if not result.empty:
        score = format_number(macro(result["Aktual"], result[MODEL]), 4)
        baseline_score = format_number(macro(result["Aktual"], result[BASELINE]), 4)
    else:
        score = baseline_score = "—"
    cards([
        ("Observasi harga", format_number(len(prices)), "Negara proyek"),
        ("Negara tercatat", format_number(prices["Country"].nunique()), f"Tahun {year}"),
        ("Macro-F1 Random Forest", score, "Model terpilih"),
        ("Macro-F1 persistensi", baseline_score, "Baseline arah harga"),
    ])
    main, side = st.columns([1.9, 1])
    with main:
        with st.container(border=True):
            price_chart(prices, "overview_country")
    with side:
        with st.container(border=True):
            class_donut(result)
    with st.container(border=True):
        st.subheader("Contoh hasil klasifikasi")
        if result.empty:
            st.info("Klasifikasi notebook tersedia untuk target 2022, 2023, dan 2024.")
        else:
            preview = result[["Negara", "Bulan acuan", "Bulan sasaran", "Aktual", MODEL]].head(8)
            st.dataframe(readable_predictions(preview), hide_index=True, width="stretch")


def dataset(raw, scoped, year):
    st.subheader("Jelajahi dataset")
    selection = st.radio(
        "Cakupan data", ["Negara proyek", "Seluruh ekspor"], horizontal=True, key="dataset_scope"
    )
    base = year_slice(scoped if selection == "Negara proyek" else raw, year)
    countries = sorted(base["Country"].dropna().unique())
    chosen = st.multiselect("Filter negara", countries, placeholder="Semua negara")
    filtered = base.loc[base["Country"].isin(chosen)] if chosen else base
    cards([
        ("Baris data", format_number(len(filtered)), f"Tahun {year}"),
        ("Negara", format_number(filtered["Country"].nunique()), selection),
        ("Harga LCU terisi", format_number(filtered[PRICE].notna().sum()), "Observasi harga produsen"),
    ])
    main, side = st.columns([1.6, 1])
    with main:
        with st.container(border=True):
            price_chart(filtered, "dataset_price_country")
    with side:
        with st.container(border=True):
            st.subheader("Cakupan observasi")
            count = (filtered.dropna(subset=[PRICE]).groupby("Country").size()
                     .nlargest(10).rename_axis("Negara").reset_index(name="Observasi"))
            if count.empty:
                st.info("Tidak ada observasi harga untuk filter ini.")
            else:
                draw(alt.Chart(count).mark_bar(color=ORANGE, cornerRadiusEnd=4).encode(
                    x=alt.X("Observasi:Q", title="Jumlah observasi harga"),
                    y=alt.Y("Negara:N", sort="-x", title=None), tooltip=["Negara:N", "Observasi:Q"],
                ), 270)
                if filtered["Country"].nunique() > 10:
                    st.caption("Sepuluh negara dengan observasi terbanyak pada filter ini.")
    st.subheader("Tabel sumber")
    st.caption("FAOSTAT Producer Prices. Panel proyek memakai harga bulanan padi berstatus A pada negara yang dipilih di notebook.")
    table(filtered.sort_values(["date", "Country"]), f"dataset_{year}")


def classification(result, models, year):
    st.subheader("Klasifikasi arah harga")
    if result.empty:
        st.info("Klasifikasi notebook tersedia untuk target 2022, 2023, dan 2024.")
        return
    st.caption("Filter tahun mengikuti bulan sasaran. Prediksi memakai informasi hingga bulan acuan.")
    left, right = st.columns(2)
    model = left.selectbox("Model atau baseline", models, index=models.index(MODEL))
    country = right.selectbox("Negara", ["Semua negara", *sorted(result["Negara"].unique())], key="class_country")
    shown = result if country == "Semua negara" else result.loc[result["Negara"].eq(country)]
    tn, fp, fn, tp = confusion_matrix(shown["Aktual"], shown[model], labels=[0, 1]).ravel()
    cards([
        ("Contoh klasifikasi", len(shown), shown["Bagian"].iloc[0]),
        ("Macro-F1", format_number(macro(shown["Aktual"], shown[model]), 4), model),
        ("FP", fp, "Diprediksi naik, aktual tidak naik"),
        ("FN", fn, "Diprediksi tidak naik, aktual naik"),
    ])
    with st.container(border=True):
        st.subheader("Kenaikan aktual dan prediksi per bulan")
        trend = shown.groupby("Bulan sasaran")[["Aktual", model]].sum().rename(
            columns={model: "Prediksi"}
        ).reset_index().melt("Bulan sasaran", var_name="Seri", value_name="Jumlah naik")
        draw(alt.Chart(trend).mark_bar(cornerRadiusEnd=4).encode(
            x=alt.X("Bulan sasaran:O", title="Bulan sasaran", axis=alt.Axis(labelAngle=0)),
            xOffset="Seri:N",
            y=alt.Y("Jumlah naik:Q", title="Jumlah contoh naik"),
            color=alt.Color("Seri:N", scale=alt.Scale(domain=["Aktual", "Prediksi"], range=[GRAY, ORANGE]),
                            legend=alt.Legend(title=None)),
            tooltip=["Bulan sasaran:O", "Seri:N", "Jumlah naik:Q"],
        ))
    st.subheader("Prediksi per negara dan bulan")
    table(readable_predictions(shown), f"klasifikasi_{year}", height=440)


def eval_metrics(result, models):
    actual = result["Aktual"]
    rows = []
    for model in models:
        predicted = result[model]
        tn, fp, fn, tp = confusion_matrix(actual, predicted, labels=[0, 1]).ravel()
        rows.append({
            "Model atau baseline": model, "Macro-F1": macro(actual, predicted),
            "Balanced accuracy": balanced_accuracy_score(actual, predicted),
            "Recall naik": recall_score(actual, predicted, zero_division=0),
            "Precision naik": precision_score(actual, predicted, zero_division=0),
            "Accuracy": accuracy_score(actual, predicted),
            "TN": tn, "FP": fp, "FN": fn, "TP": tp,
            "Jenis": "Baseline" if model.startswith("Baseline ") else "Model",
        })
    return pd.DataFrame(rows).sort_values("Macro-F1", ascending=False)


def evaluation(result, predictions, models, year):
    st.subheader("Evaluasi model")
    if result.empty:
        st.info("Metrik tersedia pada tahun klasifikasi 2022–2024.")
        return
    split = result["Bagian"].iloc[0]
    st.caption(f"{split} {year} · {len(result)} contoh dari {result['Negara'].nunique()} negara")
    if split == "Latih":
        st.caption("Skor latih menggambarkan kinerja pada data yang dipakai untuk melatih model.")
    metrics = eval_metrics(result, models)
    left, right = st.columns([1.45, 1])
    with left:
        with st.container(border=True):
            st.subheader("Macro-F1 per model")
            graphic = alt.Chart(metrics).mark_bar(cornerRadiusEnd=4).encode(
                y=alt.Y("Model atau baseline:N", sort="-x", title=None),
                x=alt.X("Macro-F1:Q", scale=alt.Scale(domain=[0, 1])),
                color=alt.Color("Jenis:N", scale=alt.Scale(domain=["Model", "Baseline"], range=[ORANGE, GRAY]),
                                legend=None),
                tooltip=["Model atau baseline:N", alt.Tooltip("Macro-F1:Q", format=".4f")],
            )
            draw(graphic, 260)
    with right:
        with st.container(border=True):
            st.subheader("Confusion matrix")
            model = st.selectbox("Tampilkan untuk", models, index=models.index(MODEL), key="matrix_model")
            cm = confusion_matrix(result["Aktual"], result[model], labels=[0, 1])
            matrix = pd.DataFrame([
                {"Aktual": LABELS[i], "Prediksi": LABELS[j], "Jumlah": int(cm[i, j]), "Sel": tag}
                for i, names in enumerate((("TN", "FP"), ("FN", "TP")))
                for j, tag in enumerate(names)
            ])
            base = alt.Chart(matrix).encode(
                x=alt.X("Prediksi:N", sort=list(LABELS.values()), axis=alt.Axis(labelAngle=0)),
                y=alt.Y("Aktual:N", sort=list(LABELS.values())),
                tooltip=["Sel:N", "Aktual:N", "Prediksi:N", "Jumlah:Q"],
            )
            blocks = base.mark_rect(cornerRadius=6).encode(
                color=alt.Color("Jumlah:Q", scale=alt.Scale(range=["#fff3e9", "#f1975b"]), legend=None)
            )
            draw(blocks + base.mark_text(color=INK, size=16, fontWeight="bold").encode(text="Jumlah:Q"), 207)
    st.subheader("Metrik klasifikasi")
    st.dataframe(metrics.drop(columns="Jenis").round(4), hide_index=True, width="stretch")
    countries = []
    for name, group in result.groupby("Negara"):
        for method in [MODEL, BASELINE]:
            countries.append({
                "Negara": name, "Metode": method, "Contoh": len(group),
                "Macro-F1": macro(group["Aktual"], group[method]),
            })
    with st.container(border=True):
        st.subheader("Hasil per negara")
        draw(alt.Chart(pd.DataFrame(countries)).mark_point(filled=True, size=75).encode(
            y=alt.Y("Negara:N", title=None),
            x=alt.X("Macro-F1:Q", scale=alt.Scale(domain=[0, 1])),
            color=alt.Color("Metode:N", scale=alt.Scale(domain=[MODEL, BASELINE], range=[ORANGE, GRAY]),
                            legend=alt.Legend(orient="bottom", title=None)),
            shape=alt.Shape("Metode:N", legend=None),
            tooltip=["Negara:N", "Metode:N", "Contoh:Q", alt.Tooltip("Macro-F1:Q", format=".4f")],
        ), max(230, result["Negara"].nunique() * 24))
        st.caption("Baca skor negara bersama jumlah contoh dan cakupan kelas.")
    with st.expander("Perbandingan data latih dan uji", expanded=True):
        scores = []
        for part in ("Latih", "Uji"):
            data = predictions.loc[predictions["Bagian"].eq(part)]
            for trained in models[:3]:
                scores.append({"Model": trained, "Bagian": part, "Macro-F1": macro(data["Aktual"], data[trained])})
        draw(alt.Chart(pd.DataFrame(scores)).mark_bar(cornerRadiusEnd=4).encode(
            x=alt.X("Model:N", axis=alt.Axis(labelAngle=0), title=None),
            xOffset="Bagian:N", y=alt.Y("Macro-F1:Q", scale=alt.Scale(domain=[0, 1])),
            color=alt.Color("Bagian:N", scale=alt.Scale(domain=["Latih", "Uji"], range=[GRAY, ORANGE]),
                            legend=alt.Legend(title=None)),
            tooltip=["Model:N", "Bagian:N", alt.Tooltip("Macro-F1:Q", format=".4f")],
        ), 240)


def group_sections(cells):
    sections = {}
    current = "Ikhtisar"
    for cell in cells:
        source = "".join(cell.get("source", []))
        if cell["cell_type"] == "markdown":
            heading = re.match(r"^# ([^\n]+)", source)
            if heading and not heading.group(1).startswith("Klasifikasi Kenaikan Harga"):
                current = heading.group(1).strip()
        sections.setdefault(current, []).append(cell)
    return sections


def notebook_section(cells, current):
    for cell in cells:
        source = "".join(cell.get("source", []))
        if cell["cell_type"] == "markdown":
            source = re.sub(rf"^# {re.escape(current)}\s*\n", "", source, count=1)
            if source.strip():
                st.markdown(source)
            continue
        for output in cell.get("outputs", []):
            mime = output.get("data", {})
            if "image/png" in mime:
                image = "".join(mime["image/png"]).replace("\n", "")
                st.image(base64.b64decode(image), width="stretch")
            elif "text/html" in mime:
                st.html('<div class="notebook-table">' + "".join(mime["text/html"]) + "</div>")
            elif output.get("output_type") == "stream" and output.get("name") == "stdout":
                st.code("".join(output.get("text", [])), language=None)
            elif "text/plain" in mime:
                st.code("".join(mime["text/plain"]), language=None)


def main():
    st.set_page_config(page_title="Dashboard", layout="wide", initial_sidebar_state="expanded")
    st.html(CSS)
    try:
        paths = (RAW_PATH, NOTEBOOK_PATH, RESULTS_PATH)
        raw, project, predictions, models, cells = load_data(tuple(path.stat().st_mtime_ns for path in paths))
    except (OSError, ValueError) as exc:
        st.error(f"Data dashboard tidak dapat dibaca. {exc}")
        st.stop()

    years = sorted(predictions["Tahun sasaran"].unique(), reverse=True)
    with st.sidebar:
        st.subheader("Navigasi")
        page = st.radio(
            "Halaman", ["Ringkasan", "Dataset", "Klasifikasi", "Evaluasi", "Notebook"],
            label_visibility="collapsed", key="page",
        )
        if page == "Dataset":
            dataset_years = sorted(raw.loc[raw["date"].dt.year.le(max(years)), "date"].dt.year.unique(), reverse=True)
            year = st.selectbox("Tahun observasi", dataset_years, key="dataset_year")
        elif page == "Notebook":
            year = None
        else:
            year = st.selectbox("Tahun sasaran", years, key="result_year")
        st.divider()
        st.caption("Sumber data FAOSTAT Producer Prices")

    result = predictions.loc[predictions["Tahun sasaran"].eq(year)]
    subtitle = "Harga produsen padi di negara-negara Asia"
    period = f'{year} · {result["Bagian"].iloc[0]}' if year and not result.empty and page != "Dataset" else (
        str(year) if year else "Projek.ipynb"
    )
    st.html(
        '<header class="dash-hero"><div><h1>Dashboard</h1>'
        f'<p>{subtitle}</p></div><span class="dash-period">{html.escape(period)}</span></header>'
    )
    if page == "Ringkasan":
        overview(year_slice(project, year), result, year)
    elif page == "Dataset":
        dataset(raw, project, year)
    elif page == "Klasifikasi":
        classification(result, models, year)
    elif page == "Evaluasi":
        evaluation(result, predictions, models, year)
        if year == max(years):
            sections = group_sections(cells)
            with st.expander("Analisis FP dan FN dari notebook"):
                notebook_section(sections["Analisis Kesalahan"], "Analisis Kesalahan")
    else:
        sections = group_sections(cells)
        selected = st.selectbox("Bagian notebook", list(sections), index=list(sections).index("Business Understanding"))
        st.subheader(selected)
        notebook_section(sections[selected], selected)


if __name__ == "__main__":
    main()
