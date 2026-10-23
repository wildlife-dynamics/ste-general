"""
Generate the STE General Workflow Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: ste_general_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from datetime import date

OUTPUT_FILE = "ste_general_technical_guide.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
GREEN_LIGHT = colors.HexColor("#d8f3dc")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)

H1       = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                  spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                  spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                  spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")

BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=6, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=3, leftIndent=14, firstLineIndent=-10,
                  bulletIndent=4)
CODE     = _style("InlineCode", fontSize=8, leading=12, fontName="Courier",
                  backColor=LIGHT_GREY, textColor=colors.HexColor("#c0392b"),
                  spaceAfter=4, leftIndent=10, rightIndent=10, borderPad=3)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():           return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)
def p(text, style=BODY): return Paragraph(text, style)
def h1(text):       return Paragraph(text, H1)
def h2(text):       return Paragraph(text, H2)
def h3(text):       return Paragraph(text, H3)
def sp(n=6):        return Spacer(1, n)
def bullet(text):   return Paragraph(f"• {text}", BULLET)
def note(text):     return Paragraph(f"<b>Note:</b> {text}", NOTE)
def code(text):     return Paragraph(text, CODE)

def c(text):
    """Wrap text in a Paragraph for use inside Table cells."""
    return Paragraph(str(text), BODY)

def make_table(data, col_widths, header_row=True):
    wrapped = [[c(cell) if isinstance(cell, str) else cell for cell in row]
               for row in data]
    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header_row else 0)
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",    (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",     (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS",(0, 1),(-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",         (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
    ]))
    return t


# ── Page template ──────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(GREEN_DARK)
    canvas.rect(0, 0, w, 22, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(1.5*cm, 7, "STE General Workflow — Technical Guide")
    canvas.drawRightString(w - 1.5*cm, 7, f"Page {doc.page}")
    canvas.setFillColor(AMBER)
    canvas.rect(0, h - 4, w, 4, fill=1, stroke=0)
    canvas.restoreState()


# ── Build story ────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2*cm,
        title="STE General Workflow — Technical Guide",
        author="Ecoscope",
    )

    story = []

    # ── Cover ──────────────────────────────────────────────────────────────────
    story += [
        sp(60),
        p("STE General Workflow", TITLE),
        p("Technical Guide", SUBTITLE),
        sp(8),
        hr(),
        p("Elephant Movement Ecology — Methodology &amp; Calculation Reference", META),
        p(f"Version 1.3  ·  Generated {date.today().strftime('%B %d, %Y')}", META),
        hr(),
        PageBreak(),
    ]

    # ── 1. Overview ───────────────────────────────────────────────────────────
    story += [
        h1("1. Overview"),
        hr(),
        p(
            "The <b>STE General Workflow</b> is a comprehensive data-to-report pipeline "
            "purpose-built for analysing African elephant (<i>Loxodonta africana</i>) "
            "movement ecology. It ingests GPS telemetry from <b>EarthRanger</b>, derives "
            "seasonal boundaries from <b>Google Earth Engine</b> NDVI time-series, "
            "performs a rich sequence of spatial computations, and delivers <b>14 interactive "
            "map products</b>, a protection status chart, seasonal CSV data, an interactive "
            "dashboard, and a print-ready Word report — all at the subject-group level."
        ),
        p(
            "The workflow is implemented as an <b>Ecoscope Workflow</b> (YAML spec) "
            "and executes within the <code>ecoscope-workflows</code> runtime. Tasks "
            "are chained via data references (<code>${{ workflow.&lt;id&gt;.return }}</code>); "
            "the engine resolves execution order automatically. Fan-out iteration "
            "over individual subjects uses the <code>mapvalues</code> directive."
        ),
        sp(4),
        note(
            "The trajectory segment filter defaults (max speed 9 knots, max gap 6 h) "
            "are tuned for elephant movement. All thresholds are user-configurable "
            "at run time through the workflow configuration form."
        ),
        sp(4),
        p("The workflow produces the following outputs per run:"),
        make_table(
            [
                ["Category", "Outputs"],
                ["Movement maps",      "Movement Tracks (current + previous), Subject Tracks"],
                ["Home range maps",    "Overall ETD, Filtered 99th percentile, Protected areas ETD, Unprotected areas ETD, Seasonal HR per subject"],
                ["Habitat use maps",   "Recursion Events raster, Dry season speed raster, Wet season speed raster"],
                ["Activity maps",      "Time of Day Dominance grid, Night Fixes grid"],
                ["Event maps",         "Elephant Sightings / Collaring Events"],
                ["Charts",             "Protection Status bar chart"],
                ["Data files",         "Relocations, trajectories, ETD polygons, seasonal windows CSV (GeoParquet + CSV)"],
                ["Report",             "Word document: cover page + general section; Interactive dashboard"],
            ],
            [4.5*cm, 12*cm],
        ),
    ]

    # ── 2. Dependencies ───────────────────────────────────────────────────────
    story += [
        sp(4), h1("2. Dependencies &amp; Prerequisites"), hr(),

        h2("2.1 EarthRanger Connection"),
        p(
            "All telemetry is sourced from an <b>EarthRanger</b> instance "
            "(<code>set_er_connection</code>). The workflow calls "
            "<code>get_subjectgroup_observations</code> twice — once for the current "
            "analysis period and once for the comparison (previous) period. Both calls "
            "use <code>filter: clean</code>, discarding any observation already flagged "
            "as junk before the data reaches the workflow. "
            "<code>include_details</code> and <code>include_subjectsource_details</code> "
            "are both set to <code>false</code> to minimise payload size."
        ),
        bullet("The connection handle is passed as <code>client</code> to every EarthRanger fetch task."),
        bullet("EarthRanger events are fetched separately via <code>get_events</code> using the same client."),

        sp(4), h2("2.2 Google Earth Engine Connection"),
        p(
            "A <b>Google Earth Engine (GEE)</b> service account is required for "
            "seasonal analysis. The task <code>custom_determine_season_windows</code> "
            "queries the GEE NDVI time-series for the region of interest (derived from "
            "the ETD raster extent) to classify the analysis period into wet and dry "
            "seasons. The GEE project is supplied by the user via <code>set_gee_connection</code>."
        ),

        sp(4), h2("2.3 Subject Group"),
        p(
            "The user picks a <b>Subject Group Name</b> (default: <code>Elephants</code>) "
            "from a drop-down of the subject groups on the chosen EarthRanger data source, "
            "filled by the <code>EarthRangerEnumResolver</code> form transformer once a data "
            "source is selected. All subjects within that group are fetched for the "
            "configured time range. The grouper is fixed to <code>subject_name</code>, "
            "so outputs are produced at the group level (not per individual)."
        ),
        note(
            "Unlike the STE Mapbook workflow, the General workflow does not split outputs "
            "per subject for most maps — it generates one map per map type across the "
            "entire group. Only seasonal home range maps are fanned out per subject."
        ),
        p(
            "Both observation fetches set <code>include_subject_additional: false</code>, "
            "so each subject's free-form <code>additional</code> JSON field is not "
            "retained. This is fixed in the spec and no longer exposed on the form."
        ),

        sp(4), h2("2.4 Map Overlay &amp; landDx Geodatabase"),
        p(
            "The <b>Map Overlay</b> step (<code>select_map_overlay</code>) selects the "
            "protected-area layer shared by every map, and doubles as the basis for the "
            "protected/unprotected split (Section 4.6) and the Protection Status bar "
            "chart (Section 5). Only protected-area-style layers are supported. Three "
            "sources are available:"
        ),
        bullet("<b>LandDx (default)</b> — the standard protected-area GeoPackage, downloaded and styled automatically; no input required."),
        bullet("<b>EarthRanger Spatial Feature</b> — fetches one or more named feature sets from the connected EarthRanger instance."),
        bullet("<b>Custom Local File</b> — one or more local GeoJSON / GeoPackage / GeoParquet files, each becoming its own styled layer."),
        p(
            "When <b>LandDx</b> is selected, the geodatabase (<code>landDx.gpkg</code>, "
            "layer <code>landDx_polygons</code>) is downloaded from a Dropbox URL by "
            "default (a local path may be supplied instead), then filtered to three "
            "land-use types with only three columns retained "
            "(<code>type</code>, <code>name</code>, <code>geometry</code>)."
        ),
        make_table(
            [
                ["Land-use Type",          "Fill / Line Colour",               "Opacity"],
                ["Community Conservancy",  "RGB(166, 182, 151)  —  #a6b697",  "17.5 %"],
                ["National Reserve",       "RGB(136, 167, 142)  —  #88a78e",  "17.5 %"],
                ["National Park",          "RGB(17,  86,  49)   —  #115631",  "17.5 %"],
            ],
            [5*cm, 7.5*cm, 4*cm],
        ),
        p(
            "A text-label layer (centroid-anchored, Arial, 1 000 m base size, "
            "40–75 px screen clamp) renders protected-area names. "
            "The database is also split by <code>type</code> and the geometry type "
            "is annotated before DeckGL layer creation."
        ),

        sp(4), h2("2.5 Base Map Tile Layers"),
        p(
            "Every map uses two stacked tile services, configured through the "
            "<b>Configure basemap layers</b> step (the platform's <code>set_base_maps</code> "
            "task). The layers are set in the task's <code>partial</code>, so they don't "
            "appear on the form; change them in <code>spec.yaml</code> and recompile:"
        ),
        make_table(
            [
                ["Layer", "URL (abbreviated)", "Opacity", "Max zoom"],
                ["ESRI World Hillshade",
                 "arcgisonline.com/…/World_Hillshade/…/{z}/{y}/{x}",
                 "0.995", "20"],
                ["ESRI World Boundaries &amp; Places",
                 "arcgisonline.com/…/World_Boundaries_and_Places_Alternate/…/{z}/{y}/{x}",
                 "0.35", "20"],
            ],
            [4.5*cm, 7*cm, 2*cm, 2.5*cm],
        ),
    ]

    # ── 3. Data Ingestion Pipeline ────────────────────────────────────────────
    story += [
        sp(4), h1("3. Data Ingestion Pipeline"), hr(),

        h2("3.1 Observations → Relocations"),
        p(
            "<code>process_relocations</code> converts raw EarthRanger observations "
            "into a standardised relocations GeoDataFrame. The following columns are "
            "extracted and retained:"
        ),
        make_table(
            [
                ["Column",                          "Source field",              "Description"],
                ["groupby_col",                     "internal",                  "Subject identifier for grouping"],
                ["fixtime",                         "observation timestamp",     "UTC datetime of the GPS fix"],
                ["junk_status",                     "EarthRanger flag",          "True if fix is marked junk"],
                ["geometry",                        "lat/lon",                   "Point geometry (WGS 84)"],
                ["extra__subject__name",            "subject.name",              "Elephant display name"],
                ["extra__subject__hex",             "subject.hex_color",         "Subject colour used for per-subject maps"],
                ["extra__subject__sex",             "subject.sex",               "Subject sex (M / F / unknown)"],
                ["extra__created_at",               "observation.created_at",    "Record creation timestamp"],
                ["extra__subject__subject_subtype", "subject.subject_subtype",   "Subject subtype (e.g. elephant)"],
            ],
            [4*cm, 4*cm, 8.5*cm],
        ),
        p("Three known-bad coordinate pairs are filtered out unconditionally:"),
        bullet("(180.0, 90.0) — boundary sentinel"),
        bullet("(0.0, 0.0) — null-island artefact"),
        bullet("(1.0, 1.0) — common default / test value"),

        sp(4), h2("3.2 Day / Night Annotation"),
        p(
            "Each relocation is labelled as day or night by "
            "<code>classify_is_night</code>. Solar elevation is calculated at the "
            "fix's location and UTC timestamp. A fix is classified as night "
            "(<code>is_night = True</code>) when the sun is below the horizon. "
            "This boolean is later used as the colour key for the Time of Day "
            "Dominance and Night Fixes maps."
        ),

        sp(4), h2("3.3 Trajectory Segment Filter"),
        p(
            "<code>custom_trajectory_segment_filter</code> builds a reusable filter "
            "object that is applied to <i>both</i> the current and previous period "
            "trajectories, ensuring methodological consistency across periods."
        ),
        make_table(
            [
                ["Parameter",         "Default",  "Unit",  "Purpose"],
                ["min_length_meters", "0.001",    "m",     "Remove sub-centimetre GPS noise"],
                ["max_length_meters", "5 000",    "m",     "Remove implausible long jumps"],
                ["min_time_secs",     "1",        "s",     "Remove zero-duration segments"],
                ["max_time_secs",     "21 600",   "s",     "Remove gaps > 6 h (fix dropout)"],
                ["min_speed_kmhr",    "0.01",     "km/h",  "Remove near-stationary fixes"],
                ["max_speed_kmhr",    "9",        "km/h",  "Remove biologically impossible speeds for elephants"],
            ],
            [4*cm, 2.2*cm, 1.8*cm, 8.5*cm],
        ),

        sp(4), h2("3.4 Relocations → Trajectories"),
        p(
            "<code>relocations_to_trajectory</code> connects consecutive fixes for "
            "the same subject into linear trajectory segments. Each segment records:"
        ),
        bullet("<b>dist_meters</b> — straight-line distance between the two fixes"),
        bullet("<b>speed_kmhr</b> — dist_meters ÷ elapsed time × 3.6"),
        bullet("<b>segment_start / segment_end</b> — timestamps of the bounding fixes"),
        bullet("<b>geometry</b> — LineString in WGS 84"),
        p(
            "A temporal index is then added (<code>add_temporal_index</code>) keyed "
            "on <code>segment_start</code> and grouped by subject name. "
            "Column names are normalised via <code>map_columns</code> (e.g. "
            "<code>extra__name → subject_name</code>, <code>extra__hex → hex_color</code>)."
        ),

        sp(4), h2("3.5 NDVI Seasonal Window Detection"),
        p(
            "<code>custom_determine_season_windows</code> queries the Google Earth "
            "Engine NDVI time-series for the region of interest (the ETD raster extent). "
            "Wet and dry season windows are identified from the NDVI phenology curve: "
            "periods where NDVI exceeds a threshold are classified as <i>wet</i>; "
            "periods below are classified as <i>dry</i>. The function returns a "
            "DataFrame of dated season intervals, which is persisted as "
            "<code>seasonal_windows.csv</code> for auditability."
        ),
        note(
            "Season boundaries are data-driven — they reflect the actual green-up and "
            "senescence pattern for the specific landscape and year, rather than fixed "
            "calendar dates. This is critical in East African ecosystems where rainfall "
            "timing varies considerably year to year."
        ),
        note(
            "A short analysis period can cause <code>custom_determine_season_windows</code> "
            "to fail with <code>EEException('User memory limit exceeded.')</code> — "
            "there isn't enough NDVI history for Earth Engine to resolve season windows "
            "in one synchronous computation. Widen the workflow's Since/Until range to "
            "at least two to three months and re-run."
        ),

        sp(4), h2("3.6 Season Labelling"),
        p(
            "<code>create_seasonal_labels</code> joins the season windows onto the "
            "trajectory GeoDataFrame by timestamp, appending a <code>season</code> "
            "column (<code>'wet'</code> or <code>'dry'</code>) to each segment. "
            "All subsequent raster and home range analyses that are season-specific "
            "operate on this labelled GeoDataFrame."
        ),

        sp(4), h2("3.7 Previous Period"),
        p(
            "The previous period is determined by <code>flexible_previous_period</code> "
            "(Section 8.3). "
            "The same trajectory segment filter is applied to the previous period "
            "trajectories. A <code>duration_status</code> column is appended — "
            "<code>'Previous tracks'</code> — before merging with current period "
            "trajectories for the Movement Tracks Map."
        ),

        sp(4), h2("3.8 Speed Classification"),
        p(
            "<code>apply_classification</code> bins the <code>speed_kmhr</code> "
            "column using <b>Equal Interval</b> with <b>k = 6</b>. Labels are "
            "formatted to one decimal place with the suffix <code>km/h</code>. "
            "The resulting <code>speed_bins</code> column is used on the speed-coloured "
            "layers in the Subject Tracks context."
        ),
    ]

    # ── 4. Map Outputs ────────────────────────────────────────────────────────
    story += [
        sp(4), h1("4. Map Outputs — Methodology"), hr(),
    ]

    # 4.1 Movement Tracks
    story += [
        h2("4.1 Movement Tracks Map"),
        p(
            "Overlays current and previous period trajectories for the entire subject "
            "group, allowing rangers to identify range shifts across time."
        ),
        h3("Dual-period construction"),
        p(
            "After independent trajectory builds for both periods, a "
            "<code>duration_status</code> column is appended to each "
            "(<code>'Current tracks'</code> or <code>'Previous tracks'</code>). "
            "The two GeoDataFrames are merged with <code>merge_multiple_df</code> "
            "and colours are assigned by <code>assign_duration_colors</code> / "
            "<code>modify_status_colors</code>. Trajectories are sorted descending "
            "by <code>duration_status</code> so current tracks always render on top."
        ),
        h3("Retained columns"),
        p(
            "Before layer creation, <code>filter_movement_cols</code> retains only: "
            "<code>duration_status</code>, <code>duration_status_colors</code>, "
            "<code>is_night</code>, <code>geometry</code>."
        ),
        h3("Line styling"),
        make_table(
            [
                ["Property",       "Value"],
                ["Width",          "2.85 px (min 2, max 8, screen-space)"],
                ["Opacity",        "55 %"],
                ["Cap / Join",     "Rounded"],
                ["Legend sort",    "Ascending by duration_status"],
            ],
            [5*cm, 11.5*cm],
        ),
    ]

    # 4.2 Subject Tracks
    story += [
        sp(4), h2("4.2 Subject Tracks Map"),
        p(
            "Trajectories coloured by individual subject using each animal's own "
            "EarthRanger hex colour, providing a per-animal view of space use "
            "without the time-comparison overlay of the Movement Tracks Map."
        ),
        p(
            "<code>convert_hex_to_rgba</code> converts the <code>hex_color</code> "
            "string field to an RGBA list (<code>rgba_colors</code>) compatible with "
            "DeckGL's <code>get_color</code> property. "
            "The legend labels subjects by <code>subject_name</code>."
        ),
    ]

    # 4.3 Collaring Events
    story += [
        sp(4), h2("4.3 Elephant Sightings / Collaring Events Map"),
        p(
            "<code>get_events</code> fetches EarthRanger events for the analysis "
            "period. Events include collaring records and elephant sightings logged "
            "in the field. The optional <b>Event Types</b> filter is a drop-down of the "
            "event types on the chosen data source (<code>EarthRangerEnumResolver</code>). "
            "Only events with a point geometry are included "
            "(<code>include_null_geometry: false</code>)."
        ),
        p("Columns retained per event:"),
        bullet("id, time, event_type, event_category, reported_by, serial_number, geometry, created_at, event_details"),
        h3("Scatter layer styling"),
        make_table(
            [
                ["Property",         "Value"],
                ["Fill colour",      "RGB(85, 107, 47)  —  #556b2f  (dark olive green)"],
                ["Line colour",      "RGBA(0, 0, 0, 200)  (near-black outline)"],
                ["Line width",       "0.55"],
                ["Radius",           "3.55"],
                ["Opacity",          "75 %"],
            ],
            [5*cm, 11.5*cm],
        ),
    ]

    # 4.4 Overall Home Range
    story += [
        sp(4), h2("4.4 Overall Home Range Map (ETD)"),
        p(
            "The primary space-use estimator. Elliptical Time Density (ETD) weights "
            "space use by the time spent in each area, producing ecologically realistic "
            "home range contours."
        ),
        h3("ETD parameters — calculate_elliptical_time_density"),
        make_table(
            [
                ["Parameter",           "Value",          "Meaning"],
                ["CRS",                 "ESRI:53042",      "World Azimuthal Equidistant — equal-area, minimises distortion across Africa"],
                ["cell_size",           "Auto-scale",      "Derived automatically from data extent and trajectory density"],
                ["max_speed_factor",    "1.05",            "Segments with speed > 1.05 × median are down-weighted"],
                ["expansion_factor",    "1.3",             "Raster extent expanded 30 % beyond data envelope"],
                ["band_count",          "1",               "Single density band output"],
                ["nodata_value",        "NaN",             "Cells outside probability mass are transparent"],
                ["percentiles",         "50, 60, 70, 80, 90, 95, 99.9", "Contour polygons at these probability thresholds"],
            ],
            [4*cm, 3*cm, 9.5*cm],
        ),
        p(
            "After computation the raster is reprojected to <b>EPSG:4326</b>. "
            "Contour polygons are coloured using the <b>RdYlGn</b> diverging colormap "
            "— inner core (50th percentile) in red, outer extent (99.9th) in green."
        ),
    ]

    # 4.5 Filtered HR
    story += [
        sp(4), h2("4.5 Filtered 99th Percentile Home Range Map"),
        p(
            "A simplified view retaining only the 99th percentile contour from the "
            "overall ETD, displayed in a single chocolate tone for clean cartographic "
            "presentation."
        ),
        p(
            "<code>filter_df_values</code> selects rows where <code>percentile ≥ 99.0</code>. "
            "The layer uses a fixed fill colour of <b>RGB(210, 105, 30) — #d2691e</b> "
            "(chocolate) at 55 % opacity, with a static legend entry labelled "
            "<i>99th percentile</i>."
        ),
    ]

    # 4.6 Protected / Unprotected Home Range
    story += [
        sp(4), h2("4.6 Protected and Unprotected Areas Home Range Maps"),
        p(
            "Two additional ETD maps show how much time elephants spend inside "
            "versus outside protected land, supporting ranger management decisions."
        ),
        h3("Protection status determination"),
        p(
            "<code>generate_protected_column</code> performs a spatial join between "
            "the trajectory GeoDataFrame and the filtered landDx polygons "
            "(<code>column: type</code>). Each trajectory segment is labelled "
            "<code>protection_status = 'Protected'</code> if its centroid falls "
            "within a Community Conservancy, National Reserve, or National Park "
            "polygon; otherwise <code>'Unprotected'</code>."
        ),
        p(
            "Two separate ETD calculations are then run — one on the protected subset "
            "and one on the unprotected subset — using identical parameters to the "
            "overall ETD (percentiles 50–99.9 %, RdYlGn colormap). The resulting "
            "GeoDataFrames are persisted as:"
        ),
        bullet("<code>protected_areas_home_range_etd.geoparquet</code>"),
        bullet("<code>unprotected_areas_home_range_etd.geoparquet</code>"),
    ]

    # 4.7 Seasonal HR
    story += [
        sp(4), h2("4.7 Seasonal Home Range Maps (per subject)"),
        p(
            "The only outputs fanned out <i>per subject</i> via <code>mapvalues</code>. "
            "Shows how each individual's space use shifts between wet and dry seasons."
        ),
        h3("Fan-out pipeline"),
        p(
            "<code>split_groups</code> partitions the season-labelled trajectory "
            "GeoDataFrame by the <code>subject_name</code> grouper, producing one "
            "GeoDataFrame per subject. <code>calculate_seasonal_home_range</code> "
            "then groups each subject's trajectories by <code>season</code> and "
            "computes an ETD for each season, extracting only the "
            "<b>99.9th percentile</b> contour. Cell size is auto-scaled independently "
            "for each subject–season combination."
        ),
        h3("Colour assignment"),
        p(
            "<code>assign_season_colors</code> maps season labels to a fixed palette "
            "(wet = blue family, dry = orange/brown family). The <code>season</code> "
            "column is first converted to string to ensure consistent matching. "
            "Polygons are rendered as filled, semi-transparent GeoJSON layers "
            "(55 % opacity, 0.35 px line width) so both seasons are visible when overlapping."
        ),
        p(
            "View state and map layers are zipped per subject via "
            "<code>zip_groupbykey</code> before being passed to <code>draw_map</code>. "
            "Output filenames are suffixed with the unique subject name retrieved by "
            "<code>dataframe_column_first_unique_str</code>."
        ),
    ]

    # 4.8 Recursion Raster
    story += [
        sp(4), h2("4.8 Recursion Events Raster"),
        p(
            "The recursion raster identifies landscape cells that elephants return to "
            "repeatedly — key resource hotspots such as waterholes, mineral licks, "
            "and seasonal foraging areas."
        ),
        h3("Ecograph raster parameters"),
        make_table(
            [
                ["Parameter",          "Value",     "Effect"],
                ["step_length",        "User-set via Raster maps → Step Length / Grid Size (default 2 000 m)", "Trajectories are resampled to this step length before aggregation"],
                ["movement_covariate", "null",       "No speed metric — the count of revisits (network weight) is aggregated"],
                ["interpolation",      "mean",       "Cell values averaged across contributing steps"],
                ["network_metric",     "weight",     "Ecograph network edge weight — proportional to revisit frequency"],
                ["radius",             "2",          "Each cell incorporates contributions from its 2-ring neighbourhood"],
                ["dist_col",           "dist_meters","Source column for step-length weighting"],
                ["tortuosity_length",  "3",          "Path sinuosity computed over 3-step windows"],
                ["filename",           "weighted_raster", "Output raster filename prefix"],
            ],
            [3.8*cm, 5*cm, 7.8*cm],
        ),
        note(
            "The <b>Step Length / Grid Size</b> field in the <b>Raster maps</b> step of "
            "the workflow form sets a single grid size shared by this Recursion Events "
            "raster <i>and</i> both the Dry and Wet Season Mean Speed rasters (Sections "
            "4.9–4.10) — it is not fixed per raster."
        ),
        h3("Classification and colouring"),
        p(
            "Raw per-cell values are classified using <b>Natural Breaks (Jenks)</b> "
            "with <b>k = 6</b>. Natural breaks minimises within-class variance — "
            "well-suited to the right-skewed distribution of revisit counts. "
            "The six-colour green-to-red ramp is applied:"
        ),
        make_table(
            [
                ["Bin", "Hex",     "Perception"],
                ["1 (lowest)",  "#1a9850", "Dark green — rarely visited"],
                ["2",           "#91cf60", "Light green"],
                ["3",           "#d9ef8b", "Yellow-green"],
                ["4",           "#fee08b", "Yellow"],
                ["5",           "#fc8d59", "Orange"],
                ["6 (highest)", "#d73027", "Red — high-frequency recursion area"],
            ],
            [3*cm, 3*cm, 10.5*cm],
        ),
    ]

    # 4.9 / 4.10 Speed Rasters
    story += [
        sp(4), h2("4.9 Dry Season Mean Speed Raster"),
        p(
            "Reveals landscape-scale movement intensity during the dry season — "
            "typically characterised by longer, faster directional travel to water."
        ),
        h3("Season filtering"),
        p(
            "<code>filter_df</code> selects rows where <code>season == 'dry'</code> "
            "from the season-labelled trajectory GeoDataFrame."
        ),
        h3("Ecograph raster parameters"),
        make_table(
            [
                ["Parameter",          "Value",   "Effect"],
                ["step_length",        "Shared with Recursion Events raster (default 2 000 m, user-set)", "Trajectories resampled to this step length before aggregation"],
                ["movement_covariate", "speed",   "Metric being aggregated is speed (km/h)"],
                ["interpolation",      "mean",    "Per-cell values are mean speed across contributing steps"],
                ["radius",             "2",       "Neighbourhood smoothing over 2-ring radius"],
                ["network_metric",     "null",    "No network metric — pure speed raster"],
            ],
            [4*cm, 5.5*cm, 7*cm],
        ),
        h3("Post-processing"),
        p(
            "After feature extraction, the GeoDataFrame is reprojected to "
            "<b>EPSG:4326</b> and sorted ascending by value. "
            "Natural Breaks classification (<b>k = 6</b>) produces <code>value_bins</code>. "
            "<code>map_values_with_unit</code> formats bin labels to one decimal "
            "place in km/h. The same six-colour green-to-red ramp used for the "
            "recursion raster is applied."
        ),

        sp(4), h2("4.10 Wet Season Mean Speed Raster"),
        p(
            "Identical pipeline to the dry season speed raster (Section 4.9) but "
            "filtering for <code>season == 'wet'</code>. Wet season movement typically "
            "shows slower, more exploratory patterns as resource availability is higher."
        ),
    ]

    # 4.11 Day/Night Dominance
    story += [
        sp(4), h2("4.11 Time of Day Dominance Map"),
        p(
            "A grid-based map showing whether each landscape cell is used "
            "predominantly during the day or at night — revealing temporal "
            "habitat partitioning."
        ),
        h3("Meshgrid construction"),
        p(
            "<code>create_meshgrid</code> generates a regular spatial grid over the "
            "extent of the annotated relocations (CRS ESRI:53042, auto-scaled cell "
            "size, <code>intersecting_only: false</code>). The same meshgrid is "
            "reused for the Night Fixes map (Section 4.12)."
        ),
        h3("Dominance calculation"),
        p(
            "<code>get_day_night_dominance</code> assigns each grid cell a boolean "
            "<code>is_night_majority</code> — <code>True</code> if more than half "
            "of fixes within the cell have <code>is_night = True</code>."
        ),
        h3("Colour assignment"),
        make_table(
            [
                ["is_night_majority", "Colour",          "Hex"],
                ["False (day)",       "Cornflower blue", "#6495ed"],
                ["True  (night)",     "Dark navy blue",  "#00008b"],
            ],
            [4.5*cm, 4.5*cm, 7.5*cm],
        ),
        p(
            "Cells are sorted descending by <code>is_night_majority</code> so night "
            "cells (True) render last and appear on top where they overlap with day cells."
        ),
    ]

    # 4.12 Night Fixes
    story += [
        sp(4), h2("4.12 Night Fixes Map"),
        p(
            "Highlights cells where a large majority of GPS fixes are nocturnal — "
            "identifying areas of consistent night-time habitat use."
        ),
        p(
            "<code>get_grid_night_fixes</code> operates on the same meshgrid and "
            "annotated relocations as Section 4.11. A cell is labelled "
            "<code>night_activity = True</code> when the proportion of nocturnal "
            "fixes meets or exceeds the <b>threshold of 0.65</b> (65 %)."
        ),
        make_table(
            [
                ["night_activity", "Colour",          "Hex"],
                ["False",          "Cornflower blue", "#6495ed"],
                ["True  (≥ 65 %)", "Dark navy blue",  "#00008b"],
            ],
            [4.5*cm, 4.5*cm, 7.5*cm],
        ),
    ]

    # 4.13 Map Rendering & Tooltips
    story += [
        sp(4), h2("4.13 Map Rendering &amp; Tooltips"),
        p(
            "All 13 maps are drawn with the built-in <b>ecoscope-platform</b> map tasks "
            "rather than the earlier copies in <code>ecoscope-workflows-ext-custom</code>: "
            "<code>create_path_layer</code> (Movement Tracks, Subject Tracks), "
            "<code>create_scatterplot_layer</code> (Collaring Events), "
            "<code>create_geojson_layer</code> (all home range and raster/grid maps), and "
            "<code>draw_map</code> with <code>output_type: html</code>. Layer and legend "
            "styling is unchanged."
        ),
        p("Each layer's <code>tooltip_columns</code> sets what hovering shows:"),
        make_table(
            [
                ["Layer",                          "Tooltip columns"],
                ["Movement tracks",                "duration_status, subject_name"],
                ["Overall home range",             "percentile, area_sqkm"],
                ["Protected / unprotected home range", "etd_percentile_colors, percentile, area_sqkm"],
                ["Seasonal home range",            "season_colors, season"],
                ["Recursion events raster",        "value_bins"],
                ["Dry / wet mean speed raster",    "bins_formatted, value_bins"],
                ["Subject tracks, collaring events, filtered 99th home range, time of day dominance, night fixes",
                 "none (tooltip_columns: null)"],
            ],
            [7*cm, 9.5*cm],
        ),
        note(
            "<code>etd_percentile_colors</code> and <code>season_colors</code> hold the "
            "colour each feature is drawn with, so those tooltips show a raw colour value. "
            "Tooltips exist only on the HTML maps; the PNG screenshots and the Word report "
            "are static."
        ),
    ]

    # ── 5. Protection Status Analysis ─────────────────────────────────────────
    story += [
        sp(4), h1("5. Protection Status Analysis"), hr(),
        p(
            "In addition to the home range maps (Section 4.6), the workflow "
            "generates a <b>Protection Status Bar Chart</b> that summarises the "
            "proportion of trajectory fixes occurring inside versus outside protected "
            "land across all subjects and the full analysis period."
        ),
        p(
            "<code>plot_fix_protection_status</code> receives the full "
            "<code>protection_status</code>-annotated GeoDataFrame "
            "(from <code>generate_protected_column</code>) and renders an "
            "interactive bar chart grouped by protection status. "
            "The chart is persisted as both HTML and a 2× PNG screenshot."
        ),
    ]

    # ── 6. Word Report & Dashboard ────────────────────────────────────────────
    story += [
        sp(4), h1("6. Word Report &amp; Dashboard"), hr(),

        h2("6.1 Cover Page"),
        p(
            "The cover page template (<code>general_ele_cover_page.docx</code>) "
            "is downloaded automatically from Dropbox and populated by "
            "<code>create_mapbook_ctx_cover</code> with:"
        ),
        bullet("Total unique subject count (derived from <code>dataframe_column_nunique</code> on <code>subject_name</code>)"),
        bullet("Analysis time range (since / until)"),
        bullet("Prepared by: <i>Ecoscope</i>"),
        bullet("Organisation logo (user-supplied; fetched via <code>get_file_path</code> / Report logo task group)"),

        sp(4), h2("6.2 General Report Section"),
        p(
            "The per-run section template (<code>general_elephant_grouper_page.docx</code>) "
            "is downloaded from Dropbox and rendered by <code>general_template_context</code>. "
            "Map image boxes are <b>5.34 × 3.12 inches</b>. Screenshots are captured "
            "at 2× device scale factor with a 40 000 ms tile-load wait."
        ),

        sp(4), h2("6.3 Document Merge"),
        p(
            "<code>merge_mapbook_files</code> concatenates the cover page document "
            "and the general section into a single Word file, saved as the final "
            "combined report."
        ),

        sp(4), h2("6.4 Interactive Dashboard"),
        p(
            "<code>gather_dashboard</code> assembles the dashboard from workflow "
            "metadata (details, time range, groupers). The <code>widgets</code> "
            "list is empty for this workflow — the dashboard provides a summary "
            "view of run parameters rather than embedded map widgets."
        ),
    ]

    # ── 7. Output Files ───────────────────────────────────────────────────────
    story += [
        sp(4), h1("7. Output Files"), hr(),
        p(
            "All outputs are written to the directory defined by "
            "<code>ECOSCOPE_WORKFLOWS_RESULTS</code>."
        ),
        make_table(
            [
                ["File",                                          "Format",     "Content"],
                ["relocations.geoparquet",                        "GeoParquet", "Current period GPS fixes with day/night labels"],
                ["previous_period_relocations.geoparquet",        "GeoParquet", "Previous period GPS fixes"],
                ["trajectories.geoparquet",                       "GeoParquet", "Current period segments with season labels"],
                ["previous_period_trajectories.geoparquet",       "GeoParquet", "Previous period segments"],
                ["home_range_etd.geoparquet",                     "GeoParquet", "Overall ETD contours (50–99.9th percentiles)"],
                ["protected_areas_home_range_etd.geoparquet",     "GeoParquet", "ETD for fixes inside protected land"],
                ["unprotected_areas_home_range_etd.geoparquet",   "GeoParquet", "ETD for fixes outside protected land"],
                ["<subject>_seasonal_etd.geoparquet",             "GeoParquet", "Seasonal ETD polygons per subject"],
                ["seasonal_windows.csv",                          "CSV",        "NDVI-derived wet/dry season date ranges"],
                ["weighted_raster.*",                             "Raster",     "Recursion ecograph raster file"],
                ["movement_tracks.html / .png",                   "HTML / PNG", "Movement Tracks map (current + previous period)"],
                ["subject_tracks.html / .png",                    "HTML / PNG", "Subject Tracks map (coloured per individual)"],
                ["collared_points.html / .png",                   "HTML / PNG", "Elephant Sightings / Collaring Events map"],
                ["overall_homerange.html / .png",                 "HTML / PNG", "Overall ETD Home Range map"],
                ["filtered_homerange.html / .png",                "HTML / PNG", "Filtered 99th percentile Home Range map"],
                ["protected_areas.html / .png",                   "HTML / PNG", "Protected Areas Home Range map"],
                ["unprotected_areas.html / .png",                 "HTML / PNG", "Unprotected Areas Home Range map"],
                ["<subject>_seasonal_homerange.html / .png",      "HTML / PNG", "Seasonal Home Range per subject"],
                ["recursion_events.html / .png",                  "HTML / PNG", "Recursion Events raster map"],
                ["dry_mean_speed_raster_map.html / .png",         "HTML / PNG", "Dry Season Mean Speed raster map"],
                ["wet_mean_speed_raster_map.html / .png",         "HTML / PNG", "Wet Season Mean Speed raster map"],
                ["time_of_day_dominance.html / .png",             "HTML / PNG", "Time of Day Dominance grid map"],
                ["night_fixes.html / .png",                       "HTML / PNG", "Night Fixes grid map"],
                ["protection_status_bar.html / .png",             "HTML / PNG", "Protection Status bar chart"],
                ["general_cover_page.docx",                       "Word",       "Report cover page"],
                ["general.docx",                                  "Word",       "General per-subject report section"],
                ["<merged_report>.docx",                          "Word",       "Final combined Word report"],
            ],
            [6.5*cm, 2.5*cm, 7.5*cm],
        ),
    ]

    # ── 8. Workflow Execution Logic ───────────────────────────────────────────
    story += [
        sp(4), h1("8. Workflow Execution Logic"), hr(),

        h2("8.1 Grouping Strategy"),
        p(
            "The grouper is fixed to <code>subject_name</code>. Most maps operate "
            "at the group level (all subjects combined). Only the seasonal home range "
            "maps use <code>mapvalues</code> to fan out per subject — splitting the "
            "trajectory GeoDataFrame with <code>split_groups</code> and processing "
            "each subject independently."
        ),

        sp(4), h2("8.2 Skip Conditions"),
        p(
            "Every task carries two default skip conditions via "
            "<code>task-instance-defaults</code>:"
        ),
        bullet("<b>any_is_empty_df</b> — if any input DataFrame is empty, the task and all its dependants are skipped rather than raising an error."),
        bullet("<b>any_dependency_skipped</b> — if an upstream task was skipped, all downstream tasks are also skipped automatically."),
        p(
            "The <code>get_events_data</code> task carries an explicit "
            "<code>skipif</code> block with both conditions, ensuring that if no "
            "events are returned from EarthRanger the collaring events map pipeline "
            "is bypassed cleanly."
        ),

        sp(4), h2("8.3 Previous Period Logic"),
        p(
            "The previous period is determined by <code>flexible_previous_period</code>. "
            "In every mode, the comparison period's <b>end date</b> is fixed to the "
            "current time range's start date (so the two periods never overlap) — only "
            "the start date calculation differs. There are three modes:"
        ),
        make_table(
            [
                ["Mode",     "Behaviour"],
                ["Preset",   "Choose a common lookback — Same as current period, 1 month back, 3 months back, 6 months back, or 1 year back (default: Same as current period)"],
                ["Calendar", "Manually pick the exact start date for the comparison period"],
                ["Custom",   "Enter a Years / Months / Weeks / Days offset to count backward from the current time range's start date (default: 1 month back)"],
            ],
            [4*cm, 12.5*cm],
        ),
        p(
            "Default is the <b>Preset</b> mode with <b>Same as current period</b> "
            "selected (set in the spec's form overrides). It subtracts the length of the "
            "current time range from its start date, giving a comparison period of equal "
            "length immediately before it — e.g. a 1 Jul – 30 Sep range is compared with "
            "1 Apr – 1 Jul. The fixed presets subtract a calendar offset "
            "(<code>relativedelta</code>) from the start date instead."
        ),

        sp(4), h2("8.4 mapvalues Fan-out (Seasonal Home Range)"),
        p(
            "The seasonal home range pipeline uses <code>mapvalues</code> to iterate "
            "over the list produced by <code>split_groups</code>. Each subsequent "
            "task in the chain (<code>calculate_seasonal_home_range</code>, "
            "<code>convert_to_str</code>, <code>assign_season_colors</code>, "
            "<code>reproject_gdf</code>, <code>filter_df_cols</code>, "
            "<code>create_geojson_layer</code>, <code>envelope_gdf</code> / <code>compute_view_state_from_gdf</code>, "
            "<code>draw_map</code>, <code>html_to_png</code>) receives the "
            "<code>argvalues</code> list from its upstream task, processing one "
            "subject per invocation. <code>zip_groupbykey</code> aligns the "
            "per-subject map layers with their corresponding view states before "
            "the final <code>draw_map</code> call."
        ),
    ]

    # ── 9. Software Versions ──────────────────────────────────────────────────
    story += [
        sp(4), h1("9. Software Versions"), hr(),
        p(
            "As of the migration to the <b>ecoscope-platform</b> task/compiler runtime, "
            "the workflow's requirements are:"
        ),
        make_table(
            [
                ["Package",                       "Version",              "Role"],
                ["ecoscope-platform",              "==2.25.3",             "Core task library and workflow engine, including the map layer, draw_map and set_base_maps tasks (replaces ecoscope-workflows-core / -ext-ecoscope / -ext-big-life)"],
                ["ecoscope-workflows-ext-custom",  "0.1.4.*",              "Custom STE utility tasks (protection status, template context)"],
                ["ecoscope-workflows-ext-ste",     "0.0.24.*",             "STE-specific tasks (seasonal analysis, day/night, recursion, previous period, view state)"],
                ["pydeck",                         "0.9.2",                "Renders the interactive DeckGL maps"],
                ["opentelemetry-sdk",              ">=1.20.0, &lt;2.0.0",  "Workflow run telemetry/observability instrumentation"],
            ],
            [5.5*cm, 4*cm, 7*cm],
        ),
        note(
            "<code>ecoscope-workflows-ext-ecoscope</code> and "
            "<code>ecoscope-workflows-ext-big-life</code> are no longer direct "
            "dependencies — their task coverage now lives in <code>ecoscope-platform</code>."
        ),
        p(
            "<code>ecoscope-platform</code> is pulled from the "
            "<code>ecoscope-workflows</code> prefix.dev channel; the two "
            "<code>ecoscope-workflows-ext-*</code> packages from the "
            "<code>ecoscope-workflows-custom</code> channel; <code>pydeck</code> and "
            "<code>opentelemetry-sdk</code> from <code>conda-forge</code>. "
            "The runtime environment is managed by <b>pixi</b>."
        ),
    ]

    # ── Build PDF ──────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF written → {OUTPUT_FILE}")


if __name__ == "__main__":
    build()
