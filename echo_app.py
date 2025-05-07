# --- Ekokardiografi App ---
import streamlit as st
import streamlit.components.v1 as components
from bs4 import BeautifulSoup
import os
import math

st.set_page_config(page_title="Ekokardiografi App", layout="wide")

tabs = st.tabs(["Patient", "Dimensioner", "Systolisk funktion", "Regionalitet", "Diastolisk funktion", "Klaffar", "Sammanfattning"])
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


    # Input: Age and weight in first column pair
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Ålder", min_value=0, max_value=120, step=1, format="%d")
    with col2:
        weight = st.number_input("Vikt (kg)", min_value=0, step=1, format="%d")

    # Input: Height and sex in second column pair
    col3, col4 = st.columns(2)
    with col3:
        height = st.number_input("Längd (cm)", min_value=0, step=1, format="%d")
    with col4:
        sex = st.selectbox("Kön", ["Man", "Kvinna"])

    # BSA calculation
    bsa = round((height * weight / 3600) ** 0.5, 1) if height > 0 and weight > 0 else 0.0
    st.markdown(f"**BSA:** {bsa:.1f} m²")

    st.markdown("---")

    st.subheader("EKG")

    # Input: EKG-rytm and frequency side by side
    col5, col6 = st.columns(2)
    with col5:
        ekg_rytm = st.selectbox(
            "EKG-rytm",
            ["Sinusrytm", "Sinusbradykardi", "Förmaksflimmer", "Förmaksfladder",
             "Pacemakerrytm", "AV-block II", "AV-block III"]
        )
    with col6:
        ekg_freq = st.number_input("EKG-frekvens (bpm)", min_value=20, max_value=200, step=1, format="%d")


# --- 🕝 Dimensioner ---
with tabs[1]:


    # Input: LVIDd, IVSd, LVPWd
    col1, col2, col3 = st.columns(3)
    with col1:
        lvdd = st.number_input("LVIDd (mm)", min_value=0, step=1, format="%d")
    with col2:
        ivsd = st.number_input("IVSd (mm)", min_value=0, step=1, format="%d")
    with col3:
        lvpwd = st.number_input("LVPWd (mm)", min_value=0, step=1, format="%d")

    # Input: Aorta and LAVI side-by-side
    col4, col5 = st.columns(2)
    with col4:
        aorta = st.number_input("Aorta ascendens (mm)", min_value=0, step=1, format="%d")
    with col5:
        lavi = st.number_input("LAVI (ml/m²)", min_value=0, step=1, format="%d")

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
    if lavi <= 34:
        lavi_status = "Normal"
    elif 35 <= lavi <= 41:
        lavi_status = "Lätt ökad"
    elif 42 <= lavi <= 48:
        lavi_status = "Måttligt ökad"
    else:
        lavi_status = "Uttalad ökad"

    # --- Tolkning ---
    st.markdown("---")
    st.markdown("### Tolkning:")
    st.markdown(f"- **LVDD-status:** {lvdd_status}")
    st.markdown(f"- **IVSd-status:** {ivsd_status}")
    st.markdown(f"- **LVPWd-status:** {lvpwd_status}")
    st.markdown(f"- **LAVI-status:** {lavi_status} ({lavi} ml/m²)")


# --- 💓 Systolisk Funktion ---
with tabs[2]:


    # Input fields
    col1, col2 = st.columns(2)
    with col1:
        ef = st.number_input("Ejektionsfraktion (EF %)", min_value=0, max_value=100, step=1, format="%d")
    with col2:
        stroke_volume = st.number_input("Slagvolym (ml)", min_value=0, step=1, format="%d")

    col3, col4 = st.columns(2)
    with col3:
        tapse = st.number_input("TAPSE (mm)", min_value=0, max_value=40, step=1, format="%d")
    with col4:
        gls = st.number_input("Global Longitudinal Strain (GLS %)", min_value=-30.0, max_value=0.0, step=0.1, format="%.1f")

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

        # Inject JavaScript
        script = """
<script>
let selectedSegments = [];

function updateSegmentListDisplay() {
    const listDiv = document.getElementById("segment_display");
    const segmentStatus = JSON.parse(localStorage.getItem("segmentStatus") || "{}");
    const uniqueBaseSegments = [...new Set(selectedSegments.map(s => s.replace(/_(A4C|A2C|PLAX|SAX)$/i, "")))];

    listDiv.innerHTML = uniqueBaseSegments.map(base => {
        const rep = selectedSegments.find(s => s.startsWith(base)) || base;
        return `
            <div style='margin-bottom: 10px;'>
                <label style='font-weight: bold;'>${base.replaceAll("_", " ")}:</label>
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
    const lad = ["Apex_A4C", "Apical_septal_A4C", "Apex_A2C", "Apical_inferior_A2C", "Apical_anterior_A2C", "Mid_anterior_A2C", "Basal_anterior_A2C", "Apex_PLAX", "Apical_lateral_PLAX", "Apical_anterior_PLAX", "Mid_anteroseptal_PLAX", "Basal_anteroseptal_PLAX", "Basal_anterior_SAX", "Basal_anteroseptal_SAX", "Mid_anterior_SAX", "Mid_anteroseptal_SAX", "Apical_anterior_SAX", "Apical_septal_SAX"];
    const lad_lcx = ["Apical_lateral_A4C", "Apical_lateral_SAX", "Mid_anterolateral_SAX", "Basal_anterolateral_SAX", "Basal_anterolateral_A4C", "Mid_anterolateral_A4C"];
    const rca = ["Basal_inferoseptal_A4C", "Basal_inferoseptal_SAX", "Basal_inferior_SAX", "Basal_inferior_A2C", "Mid_inferior_A2C", "Mid_inferior_SAX"];
    const rca_lad = ["Mid_inferoseptal_A4C", "Mid_inferoseptal_SAX", "Apical_inferior_SAX"];
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
    const has = (arr) => arr.some(id => selectedSegments.includes(id) && ["Hypokinesi", "Akinesi"].includes(segStat[id]));
    if (has(lad)) alerts.push(`<span style='background-color:#f0f4f8;color:purple;padding:3px 6px;font-weight:bold;font-size:18px;'>Misstänkt LAD skada</span>`);
    if (has(lad_lcx)) alerts.push(`<span style='background-color:#f0f4f8;color:orange;padding:3px 6px;font-weight:bold;font-size:18px;'>Misstänkt LAD eller LCx skada</span>`);
    if (has(rca)) alerts.push(`<span style='background-color:#f0f4f8;color:red;padding:3px 6px;font-weight:bold;font-size:18px;'>Misstänkt RCA skada</span>`);
    if (has(rca_lad)) alerts.push(`<span style='background-color:#f0f4f8;color:blue;padding:3px 6px;font-weight:bold;font-size:18px;'>Misstänkt RCA eller LAD skada</span>`);
    if (has(rca_lcx)) alerts.push(`<span style='background-color:#f0f4f8;color:green;padding:3px 6px;font-weight:bold;font-size:18px;'>Misstänkt RCA eller LCx skada</span>`);

    document.getElementById("alert_display").innerHTML = alerts.join("<br>");
}

function toggleSegment(id) {
    const base = id.replace(/_(A4C|A2C|PLAX|SAX)$/i, "");
    const matches = Array.from(document.querySelectorAll('[id]')).map(el => el.id).filter(s => s.replace(/_(A4C|A2C|PLAX|SAX)$/i, "") === base);
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

           # Update each segment with interactivity
        for tag in soup.find_all(["path", "polygon", "rect", "ellipse"]):
            if tag.has_attr("id"):
                seg_id = tag["id"]
                tag["onclick"] = f"toggleSegment('{seg_id}')"
                tag["id"] = seg_id

        modified_svg = str(soup)

        # CSS Styles
        style_block = """
<style>
svg {
    width: 100vw;
    height: auto;
    max-height: 70vh; /* reduced from 90vh for better space below */
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

/* 📱 Responsive layout for small screens */
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

        # Inject full HTML into Streamlit
        components.html(
            style_block + script + modified_svg + """
<script>
window.addEventListener('DOMContentLoaded', function() {
    const height = window.innerWidth <= 768 ? 1000 : 1900;
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

<!-- Segment Status Controls -->
<div id="segment_display" style="margin-top:20px; font-size:18px;"></div>

<!-- Summary & Alert Display -->
<div id="combined_display" style="
    margin: 20px auto 40px auto;
    padding: 12px 20px;
    border: 2px solid #003366;
    border-radius: 12px;
    background-color: #f0f4f8;
    max-width: 600px;
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
        tr_gradient = st.number_input("TI-gradient (mmHg)", min_value=0, step=1, format="%d", key="tr_value_dia")
        pa_pressure = round(tr_gradient + cvp, 1)
    else:
        pa_pressure = None

    col3, col4 = st.columns(2)
    with col3:
        e_wave = st.number_input("E-våg (m/s)", min_value=0.0, step=0.1, format="%.1f")
        e_prime_septal = st.number_input("e′ septal (cm/s)", min_value=0, step=1, format="%d")
    with col4:
        a_wave = st.number_input("A-våg (m/s)", min_value=0.0, step=0.1, format="%.1f")
        e_prime_lateral = st.number_input("e′ lateral (cm/s)", min_value=0, step=1, format="%d")

    col5, col6 = st.columns(2)
    with col5:
        pv_flow = st.selectbox("Pulmonell venflöde (S/D)", ["Ej angivet", "S > D", "S < D"])
    with col6:
        pva_duration = st.number_input("PV-a duration (ms)", min_value=0, step=1)

    a_dur = st.number_input("A-vågs duration (ms)", min_value=0, step=1)

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
        e_prime_avg = 0

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

# --- 🩺 Klaffunktion ---
with tabs[5]:


    # --- AORTAKLAFF ---
    st.markdown("### Aortaklaff")
    aorta_morphology = st.selectbox("Aortaklaff morfologi", ["Trikuspid", "Bikuspid"])
    use_manual_aorta = st.radio("Bedömning av aortaklaff", ["Manuell bedömning", "Avancerade parametrar"], horizontal=True)

    aorta_pathology = []
    aorta_stenosis_severity = None
    aorta_insuff_severity = None

    if use_manual_aorta == "Manuell bedömning":
        aorta_pathology = st.multiselect("Aortaklaff patologi", ["Stenos", "Insufficiens"])
        if "Stenos" in aorta_pathology:
            aorta_stenosis_severity = st.selectbox("Grad av aortastenos", ["Lindrig", "Måttlig", "Uttalad"])
        if "Insufficiens" in aorta_pathology:
            aorta_insuff_severity = st.selectbox("Grad av aortainsufficiens", ["Lindrig", "Måttlig", "Uttalad"])
    else:
        with st.expander("Avancerade parametrar – aortaklaff"):
            aortic_vmax = st.number_input("Maxhastighet (m/s)", min_value=0.0, step=0.1, format="%.1f")
            mean_pg = st.number_input("Medelgradient (mmHg)", min_value=0, step=1, format="%d")
            ava = st.number_input("Aortaklaffarea (cm²)", min_value=0.0, step=0.1, format="%.1f")
            vena_contracta_ai = st.number_input("Vena Contracta AI (cm)", min_value=0.0, step=0.1, format="%.1f")
            pht_ai = st.number_input("Pressure Half-Time AI (ms)", min_value=0, step=1, format="%d")
            diastolic_flow_reversal = st.selectbox("Diastoliskt backflöde i aorta descendens", ["Nej", "Ja"])

        if aortic_vmax > 2.6 or ava < 1.5:
            aorta_pathology.append("Stenos")
            if aortic_vmax > 4.0 or mean_pg > 40 or ava < 1.0:
                aorta_stenosis_severity = "Uttalad"
            elif 3.0 <= aortic_vmax <= 4.0 or 20 <= mean_pg <= 40 or 1.0 <= ava < 1.5:
                aorta_stenosis_severity = "Måttlig"
            else:
                aorta_stenosis_severity = "Lindrig"

        if vena_contracta_ai > 0.3 or pht_ai < 250 or diastolic_flow_reversal == "Ja":
            aorta_pathology.append("Insufficiens")
            if vena_contracta_ai >= 0.6 or pht_ai < 200:
                aorta_insuff_severity = "Uttalad"
            elif 0.4 <= vena_contracta_ai < 0.6 or 200 <= pht_ai < 250:
                aorta_insuff_severity = "Måttlig"
            else:
                aorta_insuff_severity = "Lindrig"

    # --- MITRALISKLAFF ---
    st.markdown("### Mitralisklaff")
    use_manual_mitral = st.radio("Bedömning av mitralisklaff", ["Manuell bedömning", "Avancerade parametrar"], horizontal=True)

    mitral_pathology = []
    mitral_stenosis_severity = None
    mitral_insuff_severity = None

    if use_manual_mitral == "Manuell bedömning":
        mitral_pathology = st.multiselect("Mitralisklaff patologi", ["Stenos", "Insufficiens"])
        if "Stenos" in mitral_pathology:
            mitral_stenosis_severity = st.selectbox("Grad av mitralisstenos", ["Lindrig", "Måttlig", "Uttalad"])
        if "Insufficiens" in mitral_pathology:
            mitral_insuff_severity = st.selectbox("Grad av mitralisinsufficiens", ["Lindrig", "Måttlig", "Uttalad"])
    else:
        with st.expander("Avancerade parametrar – mitralisklaff"):
            mva = st.number_input("Mitralisarea (cm²)", min_value=0.0, step=0.1, format="%.1f")
            vena_contracta_mr = st.number_input("Vena Contracta MR (cm)", min_value=0.0, step=0.1, format="%.1f")

        if mva < 1.5:
            mitral_pathology.append("Stenos")
            mitral_stenosis_severity = "Uttalad" if mva < 1.0 else "Måttlig"

        if vena_contracta_mr > 0.3:
            mitral_pathology.append("Insufficiens")
            if vena_contracta_mr >= 0.7:
                mitral_insuff_severity = "Uttalad"
            elif 0.4 <= vena_contracta_mr < 0.7:
                mitral_insuff_severity = "Måttlig"
            else:
                mitral_insuff_severity = "Lindrig"

    # --- TRIKUSPIDALISKLAFF ---
    st.markdown("### Trikuspidalisklaff")
    use_manual_tricuspid = st.radio("Bedömning av trikuspidalisklaff", ["Manuell bedömning", "Avancerade parametrar"], horizontal=True)

    vena_contracta_tr = 0.0
    ti_grade = "Ingen"

    if use_manual_tricuspid == "Manuell bedömning":
        ti_grade = st.selectbox("Grad av trikuspidalinsufficiens (manuell)", ["Ingen", "Lindrig", "Måttlig", "Uttalad"])
    else:
        with st.expander("Avancerade parametrar – trikuspidalisklaff"):
            vena_contracta_tr = st.number_input("Vena Contracta TR (cm)", min_value=0.0, step=0.1, format="%.1f")

        if vena_contracta_tr >= 0.7:
            ti_grade = "Uttalad"
        elif 0.4 <= vena_contracta_tr < 0.7:
            ti_grade = "Måttlig"
        elif 0.1 <= vena_contracta_tr < 0.4:
            ti_grade = "Lindrig"
        else:
            ti_grade = "Ingen"

# --- 📋 Sammanfattning ---
with tabs[6]:
    st.markdown("<h2 style='text-align: center;'>Sammanfattning</h2>", unsafe_allow_html=True)

    patient_info = (
        f"\u00c5lder: {age:.0f} \u00e5r, "
        f"Vikt: {weight:.0f} kg, "
        f"L\u00e4ngd: {height:.0f} cm, "
        f"BSA: {bsa:.1f} m², "
        f"Rytm: {ekg_rytm.lower()} med frekvens {ekg_freq:.0f} /min."
    )

    findings = ""

    # Kammarfunktion
    if lvdd_status == "Normal":
        findings += "Normalstor v\u00e4nsterkammare i diastole. "
    else:
        if "dilaterad" in lvdd_status.lower():
            findings += f"{lvdd_status.capitalize()} v\u00e4nsterkammare i diastole. "
        else:
            findings += f"{lvdd_status.capitalize()} dilaterad v\u00e4nsterkammare i diastole. "

    # Hypertrofi
    def clean_hypertrofi_term(status: str) -> str:
        return status.replace("hypertrofi", "").strip().capitalize()

    if ivsd_status == "Normal" and lvpwd_status == "Normal":
        findings += f"Ingen hypertrofi (septum {ivsd} mm, bakv\u00e4gg {lvpwd} mm). "
    else:
        if ivsd_status != "Normal":
            cleaned_ivsd = clean_hypertrofi_term(ivsd_status)
            findings += f"{cleaned_ivsd} hypertrofi i septum ({ivsd} mm). "
        if lvpwd_status != "Normal":
            cleaned_lvpwd = clean_hypertrofi_term(lvpwd_status)
            findings += f"{cleaned_lvpwd} hypertrofi i bakv\u00e4ggen ({lvpwd} mm). "

    # Aorta
    if age > 0 and is_aorta_dilated(aorta, age, sex, bsa):
        findings += f"Dilaterad aorta ascendens ({aorta} mm). "
    else:
        findings += f"Normalvid aorta ascendens ({aorta} mm). "

    # V\u00e4nster f\u00f6rmak
    if lavi <= 34:
        findings += f"Normalstor v\u00e4nster f\u00f6rmak (LAVI {lavi} ml/m\u00b2). "
    elif 35 <= lavi <= 41:
        findings += f"L\u00e4tt \u00f6kad v\u00e4nster f\u00f6rmak storlek (LAVI {lavi} ml/m\u00b2). "
    elif 42 <= lavi <= 48:
        findings += f"M\u00e5ttligt \u00f6kad v\u00e4nster f\u00f6rmak storlek (LAVI {lavi} ml/m\u00b2). "
    else:
        findings += f"Uttalad \u00f6kad v\u00e4nster f\u00f6rmak storlek (LAVI {lavi} ml/m\u00b2). "

    # V\u00e4nsterkammarfunktion
    if ef > 50:
        findings += f"Normal systolisk funktion med EF {ef}%. "
    elif 41 <= ef <= 50:
        findings += f"L\u00e4tt nedsatt systolisk funktion med EF {ef}%. "
    elif 30 <= ef <= 40:
        findings += f"M\u00e5ttligt nedsatt systolisk funktion med EF {ef}%. "
    else:
        findings += f"Sv\u00e5r nedsatt systolisk funktion med EF {ef}%. "

    if gls < 0:
        findings += f"GLS {gls:.1f}%. "

    if stroke_volume > 0 and bsa > 0:
        if sex == "Man":
            if stroke_volume < 60:
                findings += f"L\u00e5g slagvolym ({stroke_volume} ml). "
            elif stroke_volume > 95:
                findings += f"H\u00f6g slagvolym ({stroke_volume} ml). "
            else:
                findings += f"Slagvolym inom normalintervall ({stroke_volume} ml). "

            if svi < 34:
                findings += f"SVI l\u00e5gt ({svi} ml/m\u00b2). "
            elif svi > 46:
                findings += f"SVI h\u00f6gt ({svi} ml/m\u00b2). "
            else:
                findings += f"SVI inom normalintervall ({svi} ml/m\u00b2). "

        elif sex == "Kvinna":
            if stroke_volume < 50:
                findings += f"L\u00e5g slagvolym ({stroke_volume} ml). "
            elif stroke_volume > 75:
                findings += f"H\u00f6g slagvolym ({stroke_volume} ml). "
            else:
                findings += f"Normala slagvolym ({stroke_volume} ml). "

            if svi < 33:
                findings += f"SVI l\u00e5gt ({svi} ml/m\u00b2). "
            elif svi > 45:
                findings += f"SVI h\u00f6gt ({svi} ml/m\u00b2). "
            else:
                findings += f"SVI inom normalintervall ({svi} ml/m\u00b2). "

    # H\u00f6gerkammare
    if tapse > 16:
        findings += f"Normal h\u00f6gerkammarfunktion TAPSE {tapse} mm. "
        if tapse < 17:
            findings += "Tecken till nedsatt h\u00f6gerkammarfunktion. "

    # Diastolisk fyllnadstryck
    if diastolic_function_text:
        findings += diastolic_function_text + " "

    # Klaffar
    if not aorta_pathology:
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

    # Mitralisklaff
    if not mitral_pathology:
        findings += "Ingen mitralisinsufficiens eller mitralisstenos. "
    else:
        if "Stenos" in mitral_pathology and mitral_stenosis_severity:
            findings += f"{mitral_stenosis_severity.capitalize()} mitralisstenos. "
        if "Insufficiens" in mitral_pathology and mitral_insuff_severity:
            findings += f"{mitral_insuff_severity.capitalize()} mitralisinsufficiens. "

    # Trikuspidalisklaff
    if ti_grade != "Ingen":
        findings += f"{ti_grade.capitalize()} trikuspidalisinsufficiens. "
    else:
        findings += "Ingen trikuspidalisinsufficiens. "

    # PA-tryck bedömning
    if tr_gradient_option == "Ej mätbar":
        findings += f"TI-gradient ej mätbar. CVT {cvp} mmHg. "
    elif pa_pressure is not None:
        if pa_pressure > 35:
            findings += f"Förhöjt PA-tryck ({pa_pressure:.0f} mmHg inkl. CVT {cvp} mmHg). "
        else:
            findings += f"Normalt PA-tryck ({pa_pressure:.0f} mmHg inkl. CVT {cvp} mmHg). "
    else:
        findings += "Ingen trikuspidalisinsufficiens. "

    findings += "Ingen perikardvätska."

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

<style>
/* 📱 Increase textbox height on mobile */
@media (max-width: 768px) {{
    #summaryText {{
        min-height: 225px !important;
    }}
}}
</style>

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
""", height=470)

