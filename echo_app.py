# --- Ekokardiografi App ---
import streamlit as st
import streamlit.components.v1 as components
from bs4 import BeautifulSoup
import os
import math

st.set_page_config(page_title="Ekokardiografi App", layout="wide")
st.title("Ekokardiografi")

# --- 🧝 Patientuppgifter ---
st.header("Patientuppgifter")
age = st.number_input("Ålder", min_value=0, max_value=120, step=1, format="%d")
weight = st.number_input("Vikt (kg)", min_value=0, step=1, format="%d")
height = st.number_input("Längd (cm)", min_value=0, step=1, format="%d")
sex = st.selectbox("Kön", ["Man", "Kvinna"])
bsa = round((height * weight / 3600) ** 0.5, 1) if height > 0 and weight > 0 else 0.0
st.text(f"BSA: {bsa:.1f} m²")

ekg_rytm = st.selectbox(
    "EKG-rytm",
    ["Sinusrytm", "Sinusbradykardi", "Förmaksflimmer", "Förmaksfladder", "Pacemakerrytm", "AV-block II", "AV-block III"]
)
ekg_freq = st.number_input("EKG-frekvens (bpm)", min_value=20, max_value=200, step=1, format="%d")

# --- 🕝 Dimensioner ---
st.header("Dimensioner")
lvdd = st.number_input("LVIDd (mm)", min_value=0, step=1, format="%d")
ivsd = st.number_input("IVSd (mm)", min_value=0, step=1, format="%d")
lvpwd = st.number_input("LVPWd (mm)", min_value=0, step=1, format="%d")
aorta = st.number_input("Aorta ascendens (mm)", min_value=0, step=1, format="%d")
lavi = st.number_input("LAVI (ml/m²)", min_value=0, step=1, format="%d")

# --- 🕝 Dimension Bedömning --- (Aligned with Equalis S022 v1.2)
lvdd_status = "Normal"
ivsd_status = "Normal"
lvpwd_status = "Normal"

if sex == "Man":
    # LVIDd thresholds (Equalis: normal ≤ 58 mm)
    if lvdd > 65:
        lvdd_status = "Kraftig dilaterad"
    elif lvdd > 61:
        lvdd_status = "Måttligt dilaterad"
    elif lvdd > 58:
        lvdd_status = "Lätt dilaterad"
    elif lvdd < 42:
        lvdd_status = "Mindre än normalt"
    else:
        lvdd_status = "Normal"

    # IVSd (Equalis/Norre: normal ≤ 12 mm)
    if ivsd > 16:
        ivsd_status = "Uttalad hypertrofi"
    elif ivsd >= 14:
        ivsd_status = "Måttlig hypertrofi"
    elif ivsd >= 13:
        ivsd_status = "Lindrig hypertrofi"
    else:
        ivsd_status = "Normal"

    # LVPWd (Equalis/Norre: normal ≤ 12 mm)
    if lvpwd > 16:
        lvpwd_status = "Uttalad hypertrofi"
    elif lvpwd >= 14:
        lvpwd_status = "Måttlig hypertrofi"
    elif lvpwd >= 13:
        lvpwd_status = "Lindrig hypertrofi"
    else:
        lvpwd_status = "Normal"

elif sex == "Kvinna":
    # LVIDd thresholds (Equalis: normal ≤ 52 mm)
    if lvdd > 59:
        lvdd_status = "Kraftig dilaterad"
    elif lvdd > 55:
        lvdd_status = "Måttligt dilaterad"
    elif lvdd > 52:
        lvdd_status = "Lätt dilaterad"
    elif lvdd < 38:
        lvdd_status = "Mindre än normalt"
    else:
        lvdd_status = "Normal"

    # IVSd (Equalis/Norre: normal ≤ 11 mm)
    if ivsd > 15:
        ivsd_status = "Uttalad hypertrofi"
    elif ivsd >= 13:
        ivsd_status = "Måttlig hypertrofi"
    elif ivsd >= 12:
        ivsd_status = "Lindrig hypertrofi"
    else:
        ivsd_status = "Normal"

    # LVPWd (Equalis/Norre: normal ≤ 11 mm)
    if lvpwd > 15:
        lvpwd_status = "Uttalad hypertrofi"
    elif lvpwd >= 13:
        lvpwd_status = "Måttlig hypertrofi"
    elif lvpwd >= 12:
        lvpwd_status = "Lindrig hypertrofi"
    else:
        lvpwd_status = "Normal"

# --- 💓 Systolisk Funktion ---
st.header("Systolisk Funktion")
ef = st.number_input("Ejektionsfraktion (EF %)", min_value=0, max_value=100, step=1, format="%d")
stroke_volume = st.number_input("Stroke Volume (ml)", min_value=0, step=1, format="%d")
svi = round(stroke_volume / bsa, 1) if stroke_volume > 0 and bsa > 0 else 0.0
tapse = st.number_input("TAPSE (mm)", min_value=0, max_value=40, step=1, format="%d")
gls = st.number_input("Global Longitudinal Strain (GLS %)", min_value=-30.0, max_value=0.0, step=0.1, format="%.1f")

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
st.header("Regionalitet")

if os.path.exists("coronary_segments.svg"):
    with open("coronary_segments.svg", "r", encoding="utf-8") as svg_file:
        svg_raw = svg_file.read()

    soup = BeautifulSoup(svg_raw, "html.parser")

    # --- Insert JavaScript and Logic from Code 17 ---
    script = """
<script>
let selectedSegments = [];
function updateSegmentListDisplay() {
    const listDiv = document.getElementById("segment_display");
    const segmentStatus = JSON.parse(localStorage.getItem("segmentStatus") || "{}");
    const uniqueBaseSegments = [...new Set(selectedSegments.map(s => s.replace(/_(A4C|A2C|PLAX|SAX)$/i, "")))];
    listDiv.innerHTML = uniqueBaseSegments.map(base => {
        const representative = selectedSegments.find(s => s.startsWith(base)) || base;
        return `
            <div style='margin-bottom: 10px;'>
                <label style='font-weight: bold;'>${base.replaceAll("_", " ")}:</label>
                <select onchange="updateStatus('${representative}', this.value)" style='background-color: #003366; color: white; border-radius: 6px; padding: 4px;'>
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
    const ladSegments = ["Apex_A4C", "Apical_septal_A4C", "Apex_A2C", "Apical_inferior_A2C", "Apical_anterior_A2C",
        "Mid_anterior_A2C", "Basal_anterior_A2C", "Apex_PLAX", "Apical_lateral_PLAX", "Apical_anterior_PLAX",
        "Mid_anteroseptal_PLAX", "Basal_anteroseptal_PLAX", "Basal_anterior_SAX", "Basal_anteroseptal_SAX",
        "Mid_anterior_SAX", "Mid_anteroseptal_SAX", "Apical_anterior_SAX", "Apical_septal_SAX"];

    const ladOrLcxSegments = ["Apical_lateral_A4C", "Apical_lateral_SAX", "Mid_anterolateral_SAX", "Basal_anterolateral_SAX",
        "Basal_anterolateral_A4C", "Mid_anterolateral_A4C"];

    const rcaSegments = ["Basal_inferoseptal_A4C", "Basal_inferoseptal_SAX", "Basal_inferior_SAX", "Basal_inferior_A2C",
        "Mid_inferior_A2C", "Mid_inferior_SAX"];

    const rcaOrLadSegments = ["Mid_inferoseptal_A4C", "Mid_inferoseptal_SAX", "Apical_inferior_SAX"];
    const rcaOrLcxSegments = ["Mid_inferolateral_PLAX", "Basal_inferolateral_PLAX", "Basal_inferolateral_SAX", "Mid_inferolateral_SAX"];

    const segmentStatus = JSON.parse(localStorage.getItem("segmentStatus") || "{}");
    const grouped = {};
    for (const [segment, status] of Object.entries(segmentStatus)) {
        if (!selectedSegments.includes(segment)) continue;
        if (status !== "Hypokinesi" && status !== "Akinesi") continue;
        const baseLabel = segment.replace(/_(A4C|A2C|PLAX|SAX)$/i, "");
        const label = baseLabel.replaceAll("_", " ");
        if (!grouped[status]) grouped[status] = [];
        if (!grouped[status].includes(label)) grouped[status].push(label);
    }

    let summary = Object.entries(grouped)
        .map(([status, segments]) => `<strong>${status}:</strong> ${segments.join(", ")}`)
        .join("<br>");
    const summaryDiv = document.getElementById("summary_display");

    if (!Object.values(segmentStatus).some((status, index) => {
        const id = selectedSegments[index];
        return selectedSegments.includes(id) && (status === "Hypokinesi" || status === "Akinesi");
    })) {
        summaryDiv.innerHTML = "";
        return;
    }

    let ladSelected = ladSegments.some(id => selectedSegments.includes(id) && (segmentStatus[id] === "Hypokinesi" || segmentStatus[id] === "Akinesi"));
    let ladOrLcxSelected = ladOrLcxSegments.some(id => selectedSegments.includes(id) && (segmentStatus[id] === "Hypokinesi" || segmentStatus[id] === "Akinesi"));
    let rcaSelected = rcaSegments.some(id => selectedSegments.includes(id) && (segmentStatus[id] === "Hypokinesi" || segmentStatus[id] === "Akinesi"));
    let rcaOrLadSelected = rcaOrLadSegments.some(id => selectedSegments.includes(id) && (segmentStatus[id] === "Hypokinesi" || segmentStatus[id] === "Akinesi"));
    let rcaOrLcxSelected = rcaOrLcxSegments.some(id => selectedSegments.includes(id) && (segmentStatus[id] === "Hypokinesi" || segmentStatus[id] === "Akinesi"));

    let alerts = [];
    if (ladSelected) alerts.push(`<span style='background-color:#f0f4f8;color:purple;padding:3px 6px;font-weight:bold;font-size: 18px;'>Misstänkt LAD skada</span>`);
    if (ladOrLcxSelected) alerts.push(`<span style='background-color:#f0f4f8;color:orange;padding:3px 6px;font-weight:bold;font-size: 18px;'>Misstänkt LAD eller LCx skada</span>`);
    if (rcaSelected) alerts.push(`<span style='background-color:#f0f4f8;color:red;padding:3px 6px;font-weight:bold;font-size: 18px;'>Misstänkt RCA skada</span>`);
    if (rcaOrLadSelected) alerts.push(`<span style='background-color:#f0f4f8;color:blue;padding:3px 6px;font-weight:bold;font-size: 18px;'>Misstänkt RCA eller LAD skada</span>`);
    if (rcaOrLcxSelected) alerts.push(`<span style='background-color:#f0f4f8;color:green;padding:3px 6px;font-weight:bold;font-size: 18px;'>Misstänkt RCA eller LCx skada</span>`);

    document.getElementById("summary_display").innerHTML = summary ? `<strong>REGIONALITET:</strong><br>${summary}` : "";
    document.getElementById("alert_display").innerHTML = alerts.join("<br>");
}

function toggleSegment(id) {
    const el = document.getElementById(id);
    if (!el) return;
    const baseName = id.replace(/_(A4C|A2C|PLAX|SAX)$/i, "");
    let allMatching = [id];
    if (["Apical_inferior_A2C", "Apical_inferior_SAX"].includes(id)) {
        allMatching = [id];
    } else if (id === "Apical_lateral_PLAX") {
        allMatching = ["Apical_lateral_PLAX"];
    } else if (["Apical_lateral_A4C", "Apical_lateral_SAX"].includes(id)) {
        allMatching = ["Apical_lateral_A4C", "Apical_lateral_SAX"];
    } else {
        allMatching = Array.from(document.querySelectorAll('[id]')).map(el => el.id).filter(s => s.replace(/_(A4C|A2C|PLAX|SAX)$/i, "") === baseName);
    }

    const allSelected = allMatching.every(s => selectedSegments.includes(s));
    if (allSelected) {
        selectedSegments = selectedSegments.filter(s => !allMatching.includes(s));
        allMatching.forEach(s => {
            const el = document.getElementById(s);
            if (el) {
                el.style.stroke = "#999";
                el.style.strokeWidth = "1";
            }
        });
    } else {
        allMatching.forEach(s => {
            if (!selectedSegments.includes(s)) selectedSegments.push(s);
            const el = document.getElementById(s);
            if (el) {
                el.style.stroke = "blue";
                el.style.strokeWidth = "3";
            }
        });
    }
    localStorage.setItem("selectedSegments", JSON.stringify(selectedSegments));
    updateSegmentListDisplay();
}

function resetSelections() {
    selectedSegments = [];
    localStorage.removeItem("selectedSegments");
    localStorage.removeItem("segmentStatus");
    document.querySelectorAll('[id]').forEach(el => {
        el.style.stroke = "#999";
        el.style.strokeWidth = "1";
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
            tag["id"] = seg_id

    modified_svg = str(soup)

    style_block = """
<style>
svg {
    width: 100vw;
    height: auto;
    max-height: 90vh;
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

/* Responsive adjustments for mobile */
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

<div id="segment_display" style="margin-top:20px; font-size:18px;"></div>

<div id="combined_display" style="margin-top: 20px; padding: 12px; border: 2px solid #003366; border-radius: 8px; background-color: #f0f4f8;">
    <div id="summary_display" style="font-size:20px; margin-bottom: 12px;"></div>
    <div id="alert_display" style="font-size:18px;"></div>
</div>

<div style="margin-top:20px;">
    <button onclick="resetSelections()" style="padding:8px 15px; font-size:18px; border:2px solid #ccc; border-radius:8px; background-color: #003366; color:yellow; font-weight:bold;">
        Återställ
    </button>
</div>
""",
    height=0,
    scrolling=False
)

# --- 💓 Diastolisk Funktion (bedömning av fyllnadstryck) ---
st.header("Diastolisk Funktion (bedömning av fyllnadstryck)")
with st.expander("**OBSERVANDUM!**", expanded=False):
    st.markdown("""

    * **LAVI** är ej bedömbart vid mer än lindrigt mitralisvitium och svårtolkat vid intermittent **förmaksflimmer**.

    * **E/e′** bör ej bedömas vid mer än lindrigt mitralisvitium, mitralisklaffprotes, riklig förkalkning i annulus mitralis, pacemakerrytm, LBBB, prekapillär pulmonell hypertension, uttalad tricuspidalisinsufficiens och konstriktiv perikardit.

    * **E/A-kvot** är svårbedömd vid sinusrytm hos patienter med intermittent **förmaksflimmer** samt vid sinustakykardi.

    * Vid **förmaksflimmer** saknas goda riktlinjer för bedömning av fyllnadstrycket.
    """)

cvp = st.selectbox("Centralvenöst tryck (CVT mmHg)", [5, 10, 15], key="cvp_dia")
tr_gradient_option = st.selectbox("TI-gradient tillgänglig?", ["Ej mätbar", "Ange värde"], key="tr_option_dia")
if tr_gradient_option == "Ange värde":
    tr_gradient = st.number_input("TI-gradient (mmHg)", min_value=0, step=1, format="%d", key="tr_value_dia")
    pa_pressure = round(tr_gradient + cvp, 1)
else:
    pa_pressure = None

e_wave = st.number_input("E-våg (m/s)", min_value=0.0, step=0.1, format="%.1f")
a_wave = st.number_input("A-våg (m/s)", min_value=0.0, step=0.1, format="%.1f")
e_prime_septal = st.number_input("e' septal (cm/s)", min_value=0, step=1, format="%d")
e_prime_lateral = st.number_input("e' lateral (cm/s)", min_value=0, step=1, format="%d")

# Optional parameters for extra analysis
pv_flow = st.selectbox("Pulmonell venflöde (S/D)", ["Ej angivet", "S > D", "S < D"])
pva_duration = st.number_input("PV-a duration (ms)", min_value=0, step=1)
a_dur = st.number_input("A-vågs duration (ms)", min_value=0, step=1)

# Derived values
e_a_ratio = round(e_wave / a_wave, 1) if a_wave > 0 else 0
e_wave_cm_s = e_wave * 100

# Mean e′
if e_prime_septal > 0 and e_prime_lateral > 0:
    e_prime_avg = round((e_prime_septal + e_prime_lateral) / 2, 1)
elif e_prime_septal > 0:
    e_prime_avg = e_prime_septal
elif e_prime_lateral > 0:
    e_prime_avg = e_prime_lateral
else:
    e_prime_avg = 0

e_e_prime = round(e_wave_cm_s / e_prime_avg, 1) if e_prime_avg > 0 else 0

# Age-adjusted high E/A thresholds
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
        assessable.append("LAVI")
        positive += 1
    else:
        assessable.append("LAVI")

    if pa_pressure:
        assessable.append("PA")
        if pa_pressure > 35:
            positive += 1

    if e_e_prime > 0:
        assessable.append("E/e′")
        if e_e_prime > 14:
            positive += 1

    if len(assessable) >= 3:
        if positive >= 2:
            diastolic_function_text = "Tecken till förhöjt fyllnadstryck."
        else:
            diastolic_function_text = "Normalt fyllnadstryck."
    elif len(assessable) == 2 and positive == 1:
        diastolic_function_text = "Fyllnadstryck kan ej bedömas."
    elif positive == len(assessable):
        diastolic_function_text = "Tecken till förhöjt fyllnadstryck."
    else:
        diastolic_function_text = "Normalt fyllnadstryck."

# Check if pulmonary vein or PV-a findings are positive
extra_positive = False
if (pv_flow == "S < D" and age > 50) or (pva_duration > 0 and a_dur > 0 and (pva_duration - a_dur) > 30):
    extra_positive = True

if diastolic_function_text == "Normalt fyllnadstryck." and extra_positive:
    diastolic_function_text = "Tecken till förhöjt fyllnadstryck."

if diastolic_function_text == "Normalt fyllnadstryck.":
    st.markdown("**Normalt fyllnadstryck**")
elif diastolic_function_text == "Tecken till förhöjt fyllnadstryck.":
    st.markdown("**Tecken till förhöjt fyllnadstryck**")
elif diastolic_function_text == "Fyllnadstryck kan ej bedömas.":
    st.markdown("**Fyllnadstryck kan ej bedömas**")

if diastolic_function_text != "":
    if e_a_ratio > 0 and (e_a_ratio > age_threshold_high or (e_a_ratio <= 0.8 and e_wave_cm_s <= 50)):
        e_a_text = f"**E/A: {e_a_ratio} (ålder {age})**"
    else:
        e_a_text = f"E/A: {e_a_ratio}"

    e_e_prime_text = f"**E/e′: {e_e_prime}**" if e_e_prime > 14 else f"E/e′: {e_e_prime}" if e_e_prime > 0 else "E/e′: Ej angivet"
    lavi_text = f"**LAVI: {lavi} ml/m²**" if lavi > 37 else f"LAVI: {lavi} ml/m²"
    pa_text = f"**PA-tryck: {pa_pressure:.0f} mmHg**" if pa_pressure is not None and pa_pressure > 35 else f"PA-tryck: {pa_pressure:.0f} mmHg" if pa_pressure is not None else "PA-tryck: Ej angivet"

    pv_text = ""
    if pv_flow == "S < D" and age > 50:
        pv_text = "**Pulmonell venflöde S < D hos patient >50 år**"

    pva_text = ""
    if pva_duration > 0 and a_dur > 0 and (pva_duration - a_dur) > 30:
        pva_text = f"**PV-a duration längre än A-vågs duration med {pva_duration - a_dur} ms**"

    st.markdown("**Parametrar:**")
    st.markdown(f"- {e_a_text}")
    st.markdown(f"- {e_e_prime_text}")
    st.markdown(f"- {lavi_text}")
    st.markdown(f"- {pa_text}")
    if pv_text:
        st.markdown(f"- {pv_text}")
    if pva_text:
        st.markdown(f"- {pva_text}")


# --- 🩺 Klaffunktion ---
st.header("Klaffunktion")

# --- AORTAKLAFF ---
st.subheader("Aortaklaff")
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
st.subheader("Mitralisklaff")
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
st.subheader("Trikuspidalisklaff")
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



# --- Sammanfattning ---
st.header("Sammanfattning")

patient_info = (
    f"Ålder: {age:.0f} år, "
    f"Vikt: {weight:.0f} kg, "
    f"Längd: {height:.0f} cm, "
    f"BSA: {bsa:.1f} m², "
    f"Rytm: {ekg_rytm.lower()} med frekvens {ekg_freq:.0f} /min."
)

findings = ""

# Kammarfunktion
if lvdd_status == "Normal":
    findings += "Normalstor vänsterkammare i diastole. "
else:
    findings += f"Vänsterkammare {lvdd_status.lower()} i diastole. "

if ivsd_status == "Normal" and lvpwd_status == "Normal":
    findings += "Ingen hypertrofi. "
else:
    if ivsd_status != "Normal":
        findings += f"Septum {ivsd_status.lower()} ({ivsd} mm). "
    if lvpwd_status != "Normal":
        findings += f"Bakvägg {lvpwd_status.lower()} ({lvpwd} mm). "

# Aorta
if age > 0 and is_aorta_dilated(aorta, age, sex, bsa):
    findings += f"Dilaterad aorta ascendens ({aorta} mm). "
else:
    findings += f"Normalvid aorta ascendens ({aorta} mm). "

# Vänster förmak
if lavi <= 34:
    findings += f"Normalstor vänster förmak (LAVI {lavi} ml/m²). "
elif 35 <= lavi <= 41:
    findings += f"Lätt ökad vänster förmak storlek (LAVI {lavi} ml/m²). "
elif 42 <= lavi <= 48:
    findings += f"Måttligt ökad vänster förmak storlek (LAVI {lavi} ml/m²). "
else:
    findings += f"Uttalad ökad vänster förmak storlek (LAVI {lavi} ml/m²). "

# Vänsterkammarfunktion
if ef > 50:
    findings += f"Normal systolisk funktion med EF {ef}%. "
elif 41 <= ef <= 50:
    findings += f"Lätt nedsatt systolisk funktion med EF {ef}%. "
elif 30 <= ef <= 40:
    findings += f"Måttligt nedsatt systolisk funktion med EF {ef}%. "
else:
    findings += f"Svår nedsatt systolisk funktion med EF {ef}%. "

# Lägg till GLS om det är angivet (dvs < 0)
if gls < 0:
    findings += f"GLS {gls:.1f}%. "
    
if stroke_volume > 0 and bsa > 0:
    if sex == "Man":
        if stroke_volume < 60:
            findings += f"Låg slagvolym ({stroke_volume} ml). "
        elif stroke_volume > 95:
            findings += f"Hög slagvolym ({stroke_volume} ml). "
        else:
            findings += f"Slagvolym inom normalintervall ({stroke_volume} ml). "

        if svi < 34:
            findings += f"SVI lågt ({svi} ml/m²). "
        elif svi > 46:
            findings += f"SVI högt ({svi} ml/m²). "
        else:
            findings += f"SVI inom normalintervall ({svi} ml/m²). "

    elif sex == "Kvinna":
        if stroke_volume < 50:
            findings += f"Låg slagvolym ({stroke_volume} ml). "
        elif stroke_volume > 75:
            findings += f"Hög slagvolym ({stroke_volume} ml). "
        else:
            findings += f"Normala slagvolym ({stroke_volume} ml). "

        if svi < 33:
            findings += f"SVI lågt ({svi} ml/m²). "
        elif svi > 45:
            findings += f"SVI högt ({svi} ml/m²). "
        else:
            findings += f"SVI inom normalintervall ({svi} ml/m²). "

# Högerkammare
if tapse > 16:
    findings += f"Normal högerkammarfunktion TAPSE {tapse} mm. "
    if tapse < 17:
        findings += "Tecken till nedsatt högerkammarfunktion. "

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

# PA-tryck bedömning (always include if possible)
if tr_gradient_option == "Ej mätbar":
    findings += f"TI-gradient ej mätbar. CVT {cvp} mmHg. "
elif pa_pressure is not None:
    pa_status = "förhöjt" if pa_pressure > 35 else "normalt"
    findings += f"PA-tryck är {pa_status} ({pa_pressure:.0f} mmHg inkl. CVT {cvp} mmHg). "
else:
    findings += "Ingen trikuspidalisinsufficiens. "

findings += "Ingen perikardvätska."

st.markdown(f"{patient_info}\n\n{findings}")
