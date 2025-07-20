# --- Ekokardiografi App ---
import streamlit as st
import streamlit.components.v1 as components
from bs4 import BeautifulSoup
import os
import math

st.set_page_config(page_title="Ekokardiografi App", layout="wide")

tabs = st.tabs(["Patient", "Dimensioner", "Systolisk funktion", "Regionalitet", "Diastolisk funktion", "Klaffar", "Sammanfattning"])
regionalitet_findings = "Ingen regionalitet."
st.markdown("""
<style>
/* Tab text styling */
button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
    font-size: 18px !important;
    font-weight: bold !important;
    color: #003366 !important;
    margin: 0 !important;
    padding: 6px 14px !important;
}

/* Inactive tab styling */
button[data-baseweb="tab"] {
    background-color: #f9f9f9 !important;
    border-radius: 12px !important;
    border-bottom: 2px solid transparent !important;
    margin-right: 4px !important;
    transition: all 0.3s ease;
}

/* Active tab styling */
button[data-baseweb="tab"][aria-selected="true"] {
    background-color: #e6f0ff !important;
    border-radius: 12px !important;
    border-bottom: 3px solid #003366 !important;
}

/* Hover effect */
button[data-baseweb="tab"]:hover {
    background-color: #d0e2ff !important;
    border-radius: 12px !important;
    border-bottom: 2px solid #003366 !important;
}

/* Add space between tabs and the content below */
div[data-baseweb="tab-list"] {
    margin-bottom: 100px !important;
}
</style>
""", unsafe_allow_html=True)

# --- 🧝 Patientuppgifter ---
with tabs[0]:
    col1, col2 = st.columns(2)
    with col1:
        age_input = st.text_input("Ålder", value="")
        age = int(age_input) if age_input.isdigit() else 0
    with col2:
        weight_input = st.text_input("Vikt (kg)", value="")
        weight = int(weight_input) if weight_input.isdigit() else 0

    col3, col4 = st.columns(2)
    with col3:
        height_input = st.text_input("Längd (cm)", value="")
        height = int(height_input) if height_input.isdigit() else 0
    with col4:
        sex = st.selectbox("Kön", ["Man", "Kvinna"])

    bsa = round((height * weight / 3600) ** 0.5, 1) if height > 0 and weight > 0 else 0.0
    st.markdown(f"**BSA:** {bsa:.1f} m²")

    st.markdown("---")
    st.subheader("EKG")

    col5, col6 = st.columns(2)
    with col5:
        ekg_rytm = st.selectbox(
            "EKG-rytm",
            ["Sinusrytm", "Sinusbradykardi", "Förmaksflimmer", "Förmaksfladder",
             "Pacemakerrytm", "AV-block II", "AV-block III"]
        )
    with col6:
        ekg_freq_input = st.text_input("EKG-frekvens (spm)", value="")
        ekg_freq = int(ekg_freq_input) if ekg_freq_input.isdigit() else 0

# --- 🕝 Dimensioner ---
with tabs[1]:
    col1, col2, col3 = st.columns(3)
    with col1:
        ivsd_input = st.text_input("IVSd (mm)", value="")
        ivsd = int(ivsd_input) if ivsd_input.isdigit() else 0
    with col2:
        lvdd_input = st.text_input("LVIDd (mm)", value="")
        lvdd = int(lvdd_input) if lvdd_input.isdigit() else 0
    with col3:
        lvpwd_input = st.text_input("LVPWd (mm)", value="")
        lvpwd = int(lvpwd_input) if lvpwd_input.isdigit() else 0

    col4, col5, col6 = st.columns(3)
    with col4:
        aorta_input = st.text_input("Aorta ascendens (mm)", value="")
        aorta = int(aorta_input) if aorta_input.isdigit() else 0
    with col5:
        lavi_input = st.text_input("LAVI (ml/m²)", value="")
        lavi = int(lavi_input) if lavi_input.isdigit() else 0
    with col6:    
        ravi_input = st.text_input("RAVI (ml/m²)", value="")
        ravi = int(ravi_input) if ravi_input.isdigit() else 0
    # --- Equalis-baserad bedömning ---
    lvdd_status = "Normal"
    ivsd_status = "Normal"
    lvpwd_status = "Normal"

    if sex == "Man":
        if lvdd > 65:
            lvdd_status = "Kraftig dilaterad"
        elif lvdd > 61:
            lvdd_status = "Måttligt dilaterad"
        elif lvdd > 58:
            lvdd_status = "Lätt dilaterad"
        elif lvdd < 42:
            lvdd_status = "Mindre än normalt"

        if ivsd > 16:
            ivsd_status = "Uttalad hypertrofi"
        elif ivsd >= 14:
            ivsd_status = "Måttlig hypertrofi"
        elif ivsd >= 13:
            ivsd_status = "Lindrig hypertrofi"

        if lvpwd > 16:
            lvpwd_status = "Uttalad hypertrofi"
        elif lvpwd >= 14:
            lvpwd_status = "Måttlig hypertrofi"
        elif lvpwd >= 13:
            lvpwd_status = "Lindrig hypertrofi"

    elif sex == "Kvinna":
        if lvdd > 59:
            lvdd_status = "Kraftig dilaterad"
        elif lvdd > 55:
            lvdd_status = "Måttligt dilaterad"
        elif lvdd > 52:
            lvdd_status = "Lätt dilaterad"
        elif lvdd < 38:
            lvdd_status = "Mindre än normalt"

        if ivsd > 15:
            ivsd_status = "Uttalad hypertrofi"
        elif ivsd >= 13:
            ivsd_status = "Måttlig hypertrofi"
        elif ivsd >= 12:
            ivsd_status = "Lindrig hypertrofi"

        if lvpwd > 15:
            lvpwd_status = "Uttalad hypertrofi"
        elif lvpwd >= 13:
            lvpwd_status = "Måttlig hypertrofi"
        elif lvpwd >= 12:
            lvpwd_status = "Lindrig hypertrofi"

    # --- LAVI-tolkning ---
    if lavi <= 37:
        lavi_status = "Normal"
    elif 38 <= lavi <= 41:
        lavi_status = "Lätt ökad"
    elif 42 <= lavi <= 48:
        lavi_status = "Måttligt ökad"
    else:
        lavi_status = "Uttalad ökad"

    if sex == "Man":
        if ravi <= 36:
            ravi_status = "Normal"
        elif 37 <= ravi <= 42:
            ravi_status = "Lätt ökad"
        elif 43 <= ravi <= 48:
            ravi_status = "Måttligt ökad"
        else:
            ravi_status = "Uttalad ökad"
    elif sex == "Kvinna":
        if ravi <= 31:
            ravi_status = "Normal"
        elif 32 <= ravi <= 37:
            ravi_status = "Lätt ökad"
        elif 38 <= ravi <= 42:
            ravi_status = "Måttligt ökad"
        else:
            ravi_status = "Uttalad ökad"
    else:
        ravi_status = "Ej angivet"
    # --- Tolkning ---
    st.markdown("---")
    st.markdown("### Tolkning:")
    st.markdown(f"- **LVDD-status:** {lvdd_status}")
    st.markdown(f"- **IVSd-status:** {ivsd_status}")
    st.markdown(f"- **LVPWd-status:** {lvpwd_status}")
    st.markdown(f"- **LAVI-status:** {lavi_status} ({lavi} ml/m²)")
    st.markdown(f"- **RAVI-status:** {ravi_status} ({ravi} ml/m²)")
# --- 💓 Systolisk Funktion ---
with tabs[2]:
    col1, col2 = st.columns(2)
    with col1:
        ef_input = st.text_input("Ejektionsfraktion (EF %)", value="")
        ef = int(ef_input) if ef_input.isdigit() else 0
    with col2:
        stroke_volume_input = st.text_input("Slagvolym (ml)", value="")
        stroke_volume = int(stroke_volume_input) if stroke_volume_input.isdigit() else 0

    col3, col4 = st.columns(2)
    with col3:
        tapse_input = st.text_input("TAPSE (mm)", value="")
        tapse = int(tapse_input) if tapse_input.isdigit() else 0
    with col4:
        gls_input = st.text_input("Global Longitudinal Strain (GLS %)", value="")
        try:
            gls = float(gls_input) if gls_input else 0.0
        except ValueError:
            gls = 0.0

    # SVI calculation
    svi = round(stroke_volume / bsa, 1) if stroke_volume > 0 and bsa > 0 else 0.0

    # --- Tolkning ---
    st.markdown("---")
    st.markdown("### Tolkning:")

    # Slagvolym interpretation
    if sex == "Man":
        if stroke_volume < 60:
            sv_status = "Låg slagvolym"
        elif stroke_volume > 95:
            sv_status = "Hög slagvolym"
        else:
            sv_status = "Slagvolym inom normalintervall"
    else:
        if stroke_volume < 50:
            sv_status = "Låg slagvolym"
        elif stroke_volume > 75:
            sv_status = "Hög slagvolym"
        else:
            sv_status = "Slagvolym inom normalintervall"

    st.markdown(f"- **Slagvolym:** {stroke_volume} ml ({sv_status})")

    # SVI interpretation
    if stroke_volume > 0 and bsa > 0:
        if sex == "Man":
            if svi < 34:
                svi_status = "Lågt SVI"
            elif svi > 46:
                svi_status = "Högt SVI"
            else:
                svi_status = "Normalt SVI"
        else:
            if svi < 33:
                svi_status = "Lågt SVI"
            elif svi > 45:
                svi_status = "Högt SVI"
            else:
                svi_status = "Normalt SVI"

        st.markdown(f"- **SVI:** {svi} ml/m² ({svi_status})")

    # TAPSE interpretation
    if tapse > 0:
        if tapse >= 17:
            st.markdown(f"- **TAPSE:** {tapse} mm (normal)")
        else:
            st.markdown(f"- **TAPSE:** {tapse} mm (tecken till nedsatt högerkammarfunktion)")

# --- Aorta dilatation enligt Campens et al ---
def is_aorta_dilated(aorta, age, sex, bsa):
    if age <= 0:
        return False
    if sex == "Man":
        log10_pred = 1.033 + 0.188 * math.log10(age) + 0.070 * bsa
        log10_see = 0.0431
    else:
        log10_pred = 1.001 + 0.177 * math.log10(age) + 0.086 * bsa
        log10_see = 0.0453
    predicted = 10 ** log10_pred
    upper_limit = predicted * (10 ** (1.96 * log10_see))
    return aorta > upper_limit

# --- 🖼️ Regional Väggfunktion (SVG) ---
with tabs[3]:

    if os.path.exists("coronary_segments.svg"):
        with open("coronary_segments.svg", "r", encoding="utf-8") as svg_file:
            svg_raw = svg_file.read()

        soup = BeautifulSoup(svg_raw, "html.parser")

        # JavaScript for interactivity
        script = """
<script>
const independentSegments = ["Apical_lateral_PLAX", "Apical_inferior_A2C", "Apical_inferior_SAX"];
let selectedSegments = [];

function updateSegmentListDisplay() {
    const listDiv = document.getElementById("segment_display");
    const segmentStatus = JSON.parse(localStorage.getItem("segmentStatus") || "{}");

    let groupedSegments = {};
    selectedSegments.forEach(seg => {
        let base = seg.replace(/_(A4C|A2C|PLAX|SAX)$/i, "");
        if (independentSegments.includes(seg)) {
            groupedSegments[seg] = seg;
        } else {
            if (!groupedSegments[base]) groupedSegments[base] = seg;
        }
    });

    listDiv.innerHTML = Object.entries(groupedSegments).map(([baseOrFull, rep]) => {
        let label = rep.replace(/_(A4C|A2C|PLAX|SAX)$/i, "").replaceAll("_", " ");
        return `
            <div style='margin-bottom: 10px;'>
                <label style='font-weight: bold;'>${label}:</label>
                <select onchange="updateStatus('${rep}', this.value)" style='background-color: #003366; color: white; border-radius: 6px; padding: 4px;'>
                    <option value="">Välj status</option>
                    <option value="Hypokinesi">Hypokinesi</option>
                    <option value="Akinesi">Akinesi</option>
                </select>
            </div>
        `;
    }).join("");

    updateSummaryText();
}

function updateStatus(segment, status) {
    let stored = JSON.parse(localStorage.getItem("segmentStatus") || "{}");
    stored[segment] = status;
    localStorage.setItem("segmentStatus", JSON.stringify(stored));
    updateSummaryText();
}

function updateSummaryText() {
    const lad = ["Apex_A4C", "Apical_septal_A4C", "Apex_A2C", "Apical_anterior_A2C", "Mid_anterior_A2C", "Basal_anterior_A2C", "Apex_PLAX", "Apical_anterior_PLAX", "Mid_anteroseptal_PLAX", "Basal_anteroseptal_PLAX", "Basal_anterior_SAX", "Basal_anteroseptal_SAX", "Mid_anterior_SAX", "Mid_anteroseptal_SAX", "Apical_anterior_SAX", "Apical_septal_SAX"];
    const lad_lcx = ["Apical_lateral_A4C", "Apical_lateral_SAX", "Mid_anterolateral_SAX", "Basal_anterolateral_SAX", "Basal_anterolateral_A4C", "Mid_anterolateral_A4C"];
    const rca = ["Basal_inferoseptal_A4C", "Basal_inferoseptal_SAX", "Basal_inferior_SAX", "Basal_inferior_A2C", "Mid_inferior_A2C", "Mid_inferior_SAX"];
    const rca_lad = ["Mid_inferoseptal_A4C", "Mid_inferoseptal_SAX"];
    const rca_lcx = ["Mid_inferolateral_PLAX", "Basal_inferolateral_PLAX", "Basal_inferolateral_SAX", "Mid_inferolateral_SAX"];

    const segStat = JSON.parse(localStorage.getItem("segmentStatus") || "{}");
    const grouped = {};
    for (const [segment, status] of Object.entries(segStat)) {
        if (!selectedSegments.includes(segment)) continue;
        if (!["Hypokinesi", "Akinesi"].includes(status)) continue;
        const label = segment.replace(/_(A4C|A2C|PLAX|SAX)$/i, "").replaceAll("_", " ");
        grouped[status] = grouped[status] || [];
        if (!grouped[status].includes(label)) grouped[status].push(label);
    }

    const summary = Object.entries(grouped)
        .map(([status, segments]) => `<strong>${status}:</strong> ${segments.join(", ")}`)
        .join("<br>");
    document.getElementById("summary_display").innerHTML = summary || "";

    let alerts = [];
    const addAlert = (text) => {
        if (!alerts.includes(text)) alerts.push(text);
    };

    const has = (arr) => arr.some(id => selectedSegments.includes(id) && ["Hypokinesi", "Akinesi"].includes(segStat[id]));

    if (has(lad)) addAlert(`<span style='background-color:#f0f4f8;color:purple;padding:3px 6px;font-weight:bold;font-size:18px;'>Misstänkt LAD skada</span>`);
    if (has(lad_lcx)) addAlert(`<span style='background-color:#f0f4f8;color:orange;padding:3px 6px;font-weight:bold;font-size:18px;'>Misstänkt LAD elle LCx skada</span>`);
    if (has(rca)) addAlert(`<span style='background-color:#f0f4f8;color:red;padding:3px 6px;font-weight:bold;font-size:18px;'>Misstänkt RCA skada</span>`);
    if (has(rca_lad)) addAlert(`<span style='background-color:#f0f4f8;color:blue;padding:3px 6px;font-weight:bold;font-size:18px;'>Misstänkt RCA eller LAD skada</span>`);
    if (has(rca_lcx)) addAlert(`<span style='background-color:#f0f4f8;color:green;padding:3px 6px;font-weight:bold;font-size:18px;'>Misstänkt RCA eller LCx skada</span>`);

    // Independent segments
    if (segStat["Apical_lateral_PLAX"] && ["Hypokinesi", "Akinesi"].includes(segStat["Apical_lateral_PLAX"])) {
        addAlert(`<span style='background-color:#f0f4f8;color:purple;padding:3px 6px;font-weight:bold;font-size:18px;'>Misstänkt LAD skada</span>`);
    }
    if (segStat["Apical_inferior_A2C"] && ["Hypokinesi", "Akinesi"].includes(segStat["Apical_inferior_A2C"])) {
        addAlert(`<span style='background-color:#f0f4f8;color:red;padding:3px 6px;font-weight:bold;font-size:18px;'>Misstänkt RCA skada</span>`);
    }
    if (segStat["Apical_inferior_SAX"] && ["Hypokinesi", "Akinesi"].includes(segStat["Apical_inferior_SAX"])) {
        addAlert(`<span style='background-color:#f0f4f8;color:blue;padding:3px 6px;font-weight:bold;font-size:18px;'>Misstänkt RCA eller LAD skada</span>`);
    }

    document.getElementById("alert_display").innerHTML = alerts.join("<br>");
}

function toggleSegment(id) {
    const base = id.replace(/_(A4C|A2C|PLAX|SAX)$/i, "");
    const isIndependent = independentSegments.includes(id);

    let matches = [id];
    if (!isIndependent) {
        matches = Array.from(document.querySelectorAll('[id]')).map(el => el.id)
            .filter(s => {
                const sBase = s.replace(/_(A4C|A2C|PLAX|SAX)$/i, "");
                return sBase === base && !independentSegments.includes(s);
            });
    }

    const allSelected = matches.every(s => selectedSegments.includes(s));
    matches.forEach(s => {
        const el = document.getElementById(s);
        if (!el) return;
        if (allSelected) {
            selectedSegments = selectedSegments.filter(seg => seg !== s);
            el.style.stroke = "#999"; el.style.strokeWidth = "1";
        } else {
            if (!selectedSegments.includes(s)) selectedSegments.push(s);
            el.style.stroke = "blue"; el.style.strokeWidth = "3";
        }
    });

    localStorage.setItem("selectedSegments", JSON.stringify(selectedSegments));
    updateSegmentListDisplay();
}

function resetSelections() {
    selectedSegments = [];
    localStorage.removeItem("selectedSegments");
    localStorage.removeItem("segmentStatus");
    document.querySelectorAll('[id]').forEach(el => {
        el.style.stroke = "#999"; el.style.strokeWidth = "1";
    });
    document.getElementById("summary_display").innerHTML = "";
    document.getElementById("alert_display").innerHTML = "";
    updateSegmentListDisplay();
}

window.onload = () => {
    selectedSegments = JSON.parse(localStorage.getItem("selectedSegments") || "[]");
    selectedSegments.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.style.stroke = "yellow";
            el.style.strokeWidth = "3";
        }
    });
    updateSegmentListDisplay();
};
</script>
"""

        for tag in soup.find_all(["path", "polygon", "rect", "ellipse"]):
            if tag.has_attr("id"):
                seg_id = tag["id"]
                tag["onclick"] = f"toggleSegment('{seg_id}')"

        modified_svg = str(soup)
        # CSS styles for SVG and layout
        style_block = """
<style>
svg {
    width: 100vw;
    height: auto;
    max-height: 70vh;
    display: block;
    margin: auto;
}

#segment_display {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 20px;
    justify-content: flex-start;
}

#segment_display > div {
    flex: 0 0 auto;
    width: 220px;
    display: flex;
    flex-direction: column;
    align-items: stretch;
}

#segment_display label {
    width: 96%;
    padding: 3px;
    font-size: 18px;
    border-radius: 6px;
    border: 1px solid #ccc;
    background-color: #003366;
    color: yellow;
}

#segment_display select {
    width: 100%;
    padding: 8px;
    font-size: 15px;
    border-radius: 6px;
    border: 1px solid #ccc;
    background-color: #003366;
    color: white;
}

/* 📱 Mobile responsiveness */
@media (max-width: 768px) {
    h2 {
        margin-bottom: 10px !important;
    }

    #segment_display {
        margin-bottom: 5px !important;
        justify-content: center;
    }

    #segment_display > div,
    #combined_display {
        flex: 1 1 100%;
        width: 100%;
    }

    .block-container {
        padding-bottom: 10px !important;
    }
}
</style>
"""

        # Inject into Streamlit
        components.html(
            style_block + script + modified_svg + """
<script>
window.addEventListener('DOMContentLoaded', function() {
    const height = window.innerWidth <= 768 ? 1400 : 5000;
    const streamlitIframe = window.frameElement;
    if (streamlitIframe) {
        streamlitIframe.style.height = height + 'px';
    }
});
</script>

<!-- 🔄 Reset Button -->
<div style="display: flex; justify-content: center; margin-top: 20px;">
    <button onclick="resetSelections()" style="
        padding: 8px 16px;
        font-size: 16px;
        border: 2px solid #ccc;
        border-radius: 6px;
        background-color: #003366;
        color: yellow;
        font-weight: bold;
        white-space: nowrap;
    ">
        Återställ
    </button>
</div>

<!-- 📍 Segment Display Area -->
<div id="segment_display" style="margin-top:20px; font-size:18px;"></div>

<!-- 📋 Summary and Alerts Display -->
<div id="combined_display" style="
    margin: 20px auto 40px auto;
    padding: 12px 20px;
    border: 2px solid #003366;
    border-radius: 12px;
    background-color: #f0f4f8;
    max-width: 900px;
    width: 90%;
    box-sizing: border-box;
    text-align: left;
">
    <div id="summary_display" style="font-size:20px; margin-bottom: 12px;"></div>
    <div id="alert_display" style="font-size:18px;"></div>
</div>

""",
    height=0,
    scrolling=False
)

# --- 💓 Diastolisk Funktion (bedömning av fyllnadstryck) ---
with tabs[4]:
    st.subheader("Diastolisk Funktion (bedömning av fyllnadstryck)")

    with st.expander("**OBSERVANDUM!**", expanded=False):
        st.markdown("""
        - **LAVI** är ej bedömbart vid mer än lindrigt mitralisvitium och svårtolkat vid intermittent **förmaksflimmer**.
        - **E/e′** bör ej bedömas vid mitralisvitium, protes, annulusförkalkning, pacemakerrytm, LBBB, prekapillär pulmonell hypertension, tricuspidalisinsufficiens, konstriktiv perikardit.
        - **E/A-kvot** svårbedömd vid sinusrytm med intermittent förmaksflimmer samt vid takykardi.
        - Vid **förmaksflimmer** saknas goda riktlinjer för bedömning av fyllnadstrycket.
        """)

    col1, col2 = st.columns(2)
    with col1:
        cvp = st.selectbox("Centralvenöst tryck (CVT mmHg)", [5, 10, 15], key="cvp_dia")
    with col2:
        tr_gradient_option = st.selectbox("TI-gradient tillgänglig?", ["Ej mätbar", "Ange värde"], key="tr_option_dia")

    if tr_gradient_option == "Ange värde":
        tr_gradient_input = st.text_input("TI-gradient (mmHg)", value="", key="tr_value_dia")
        try:
            tr_gradient = float(tr_gradient_input)
        except ValueError:
            tr_gradient = 0.0
        pa_pressure = round(tr_gradient + cvp, 1)
    else:
        pa_pressure = None

    col3, col4 = st.columns(2)
    with col3:
        e_wave_input = st.text_input("E-våg (m/s)", value="")
        try:
            e_wave = float(e_wave_input) if e_wave_input else 0.0
        except ValueError:
            e_wave = 0.0

        e_prime_septal_input = st.text_input("e′ septal (cm/s)", value="")
        try:
            e_prime_septal = float(e_prime_septal_input) if e_prime_septal_input else 0.0
        except ValueError:
            e_prime_septal = 0.0

    with col4:
        a_wave_input = st.text_input("A-våg (m/s)", value="")
        try:
            a_wave = float(a_wave_input) if a_wave_input else 0.0
        except ValueError:
            a_wave = 0.0

        e_prime_lateral_input = st.text_input("e′ lateral (cm/s)", value="")
        try:
            e_prime_lateral = float(e_prime_lateral_input) if e_prime_lateral_input else 0.0
        except ValueError:
            e_prime_lateral = 0.0

    col5, col6 = st.columns(2)
    with col5:
        pv_flow = st.selectbox("Pulmonell venflöde (S/D)", ["Ej angivet", "S > D", "S < D"])
    with col6:
        pva_duration_input = st.text_input("PV-a duration (ms)", value="")
        try:
            pva_duration = int(pva_duration_input)
        except ValueError:
            pva_duration = 0

    a_dur_input = st.text_input("A-vågs duration (ms)", value="")
    try:
        a_dur = int(a_dur_input)
    except ValueError:
        a_dur = 0

    # --- Beräkningar ---
    e_a_ratio = round(e_wave / a_wave, 1) if a_wave > 0 else 0
    e_wave_cm_s = e_wave * 100

    if e_prime_septal > 0 and e_prime_lateral > 0:
        e_prime_avg = round((e_prime_septal + e_prime_lateral) / 2, 1)
    elif e_prime_septal > 0:
        e_prime_avg = e_prime_septal
    elif e_prime_lateral > 0:
        e_prime_avg = e_prime_lateral
    else:
        e_prime_avg = 0.0

    e_e_prime = round(e_wave_cm_s / e_prime_avg, 1) if e_prime_avg > 0 else 0

    # --- Bedömning ---
    age_threshold_high = 2.0 if age < 55 else 1.8 if age <= 64 else 1.5
    diastolic_function_text = ""

    if e_a_ratio <= 0.8 and e_wave_cm_s <= 50:
        diastolic_function_text = "Normalt fyllnadstryck."
    elif e_a_ratio > age_threshold_high:
        diastolic_function_text = "Tecken till förhöjt fyllnadstryck."
    else:
        assessable = []
        positive = 0
        if lavi > 37:
            positive += 1
        assessable.append("LAVI")

        if pa_pressure is not None:
            assessable.append("PA")
            if pa_pressure > 35:
                positive += 1

        if e_e_prime > 0:
            assessable.append("E/e′")
            if e_e_prime > 14:
                positive += 1

        if len(assessable) >= 3:
            diastolic_function_text = "Tecken till förhöjt fyllnadstryck." if positive >= 2 else "Normalt fyllnadstryck."
        elif len(assessable) == 2 and positive == 1:
            diastolic_function_text = "Fyllnadstryck kan ej bedömas."
        elif positive == len(assessable):
            diastolic_function_text = "Tecken till förhöjt fyllnadstryck."
        else:
            diastolic_function_text = "Normalt fyllnadstryck."

    # --- Extra bevis ---
    extra_positive = False
    if (pv_flow == "S < D" and age > 50) or (pva_duration > 0 and a_dur > 0 and (pva_duration - a_dur) > 30):
        extra_positive = True

    if diastolic_function_text == "Normalt fyllnadstryck." and extra_positive:
        diastolic_function_text = "Tecken till förhöjt fyllnadstryck."

    # --- Utskrift ---
    st.markdown("### Bedömning")
    if diastolic_function_text:
        st.markdown(f"**{diastolic_function_text}**")

    st.markdown("### Parametrar")
    e_a_text = f"**E/A: {e_a_ratio} (ålder {age})**" if e_a_ratio > age_threshold_high or (e_a_ratio <= 0.8 and e_wave_cm_s <= 50) else f"E/A: {e_a_ratio}"
    e_e_prime_text = f"**E/e′: {e_e_prime}**" if e_e_prime > 14 else f"E/e′: {e_e_prime}" if e_e_prime > 0 else "E/e′: Ej angivet"
    lavi_text = f"**LAVI: {lavi} ml/m²**" if lavi > 37 else f"LAVI: {lavi} ml/m²"
    pa_text = f"**PA-tryck: {pa_pressure:.0f} mmHg**" if pa_pressure and pa_pressure > 35 else f"PA-tryck: {pa_pressure:.0f} mmHg" if pa_pressure else "PA-tryck: Ej angivet"

    st.markdown(f"- {e_a_text}")
    st.markdown(f"- {e_e_prime_text}")
    st.markdown(f"- {lavi_text}")
    st.markdown(f"- {pa_text}")

    if pv_flow == "S < D" and age > 50:
        st.markdown("- **Pulmonell venflöde: S < D hos patient >50 år**")
    if pva_duration > 0 and a_dur > 0 and (pva_duration - a_dur) > 30:
        st.markdown(f"- **PV-a duration längre än A-våg med {pva_duration - a_dur} ms**")

# --- 🩺 Klafffunktion ---
with tabs[5]:
    col1, col2, col3 = st.columns(3)

    # --- Initiering av variabler ---
    aortic_vmax = mean_pg = ava = vena_contracta_ai = pht_ai = calcium_score = 0.0
    lvot_diameter = lvot_vti = aortic_vti = ava_calc = avai = dvi = 0.0
    aorta_pathology = []
    aorta_stenosis_severity = aorta_insuff_severity = None
    auto_detected_aorta_stenosis = None
    mva = mitral_pht = mean_mitral_gradient = pasp = 0
    mitral_lvot_vti_ratio = pulm_vein_reversal = ""
    mitral_pathology = []
    mitral_stenosis_severity = mitral_insuff_severity = None
    ti_grade = "Ingen"
    vena_contracta_tr = 0.0

    with col1:
        st.markdown("### Aortaklaff")
        aorta_morphology = st.selectbox("Aortaklaff morfologi", ["Trikuspid", "Bikuspid"], key="aorta_morphology")
        use_manual_aorta = st.radio("Bedömning av aortaklaff", ["Manuell bedömning", "Avancerade parametrar"], horizontal=True, key="aorta_mode")

        if use_manual_aorta == "Manuell bedömning":
            aorta_pathology = st.multiselect("Aortaklaff patologi", ["Stenos", "Insufficiens"], key="aorta_patho")
            if "Stenos" in aorta_pathology:
                aorta_stenosis_severity = st.selectbox("Grad av aortastenos", ["Lindrig", "Måttlig", "Uttalad"], key="aorta_stenosis")
            if "Insufficiens" in aorta_pathology:
                aorta_insuff_severity = st.selectbox("Grad av aortainsufficiens", ["Lindrig", "Måttlig", "Uttalad"], key="aorta_insuff")
        else:
            with st.expander("Avancerade parametrar – Aortastenos"):
                st.markdown("""
                #### Hjälptext 
                - **Vmax (m/s): ≥ 4.0** = uttalad stenos; **3.0–3.9** = måttlig; **2.6–2.9** = lindrig.
                - **Medelgradient (mmHg):** **≥ 40** = uttalad stenos, **20–39** = måttlig.
                - **AVA (cm²):** **< 1.0** = uttalad, **1.0–1.5** = måttlig; **> 1.5** = lindrig
                - **AVA indexerad (AVAi, cm²/m²):** **< 0.6** = uttalad stenos, **0.6-0.85** = måttlig
                - **DVI (dimensionless index):** **< 0.25** = uttalad stenos, **0.25–0.5** = måttlig, 
                - **Calciumscore (Agatston):** **≥ 2000 hos män** och **≥ 1200 hos kvinnor** talar för uttalad stenos. Används vid **LFLG AS**
                - Tolkning bör göras i relation till **stroke volume index (SVI)** och **EF**, särskilt vid lågflödesbilder.
                """)

                aortic_vmax = float(st.text_input("Maxhastighet (Vmax, m/s)", value="", key="aortic_vmax") or 0)
                mean_pg = int(st.text_input("Medelgradient (mmHg)", value="", key="mean_pg") or 0)
                ava = float(st.text_input("Aortaklaffarea (planimetrisk, cm²)", value="", key="ava_plan") or 0)
                lvot_diameter = float(st.text_input("LVOT-diameter (cm)", value="") or 0)
                lvot_vti = float(st.text_input("LVOT VTI (cm)", value="") or 0)
                aortic_vti = float(st.text_input("Aortaklaff VTI (cm)", value="") or 0)
                calcium_score = int(st.text_input("Calcium score (Agatston)", value="") or 0)

                # --- Beräkna AVA (kontinuitet) ---
                if lvot_diameter > 0 and lvot_vti > 0 and aortic_vti > 0:
                    lvot_area = 3.1416 * (lvot_diameter / 2) ** 2
                    ava_calc = round((lvot_area * lvot_vti) / aortic_vti, 2)
                    dvi = round(lvot_vti / aortic_vti, 2)
                    avai = round(ava_calc / bsa, 2) if bsa > 0 else 0.0

                # --- Klassificering endast om värden finns ---
                if any([aortic_vmax > 0, ava > 0, ava_calc > 0, dvi > 0]):
                    aorta_pathology.append("Stenos")
                    if any([
                        aortic_vmax >= 4.0, mean_pg >= 40,
                        ava < 1.0, ava_calc < 1.0, dvi < 0.25
                    ]):
                        aorta_stenosis_severity = "Uttalad"
                    elif any([
                        3.0 <= aortic_vmax < 4.0, 20 <= mean_pg < 40,
                        1.0 <= ava < 1.5, 1.0 <= ava_calc < 1.5
                    ]):
                        aorta_stenosis_severity = "Måttlig"
                    else:
                        aorta_stenosis_severity = "Lindrig"

            # --- Visning ---
            if aortic_vmax > 0:
                if aortic_vmax >= 4.0:
                    vmax_grade = "Uttalad aortastenos"
                elif aortic_vmax >= 3.0:
                    vmax_grade = "Måttlig aortastenos"
                elif aortic_vmax >= 2.6:
                    vmax_grade = "Lindrig aortastenos"
                else:
                    vmax_grade = ""
                st.markdown(f"- **Vmax:** {aortic_vmax} m/s {vmax_grade}")

            if mean_pg > 0:
                if mean_pg >= 40:
                    pg_grade = "Uttalad aortastenos"
                elif mean_pg >= 20:
                    pg_grade = "Måttlig aortastenos"
                elif mean_pg >= 15:
                    pg_grade = "Lindrig aortastenos"
                else:
                    pg_grade = ""
                st.markdown(f"- **Medelgradient:** {mean_pg} mmHg {pg_grade}")

            if ava > 0:
                if ava < 1.0:
                    ava_grade = "Uttalad aortastenos"
                elif ava < 1.5:
                    ava_grade = "Måttlig aortastenos"
                else:
                    ava_grade = ""
                st.markdown(f"- **Planimetrisk AVA:** {ava} cm² {ava_grade}")

            if ava_calc > 0:
                if ava_calc < 1.0:
                    ava_calc_grade = "Uttalad aortastenos"
                elif ava_calc < 1.5:
                    ava_calc_grade = "Måttlig aortastenos"
                else:
                    ava_calc_grade = ""
                st.markdown(f"- **Beräknad AVA (kontinuitet):** {ava_calc} cm² {ava_calc_grade}")

            if avai > 0:
                st.markdown(f"- **AVAi:** {avai} cm²/m²")

            if dvi > 0:
                st.markdown(f"- **DVI:** {dvi}")

            if calcium_score > 0:
                calcium_grade = "(Uttalad Calciumscore)" if (
                    (sex == "Man" and calcium_score >= 2000) or
                    (sex == "Kvinna" and calcium_score >= 1200)
                ) else ""
                st.markdown(f"- **Calciumscore:** {calcium_score} Agatston {calcium_grade}")

            if svi > 0 and ava_calc < 1.0 and mean_pg < 40:
                if ef < 50:
                    st.markdown(f"- ⚠️ **Low-flow, low-gradient AS med reducerad EF misstänks** "
                                f"(AVA: {ava_calc} cm², PG: {mean_pg} mmHg, SVI: {svi} ml/m², EF: {ef}%)")
                elif ef >= 50 and svi < 35:
                    st.markdown(f"- ⚠️ **Paradoxal low-flow, low-gradient AS misstänks** "
                                f"(AVA: {ava_calc} cm², PG: {mean_pg} mmHg, SVI: {svi} ml/m², EF: {ef}%)")

        # --- Avancerade parametrar: Aortainsufficiens ---
            with st.expander("Avancerade parametrar – Aortainsufficiens"):
                vena_contracta_ai = float(st.text_input("Vena Contracta AI (cm)", value="", key="vc_ai") or 0)
                pht_ai = int(st.text_input("Pressure Half-Time AI (ms)", value="", key="pht_ai") or 0)
                diastolic_flow_reversal = st.selectbox(
                    "Diastoliskt backflöde i aorta descendens", ["Nej", "Ja"],
                    help="Backflöde tyder på uttalad AI"
                )

                if vena_contracta_ai > 0 or pht_ai > 0 or diastolic_flow_reversal == "Ja":
                    if any([vena_contracta_ai > 0.3, pht_ai < 250, diastolic_flow_reversal == "Ja"]):
                        aorta_pathology.append("Insufficiens")
                        if vena_contracta_ai >= 0.6 or pht_ai < 200:
                            aorta_insuff_severity = "Uttalad"
                        elif 0.4 <= vena_contracta_ai < 0.6 or 200 <= pht_ai < 250:
                            aorta_insuff_severity = "Måttlig"
                        else:
                            aorta_insuff_severity = "Lindrig"
    with col2:
        st.markdown("### Mitralisklaff")
        use_manual_mitral = st.radio("Bedömning av mitralisklaff", ["Manuell bedömning", "Avancerade parametrar"], horizontal=True)

        if use_manual_mitral == "Manuell bedömning":
            mitral_pathology = st.multiselect("Mitralisklaff patologi", ["Stenos", "Insufficiens"])
            if "Stenos" in mitral_pathology:
                mitral_stenosis_severity = st.selectbox("Grad av mitralisstenos", ["Lindrig", "Måttlig", "Uttalad"])
            if "Insufficiens" in mitral_pathology:
                mitral_insuff_severity = st.selectbox("Grad av mitralisinsufficiens", ["Lindrig", "Måttlig", "Uttalad"])

        else:
            with st.expander("Avancerade parametrar – Mitralisstenos"):
                mva_input = st.text_input("Mitralisarea (cm²)", value="", help="**MVA:** Uttalad < 1.0 cm², Måttlig 1.0–1.5 cm²")
                try:
                    mva = float(mva_input) if mva_input else 0.0
                except ValueError:
                    mva = 0.0

                mitral_pht_input = st.text_input("Pressure Half-Time (ms)", value="", help="**PHT:** Uttalad > 220 ms")
                mitral_pht = int(mitral_pht_input) if mitral_pht_input.isdigit() else 0

                mean_mitral_gradient_input = st.text_input("Medelgradient (mmHg)", value="", help="**Mean Gradient:** Uttalad > 10 mmHg, Måttlig 5–10 mmHg, Lindrig < 5 mmHg")
                mean_mitral_gradient = int(mean_mitral_gradient_input) if mean_mitral_gradient_input.isdigit() else 0

                pasp_input = st.text_input("Pulmonellt artärtryck (PASP, mmHg)", value="", help="**PASP:** Uttalad > 50 mmHg, Måttlig 30–50 mmHg, Lindrig < 30 mmHg")
                pasp = int(pasp_input) if pasp_input.isdigit() else 0

                if mva > 0 and mva < 1.5:
                    mitral_pathology.append("Stenos")
                    mitral_stenosis_severity = "Uttalad" if mva < 1.0 else "Måttlig"

            with st.expander("Avancerade parametrar – Mitralisinsufficiens"):
                vena_contracta_mr_input = st.text_input("Vena Contracta MR (cm)", value="", help="**VC MR:** Uttalad ≥ 0.7 cm, Måttlig 0.4–0.69 cm, Lindrig < 0.3 cm")
                try:
                    vena_contracta_mr = float(vena_contracta_mr_input) if vena_contracta_mr_input else 0.0
                except ValueError:
                    vena_contracta_mr = 0.0

                mitral_vti_input = st.text_input("Mitralis VTI (cm)", value="", help="För flödesanalys")
                try:
                    mitral_vti = float(mitral_vti_input) if mitral_vti_input else 0.0
                except ValueError:
                    mitral_vti = 0.0

                if mitral_vti > 0 and lvot_vti > 0:
                    mitral_lvot_vti_ratio = round(lvot_vti / mitral_vti, 2)

                pulm_vein_reversal = st.selectbox("Systolisk reversering i lungvenerna?", ["Nej", "Ja"], help="Tyder på uttalad insufficiens")

                if vena_contracta_mr > 0.3:
                    mitral_pathology.append("Insufficiens")
                    if vena_contracta_mr >= 0.7 or pulm_vein_reversal == "Ja":
                        mitral_insuff_severity = "Uttalad"
                    elif 0.4 <= vena_contracta_mr < 0.7:
                        mitral_insuff_severity = "Måttlig"
                    else:
                        mitral_insuff_severity = "Lindrig"

            st.markdown("#### 🔍 Tolkning – Mitralisstenos")
            if mva > 0:
                if mva < 1.0:
                    severity = "Uttalad mitralisstenos"
                elif mva <= 1.5:
                    severity = "Måttlig mitralisstenos"
                else:
                    severity = "Lindrig eller ingen mitralisstenos"
                st.markdown(f"- **MVA:** {mva} cm² ({severity})")

            if mitral_pht > 0:
                st.markdown(f"- **PHT:** {mitral_pht} ms")

            if mean_mitral_gradient > 0:
                if mean_mitral_gradient > 10:
                    st.markdown(f"- **Medelgradient:** {mean_mitral_gradient} mmHg (Uttalad)")
                elif mean_mitral_gradient >= 5:
                    st.markdown(f"- **Medelgradient:** {mean_mitral_gradient} mmHg (Måttlig)")
                else:
                    st.markdown(f"- **Medelgradient:** {mean_mitral_gradient} mmHg (Lindrig)")

            if pasp > 0:
                if pasp > 50:
                    st.markdown(f"- **PASP:** {pasp} mmHg (Uttalad)")
                elif pasp >= 30:
                    st.markdown(f"- **PASP:** {pasp} mmHg (Måttlig)")
                else:
                    st.markdown(f"- **PASP:** {pasp} mmHg (Lindrig)")

    with col3:
        st.markdown("### Trikuspidalisklaff")
        use_manual_tricuspid = st.radio("Bedömning av trikuspidalisklaff", ["Manuell bedömning", "Avancerade parametrar"], horizontal=True)

        if use_manual_tricuspid == "Manuell bedömning":
            ti_grade = st.selectbox("Grad av trikuspidalinsufficiens (manuell)", ["Ingen", "Lindrig", "Måttlig", "Uttalad"])
        else:
            with st.expander("Avancerade parametrar – Trikuspidalisklaff"):
                vena_contracta_tr_input = st.text_input("Vena Contracta TR (cm)", value="", help="**VC TR:** Uttalad ≥ 0.7 cm, Måttlig 0.4–0.69 cm, Lindrig 0.1–0.39 cm, Ingen < 0.1 cm")
                try:
                    vena_contracta_tr = float(vena_contracta_tr_input) if vena_contracta_tr_input else 0.0
                except ValueError:
                    vena_contracta_tr = 0.0

                if vena_contracta_tr >= 0.7:
                    ti_grade = "Uttalad"
                elif 0.4 <= vena_contracta_tr < 0.7:
                    ti_grade = "Måttlig"
                elif 0.1 <= vena_contracta_tr < 0.4:
                    ti_grade = "Lindrig"
                else:
                    ti_grade = "Ingen"

            st.markdown("#### 🔍 Tolkning – Trikuspidalisinsufficiens")
            if vena_contracta_tr > 0:
                st.markdown(f"- **Vena Contracta TR:** {vena_contracta_tr} cm")
            st.markdown(f"- **Bedömd grad:** {ti_grade}")
# --- 📝 Sammanfattning ---
with tabs[6]:
    st.markdown("<h2 style='text-align: center;'>Sammanfattning</h2>", unsafe_allow_html=True)

    # --- Patientinfo ---
    patient_info = (
        f"\u00c5lder: {age:.0f} \u00e5r, "
        f"Vikt: {weight:.0f} kg, "
        f"L\u00e4ngd: {height:.0f} cm, "
        f"BSA: {bsa:.1f} m², "
        f"Rytm: {ekg_rytm.lower()} med frekvens {ekg_freq:.0f} /min."
    )

    findings = ""

    # --- Systolisk Funktion ---
    if lvdd > 0:
        if lvdd_status == "Normal":
            findings += f"Normalstor vänsterkammare i diastole ({lvdd} mm). "
        elif "dilaterad" in lvdd_status.lower():
            findings += f"{lvdd_status.capitalize()} vänsterkammare i diastole ({lvdd} mm). "
        else:
            findings += f"{lvdd_status.capitalize()} dilaterad vänsterkammare i diastole ({lvdd} mm). "

    # --- Hypertrofi ---
    def clean_hypertrofi_term(status: str) -> str:
        return status.replace("hypertrofi", "").strip().capitalize()

    if ivsd > 0 and lvpwd > 0:
        if ivsd_status == "Normal" and lvpwd_status == "Normal":
            findings += f"Ingen hypertrofi (septum {ivsd} mm, bakvägg {lvpwd} mm). "
        else:
            if ivsd_status != "Normal":
                findings += f"{clean_hypertrofi_term(ivsd_status)} hypertrofi i septum ({ivsd} mm). "
            if lvpwd_status != "Normal":
                findings += f"{clean_hypertrofi_term(lvpwd_status)} hypertrofi i bakväggen ({lvpwd} mm). "
    elif ivsd > 0 and ivsd_status != "Normal":
        findings += f"{clean_hypertrofi_term(ivsd_status)} hypertrofi i septum ({ivsd} mm). "
    elif lvpwd > 0 and lvpwd_status != "Normal":
        findings += f"{clean_hypertrofi_term(lvpwd_status)} hypertrofi i bakväggen ({lvpwd} mm). "

    # --- Aorta ---
    if aorta > 0:
        if age > 0 and is_aorta_dilated(aorta, age, sex, bsa):
            findings += f"Dilaterad aorta ascendens ({aorta} mm). "
        else:
            findings += f"Normalvid aorta ascendens ({aorta} mm). "

    # --- Vänster förmak ---
    if lavi > 0:
        if lavi <= 34:
            findings += f"Normalstor vänster förmak (LAVI {lavi} ml/m²). "
        elif 35 <= lavi <= 41:
            findings += f"Lätt ökad vänster förmak storlek (LAVI {lavi} ml/m²). "
        elif 42 <= lavi <= 48:
            findings += f"Måttligt ökad vänster förmak storlek (LAVI {lavi} ml/m²). "
        else:
            findings += f"Uttalad ökad vänster förmak storlek (LAVI {lavi} ml/m²). "

    if ravi > 0:
        if sex == "Man":
            if ravi <= 36:
                findings += f"Normalstor höger förmak (RAVI {ravi} ml/m²). "
            elif 37 <= ravi <= 42:
                findings += f"Lätt ökad höger förmak storlek (RAVI {ravi} ml/m²). "
            elif 43 <= ravi <= 48:
                findings += f"Måttligt ökad höger förmak storlek (RAVI {ravi} ml/m²). "
            else:
                findings += f"Uttalat ökad höger förmak storlek (RAVI {ravi} ml/m²). "
        else:
            if ravi <= 31:
                findings += f"Normalstor höger förmak (RAVI {ravi} ml/m²). "
            elif 32 <= ravi <= 37:
                findings += f"Lätt ökad höger förmak storlek (RAVI {ravi} ml/m²). "
            elif 38 <= ravi <= 42:
                findings += f"Måttligt ökad höger förmak storlek (RAVI {ravi} ml/m²). "
            else:
                findings += f"Uttalat ökad höger förmak storlek (RAVI {ravi} ml/m²). "        

    # --- Vänsterkammarfunktion ---
    if ef > 0:
        if ef > 50:
            findings += f"Normal systolisk funktion med EF {ef}%. "
        elif 41 <= ef <= 50:
            findings += f"Lätt nedsatt systolisk funktion med EF {ef}%. "
        elif 30 <= ef <= 40:
            findings += f"Måttligt nedsatt systolisk funktion med EF {ef}%. "
        else:
            findings += f"Svår nedsatt systolisk funktion med EF {ef}%. "

    if -30.0 < gls < 0.0:
        findings += f"GLS {gls:.1f}%. "

    # --- Regionalitet (always showing default if not filled) ---
    findings += f"{regionalitet_findings} "

    # --- Slagvolym och SVI ---
    if stroke_volume > 0 and bsa > 0:
        if sex == "Man":
            if stroke_volume < 60:
                findings += f"Låg slagvolym ({stroke_volume} ml). "
            elif stroke_volume > 95:
                findings += f"Hög slagvolym ({stroke_volume} ml). "
            else:
                findings += f"Slagvolym inom normalintervall ({stroke_volume} ml). "
        else:
            if stroke_volume < 50:
                findings += f"Låg slagvolym ({stroke_volume} ml). "
            elif stroke_volume > 75:
                findings += f"Hög slagvolym ({stroke_volume} ml). "
            else:
                findings += f"Normala slagvolym ({stroke_volume} ml). "

        if svi > 0:
            if (sex == "Man" and svi < 34) or (sex == "Kvinna" and svi < 33):
                findings += f"SVI lågt ({svi} ml/m²). "
            elif (sex == "Man" and svi > 46) or (sex == "Kvinna" and svi > 45):
                findings += f"SVI högt ({svi} ml/m²). "
            else:
                findings += f"SVI inom normalintervall ({svi} ml/m²). "

    # --- Högerkammarfunktion ---
    if tapse > 0:
        if tapse >= 17:
            findings += f"Normal högerkammarfunktion TAPSE {tapse} mm. "
        else:
            findings += f"Tecken till nedsatt högerkammarfunktion TAPSE {tapse} mm. "

    # --- Diastolisk funktion ---
    if diastolic_function_text:
        findings += diastolic_function_text + " "
    # Klaffar
    if not aorta_pathology:
        if auto_detected_aorta_stenosis:
            findings += f"{aorta_morphology} aortaklaff med {auto_detected_aorta_stenosis.lower()} aortastenos. "
        else:
            findings += f"{aorta_morphology} aortaklaff utan stenos eller insufficiens. "
    elif "Stenos" in aorta_pathology and "Insufficiens" not in aorta_pathology:
        if aorta_stenosis_severity:
            findings += f"{aorta_morphology} aortaklaff med {aorta_stenosis_severity.lower()} aortastenos utan aortainsufficiens. "
    elif "Insufficiens" in aorta_pathology and "Stenos" not in aorta_pathology:
        findings += f"{aorta_morphology} aortaklaff utan aortastenos. "
        if aorta_insuff_severity:
            findings += f"{aorta_insuff_severity.capitalize()} aortainsufficiens. "
    elif "Stenos" in aorta_pathology and "Insufficiens" in aorta_pathology:
        findings += f"{aorta_morphology} aortaklaff med "
        if aorta_stenosis_severity:
            findings += f"{aorta_stenosis_severity.lower()} aortastenos"
            if aorta_insuff_severity:
                findings += f" och {aorta_insuff_severity.lower()} aortainsufficiens. "
            else:
                findings += ". "
        elif aorta_insuff_severity:
            findings += f"{aorta_insuff_severity.lower()} aortainsufficiens. "
    # Kompletterande aortastenos-parametrar
    if use_manual_aorta == "Avancerade parametrar":
        if ava_calc > 0:
            findings += f"Beräknad AVA enligt kontinuitetsekvationen {ava_calc} cm². "
        if avai > 0:
            findings += f"Indexerad AVA (AVAi) {avai} cm²/m². "
        if dvi > 0:
            findings += f"Dimensionless Index (DVI) {dvi}. "
        

    # Mitralisklaff
    if not mitral_pathology:
        findings += "Ingen mitralisinsufficiens eller mitralisstenos. "
    else:
        if "Stenos" in mitral_pathology and mitral_stenosis_severity:
            findings += f"{mitral_stenosis_severity.capitalize()} mitralisstenos. "
        elif "Stenos" not in mitral_pathology:
            findings += "Ingen mitralisstenos. "

        if "Insufficiens" in mitral_pathology and mitral_insuff_severity:
            findings += f"{mitral_insuff_severity.capitalize()} mitralisinsufficiens. "
        elif "Insufficiens" not in mitral_pathology:
            findings += "Ingen mitralisinsufficiens. "

    # Trikuspidalisklaff
    if ti_grade != "Ingen":
        findings += f"{ti_grade.capitalize()} trikuspidalisinsufficiens. "
    else:
        findings += "Ingen trikuspidalisinsufficiens. "

    # PA-tryck
    if tr_gradient_option == "Ej mätbar":
        findings += f"TI-gradient ej mätbar. CVT {cvp} mmHg. "
    elif pa_pressure is not None:
        if pa_pressure > 35:
            findings += f"Förhöjt PA-tryck ({pa_pressure:.0f} mmHg inkl. CVT {cvp} mmHg). "
        else:
            findings += f"Normalt PA-tryck ({pa_pressure:.0f} mmHg inkl. CVT {cvp} mmHg). "

    findings += "Ingen perikardvätska."

    # --- Sammanfattningstext ---
    summary_text = f"{patient_info}\n\n{findings}"

    components.html(f"""
    <div style="margin-top: 10px; display: flex; flex-direction: column; align-items: center;">
        <div style="width: 60%; min-width: 300px;">
            <textarea id="summaryText" style="
                width: 100%;
                font-size: 16px;
                font-family: system-ui, sans-serif;
                padding: 10px;
                border-radius: 6px;
                border: 1px solid #ccc;
                resize: none;
                overflow: hidden;
                min-height: 150px;
                box-shadow: none;
            " oninput="autoResize(this)">{summary_text}</textarea>
        </div>

        <button onclick="copyToClipboard()" style="
            margin-top: 12px;
            padding: 8px 16px;
            background-color: #003366;
            color: yellow;
            border: 2px solid #ccc;
            border-radius: 6px;
            font-size: 16px;
            font-weight: bold;
            white-space: nowrap;
        ">
            📋 Kopiera
        </button>

        <p id="copyStatus" style="margin-top: 6px; font-size: 14px; color: green;"></p>
    </div>

    <script>
    function copyToClipboard() {{
        var copyText = document.getElementById("summaryText");
        copyText.select();
        copyText.setSelectionRange(0, 99999);
        document.execCommand("copy");

        var status = document.getElementById("copyStatus");
        status.innerText = "Text kopierad till urklipp!";
    }}

    function autoResize(textarea) {{
        textarea.style.height = "auto";
        textarea.style.height = textarea.scrollHeight + "px";
    }}

    document.addEventListener("DOMContentLoaded", function() {{
        var ta = document.getElementById("summaryText");
        if (ta) autoResize(ta);
    }});
    </script>
    """, height=800)
