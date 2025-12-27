Below is a **fully revised README.md** aligned with what MaintWatch has become now.
It removes anomaly language and reflects **component reliability, MTBF, and forecasting**.

You can **replace the current README.md completely** with this content.

---

MaintWatch
Aircraft Component Reliability and MTBF Tracking System

Purpose
MaintWatch is a focused aircraft maintenance reliability application designed to calculate, monitor, and analyze Mean Time Between Failures using component removal history.

The system is intentionally limited in scope.
It concentrates on component removals, not full maintenance logs, defects, or task cards.
This keeps reliability calculations clean, auditable, and aligned with standard engineering practice.

MaintWatch is built for operators, CAMO teams, and reliability engineers who need practical insight without the complexity of a full MRO system.

---

What MaintWatch does

• Records component removals in a structured and controlled way
• Separates scheduled and unscheduled events explicitly
• Calculates MTBF using repeated removals of the same serial number
• Aggregates reliability by component and ATA chapter
• Supports basic spares and planning forecasts
• Provides clean datasets for reliability review meetings

---

Core design principles

• Component master driven
• No free-text component entry
• Clear distinction between scheduled and unscheduled events
• Transparent MTBF calculation logic
• Simple CSV-based storage for auditability

---

Data model overview

1. Component master
   components.csv defines the approved component universe.

Each component has
• component_code
• component_name
• category
• criticality
• inspection_interval_days
• ata_chapter

All forms and calculations reference this file.
Invalid or unknown components are blocked at entry.

---

2. Component removal events
   removal_events.csv is the core operational dataset.

Each record represents a single component removal.

Key fields include
• aircraft_reg
• component_code
• component_name
• serial_number
• ata_chapter
• category
• criticality
• removal_date
• aircraft_fh
• aircraft_fc
• event_type
• removal_reason

event_type is mandatory and limited to
• Scheduled
• Unscheduled

Only Unscheduled events are used for MTBF.

---

3. Defect and deferred references
   defect_log.csv tracks open defects and MEL references.

This allows
• Linking removals to deferred defects
• Preserving traceability
• Keeping MTBF logic independent of defect workflows

Defects do not affect MTBF calculations directly.

---

MTBF calculation logic

MTBF is calculated using unscheduled removals only.

Rules applied
• event_type must be Unscheduled
• Same serial number must appear at least twice
• Aircraft flight hour deltas between removals are used
• First occurrence is excluded from MTBF math

Outputs include
• MTBF in flight hours
• MTBF in flight cycles
• Failure count per component

This approach aligns with standard reliability engineering methods.

---

MTBF Dashboard

The MTBF Dashboard provides

• Component-level MTBF ranking
• ATA-level aggregation
• Failure counts
• Visibility of critical components

The dashboard validates dataset structure before calculation and reports schema issues clearly.

---

Forecasting hook

MaintWatch includes a simple planning estimate.

Logic
Expected failures = Fleet hours / MTBF

Purpose
• Spares sizing
• Short-term planning
• Reliability discussion support

This is a planning aid, not a predictive maintenance model.

---

Folder structure

MaintWatch/
.streamlit/
config.toml

data/
components.csv
removal_events.csv
defect_log.csv

forms/
component_removal_form.py
defect_entry_form.py

pages/
Home.py
Component_Removal.py
MTBF_Dashboard.py
ATA_Summary.py
Pilots.py
Technicians.py

utils/
data_loader.py
mtbf_calculator.py
csv_writer.py

validation/
component_rules.py

requirements.txt
README.md

---

What MaintWatch is not

• Not an ERP
• Not a MEL system
• Not a defect rectification tracker
• Not a predictive analytics platform

It is a focused reliability analysis tool.

---

Intended users

• Maintenance planners
• CAMO engineers
• Reliability engineers
• Quality and safety teams
• Small to mid-size operators

---

Future enhancements

• MTBF trend charts over time
• Component family grouping
• Reliability alerts
• Improved forecasting models
• Export-ready review board outputs

---

If you want, next we can
• Harden MTBF logic further
• Improve dashboard visuals
• Prepare executive-level reports
• Package this as a reusable reliability toolkit
