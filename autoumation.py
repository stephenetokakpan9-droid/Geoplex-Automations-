import pandas as pd
import requests

# --------------------
# CONFIG
# --------------------
CLICKUP_API_KEY = "your_clickup_api_key_here"  # Replace with your API key
LIST_ID = "your_clickup_list_id_here"          # Replace with your ClickUp list ID
EXCEL_FILE = "rfq_data.xlsx"                   # Replace with your Excel filename

headers = {
    "Authorization": CLICKUP_API_KEY,
    "Content-Type": "application/json"
}

# --------------------
# LOAD EXCEL
# --------------------
df = pd.read_excel(EXCEL_FILE)

# Example: Mapping Excel column → ClickUp custom field ID
# You can get field IDs using ClickUp API (GET /list/{list_id}/field)
FIELD_MAPPING = {
    "RFQ Number": "custom_field_id_1",
    "Item Description": "custom_field_id_2",
    "RFQ Received Date": "custom_field_id_3",
    "Geoplex Mark Up Quote Sent Date": "custom_field_id_4",
    "Requested Vendor(s)": "custom_field_id_5",
    "Chosen Vendor": "custom_field_id_6",
    "Purchaser": "custom_field_id_7",
    "PO Number": "custom_field_id_8",
    "Ordered Date": "custom_field_id_9",
    "Vendor’s Delivery Date": "custom_field_id_10",
    "Order Status": "custom_field_id_11",
    "Geoplex Actions": "custom_field_id_12",
    "Action Party": "custom_field_id_13",
    "Yinson Comments": "custom_field_id_14",
    "Geoplex Comments": "custom_field_id_15"
}

# --------------------
# UPLOAD TO CLICKUP
# --------------------
for _, row in df.iterrows():
    task_payload = {
        "name": f"RFQ {row['RFQ Number']} - {row['Item Description']}",
        "description": f"Imported from Excel\n\nPO: {row['PO Number']}",
        "custom_fields": []
    }

    # Map custom fields
    for col, field_id in FIELD_MAPPING.items():
        if pd.notna(row[col]):  # Skip blanks
            task_payload["custom_fields"].append({
                "id": field_id,
                "value": str(row[col])
            })

    # Create Task
    url = f"https://api.clickup.com/api/v2/list/{LIST_ID}/task"
    r = requests.post(url, headers=headers, json=task_payload)

    if r.status_code == 200:
        print(f"✅ Task created for RFQ {row['RFQ Number']}")
    else:
        print(f"❌ Error creating task for RFQ {row['RFQ Number']}: {r.text}")
