import streamlit as st
import pandas as pd
import altair as alt
import random

custom_css = """
<style>
    .stApp {
        background-color: #0f172a;
        color: white;
    }

    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: white !important;
    }

    [data-testid="stMetric"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
    }

    [data-testid="stInfo"] {
        background-color: #1e293b;
        border-radius: 12px;
        padding: 10px;
    }

    [data-testid="stSuccess"] {
        border-radius: 12px;
    }

    [data-testid="stError"] {
        border-radius: 12px;
    }

    [data-testid="stWarning"] {
        border-radius: 12px;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    hr {
        border: 1px solid #334155;
    }
</style>
"""

st.set_page_config(page_title="SupplyShock Arena", layout="wide")
st.markdown(custom_css, unsafe_allow_html=True)


# ---------- Helper UI functions ----------

def kpi_card(title, value, color):
    st.markdown(
        f"""
        <div style="
            background-color: #1e293b;
            padding: 20px;
            border-radius: 12px;
            border-left: 8px solid {color};
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            text-align: center;
            margin-bottom: 10px;
        ">
            <div style="
                font-size: 18px;
                color: white;
                margin-bottom: 10px;
                font-weight: 600;
            ">
                {title}
            </div>
            <div style="
                font-size: 32px;
                color: {color};
                font-weight: bold;
            ">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_box(title, content):
    st.markdown(
        f"""
        <div style="
            background-color: #1e293b;
            padding: 20px;
            border-radius: 16px;
            border: 1px solid #334155;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            margin-bottom: 10px;
        ">
            <div style="
                font-size: 22px;
                font-weight: 700;
                color: white;
                margin-bottom: 12px;
            ">
                {title}
            </div>
            <div style="
                font-size: 16px;
                color: #cbd5e1;
                line-height: 1.6;
            ">
                {content}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def scenario_box(title, scenario):
    st.markdown(f"### {title}")
    st.info("Input Settings")
    st.write(f"**Demand:** {scenario['Demand']}")
    st.write(f"**Fuel Cost:** {scenario['Fuel Cost']}")
    st.write(f"**Supplier Reliability:** {scenario['Supplier Reliability']}")
    st.write(f"**Warehouse Capacity:** {scenario['Warehouse Capacity']}")
    st.write(f"**Staff Availability:** {scenario['Staff Availability']}")

    st.success("Output Results")
    st.write(f"**Delay Risk:** {scenario['Delay Risk']}%")
    st.write(f"**Cost Impact:** {scenario['Cost Impact']}%")
    st.write(f"**Throughput:** {scenario['Throughput']}%")
    st.write(f"**System Stress:** {scenario['System Stress']}%")
    st.write(f"**Score:** {scenario['Score']}/100")
    st.write(f"**Disruption:** {scenario['Disruption']}")


# ---------- App title ----------

st.title("🎮 SupplyShock Arena")
st.write("A real-time operations simulation for testing supply chain performance under pressure.")

st.markdown("---")


# ---------- Mission + locked disruption ----------

event_options = [
    "None",
    "Supplier Failure (-20 reliability)",
    "Demand Surge (+30 demand)",
    "Fuel Price Spike (+25 fuel)"
]

if "event" not in st.session_state:
    st.session_state["event"] = random.choice(event_options)

event = st.session_state["event"]

m1, m2 = st.columns([1, 1])

with m1:
    section_box(
        "🎯 Mission",
        "Goal: Keep Delay Risk below 40, maintain Demand above 60, and finish with a Score above 70."
    )

with m2:
    section_box(
        "⚡ Current Disruption",
        f"Event: {event}"
    )

    if st.button("🔄 Generate New Event"):
        st.session_state["event"] = random.choice(event_options)
        st.rerun()

st.markdown("---")


# ---------- Controls ----------

st.subheader("🎛️ Control Panel")
st.caption("Adjust the system inputs to manage operational pressure and complete the mission.")

left_col, right_col = st.columns(2)

with left_col:
    st.markdown("### 📦 Demand & Supply")
    st.caption("Set market pressure and supplier stability.")

    demand = st.slider("Demand", 0, 100, 50)
    st.caption("Higher demand increases pressure on the system.")

    supplier = st.slider("Supplier Reliability", 0, 100, 70)
    st.caption("Lower reliability increases operational risk.")

with right_col:
    st.markdown("### 🏭 Operations & Resources")
    st.caption("Control available capacity and execution strength.")

    fuel = st.slider("Fuel Cost", 0, 100, 30)
    st.caption("Higher fuel cost increases transportation pressure.")

    capacity = st.slider("Warehouse Capacity", 0, 100, 60)
    st.caption("Lower capacity creates bottlenecks.")

    staff = st.slider("Staff Availability", 0, 100, 80)
    st.caption("Lower staffing reduces throughput.")


# ---------- Apply disruption effects ----------

effective_demand = demand
effective_supplier = supplier
effective_fuel = fuel

if "Supplier Failure" in event:
    effective_supplier = max(supplier - 20, 0)

if "Demand Surge" in event:
    effective_demand = min(demand + 30, 100)

if "Fuel Price Spike" in event:
    effective_fuel = min(fuel + 25, 100)


# ---------- Calculations ----------

delay_risk = int((effective_demand * 0.4) + ((100 - effective_supplier) * 0.3) + ((100 - capacity) * 0.3))
cost_impact = int((effective_fuel * 0.5) + (effective_demand * 0.2))
throughput = int((capacity * 0.5) + (staff * 0.5) - (effective_demand * 0.3))
system_stress = int((delay_risk + cost_impact) / 2)

score = 100 - (delay_risk * 0.5 + cost_impact * 0.3 + (100 - throughput) * 0.2)
score = max(0, int(score))


# ---------- Scenario comparison ----------

st.markdown("---")
st.subheader("📌 Scenario Comparison")
st.caption("Preview the current setup, then save two fresh scenarios and compare them.")

if st.button("🗑️ Start New Comparison"):
    if "scenario_a" in st.session_state:
        del st.session_state["scenario_a"]
    if "scenario_b" in st.session_state:
        del st.session_state["scenario_b"]
    if "preview_scenario" in st.session_state:
        del st.session_state["preview_scenario"]
    if "show_preview" in st.session_state:
        st.session_state["show_preview"] = False
    st.success("Comparison reset. Save new Scenario A and Scenario B.")

current_scenario = {
    "Demand": demand,
    "Fuel Cost": fuel,
    "Supplier Reliability": supplier,
    "Warehouse Capacity": capacity,
    "Staff Availability": staff,
    "Delay Risk": delay_risk,
    "Cost Impact": cost_impact,
    "Throughput": throughput,
    "System Stress": system_stress,
    "Score": score,
    "Disruption": event
}

if "show_preview" not in st.session_state:
    st.session_state["show_preview"] = False

preview_button_text = "Hide Preview" if st.session_state["show_preview"] else "Preview Current Scenario"

if st.button(preview_button_text):
    st.session_state["show_preview"] = not st.session_state["show_preview"]

if st.session_state["show_preview"]:
    st.session_state["preview_scenario"] = current_scenario
    preview = st.session_state["preview_scenario"]

    st.markdown("### 👀 Current Scenario Preview")

    preview_df = pd.DataFrame({
        "Metric": list(preview.keys()),
        "Value": list(preview.values())
    })

    st.dataframe(preview_df, use_container_width=True)

    save_col1, save_col2, save_col3 = st.columns(3)

    with save_col1:
        if st.button("Save as Scenario A"):
            st.session_state["scenario_a"] = preview.copy()
            st.success("Scenario A saved.")

    with save_col2:
        if st.button("Save as Scenario B"):
            st.session_state["scenario_b"] = preview.copy()
            st.success("Scenario B saved.")

    with save_col3:
        csv = preview_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Scenario CSV",
            data=csv,
            file_name="scenario_preview.csv",
            mime="text/csv"
        )

if "scenario_a" in st.session_state or "scenario_b" in st.session_state:
    st.markdown("### ⚔️ Saved Scenarios")

    box1, box2 = st.columns(2)

    with box1:
        if "scenario_a" in st.session_state:
            scenario_box("1️⃣ First Comparison", st.session_state["scenario_a"])
        else:
            section_box("1️⃣ First Comparison", "No scenario saved yet.")

    with box2:
        if "scenario_b" in st.session_state:
            scenario_box("2️⃣ Second Comparison", st.session_state["scenario_b"])
        else:
            section_box("2️⃣ Second Comparison", "No scenario saved yet.")

    if "scenario_a" in st.session_state and "scenario_b" in st.session_state:
        a = st.session_state["scenario_a"]
        b = st.session_state["scenario_b"]

        score_a = a["Score"] + a["Throughput"] - a["Delay Risk"] - a["Cost Impact"]
        score_b = b["Score"] + b["Throughput"] - b["Delay Risk"] - b["Cost Impact"]

        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

        if score_a > score_b:
            st.success("🏆 Winner: First Comparison performs better overall.")
        elif score_b > score_a:
            st.success("🏆 Winner: Second Comparison performs better overall.")
        else:
            st.info("🤝 Result: First Comparison and Second Comparison are evenly matched.")


# ---------- KPIs ----------

delay_color = "#22c55e" if delay_risk < 40 else "#ef4444"
cost_color = "#22c55e" if cost_impact < 40 else "#ef4444"
throughput_color = "#22c55e" if throughput > 60 else "#ef4444"
stress_color = "#22c55e" if system_stress < 40 else "#ef4444"

st.markdown("---")
st.subheader("📊 System Performance")

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card("Delay Risk", f"{delay_risk}%", delay_color)

with c2:
    kpi_card("Cost Impact", f"{cost_impact}%", cost_color)

with c3:
    kpi_card("Throughput", f"{throughput}%", throughput_color)

with c4:
    kpi_card("System Stress", f"{system_stress}%", stress_color)


# ---------- Score + checklist ----------

st.markdown("---")

condition_1 = delay_risk < 40
condition_2 = effective_demand > 60
condition_3 = score > 70

s1, s2 = st.columns([1, 1])

with s1:
    st.subheader("🏆 Operational Score")
    score_color = "#22c55e" if score > 70 else "#ef4444"

    st.markdown(
        f"""
        <div style="
            background-color: #1e293b;
            padding: 30px;
            border-radius: 16px;
            border: 1px solid #334155;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        ">
            <div style="
                font-size: 18px;
                color: #cbd5e1;
                margin-bottom: 12px;
                font-weight: 600;
            ">
                Current Score
            </div>
            <div style="
                font-size: 48px;
                color: {score_color};
                font-weight: 800;
            ">
                {score}/100
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with s2:
    st.subheader("✅ Mission Checklist")
    st.markdown(f"- Delay Risk < 40 {'✅' if condition_1 else '❌'}")
    st.markdown(f"- Demand > 60 {'✅' if condition_2 else '❌'}")
    st.markdown(f"- Score > 70 {'✅' if condition_3 else '❌'}")

st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

if condition_1 and condition_2 and condition_3:
    st.success("🎉 Mission Success! System stability maintained under pressure.")
else:
    st.error("🚨 Mission Failed. The system is still under operational stress.")


# ---------- Analysis ----------

st.markdown("---")
st.subheader("🧠 Operational Analysis")

if effective_demand > 70 and capacity < 50:
    st.warning("High demand and low warehouse capacity are creating a serious bottleneck.")
elif effective_supplier < 50:
    st.warning("Supplier reliability is low. This may cause unstable operations and delays.")
elif effective_fuel > 70:
    st.warning("Fuel costs are high, which is likely increasing transportation pressure.")
else:
    st.success("The system is currently stable.")


# ---------- Chart ----------

st.markdown("---")
st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
st.subheader("📈 Resource Balance")

chart_data = pd.DataFrame({
    "Category": ["Demand", "Warehouse Capacity", "Staff Availability"],
    "Value": [effective_demand, capacity, staff]
})

chart = alt.Chart(chart_data).mark_bar(
    color="#a86bb8",
    cornerRadiusTopLeft=8,
    cornerRadiusTopRight=8
).encode(
    x=alt.X(
        "Category",
        sort=None,
        axis=alt.Axis(labelAngle=0, title=None, labelColor="white")
    ),
    y=alt.Y(
        "Value",
        axis=alt.Axis(title="Value", labelColor="white", titleColor="white")
    )
).properties(
    width=700,
    height=400
).configure_view(
    strokeWidth=0
).configure_axis(
    gridColor="#334155"
)

st.altair_chart(chart, use_container_width=True)