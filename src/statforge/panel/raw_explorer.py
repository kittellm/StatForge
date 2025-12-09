import panel as pn
import pandas as pd
from statforge.etl.extract import statcan, boc
from datetime import datetime

pn.extension('tabulator')

# --- Helper Functions ---

def fetch_statcan_data(vectors_str):
    if not vectors_str:
        return pd.DataFrame(), "Please enter Vector IDs."
    
    vector_ids = [v.strip() for v in vectors_str.split(',') if v.strip()]
    if not vector_ids:
        return pd.DataFrame(), "No valid Vector IDs found."

    try:
        # Get Metadata
        meta = statcan.get_series_info(vector_ids)
        meta_df = pd.DataFrame(meta)
        
        # Get Data
        # Defaulting to last 5 years for quick inspection
        start_date = datetime(datetime.now().year - 5, 1, 1)
        raw_data = statcan.get_data_from_vectors(vector_ids, start_date=start_date)
        
        # StatCan returns nested 'vectorDataPoint' list inside each object
        # Let's flatten it for display
        all_points = []
        for series in raw_data:
            vec_id = series.get('vectorId')
            points = series.get('vectorDataPoint', [])
            for p in points:
                p['vectorId'] = vec_id
                all_points.append(p)
        
        data_df = pd.DataFrame(all_points)
        return meta_df, data_df
        
    except Exception as e:
        return pd.DataFrame(), pd.DataFrame(), f"Error: {str(e)}"

def fetch_boc_data(series_name):
    if not series_name:
        return pd.DataFrame(), "Please enter a Series Name."
    
    try:
        # Get Data
        # Default to last 5 years
        start_date = f"{datetime.now().year - 5}-01-01"
        data = boc.get_series_observations(series_name, start_date=start_date)
        
        obs = data.get('observations', [])
        data_df = pd.DataFrame(obs)
        
        # Get Metadata (if available separately, BoC returns it in the same structure often)
        # But let's call the details endpoint just to see what it gives
        details = boc.get_series_details(series_name)
        series_info = details.get('series', {})
        meta_df = pd.DataFrame([series_info]).T # Transpose for easier reading if single row
        
        return meta_df, data_df

    except Exception as e:
        return pd.DataFrame(), pd.DataFrame(), f"Error: {str(e)}"


# --- UI Components ---

# StatCan Tab
statcan_input = pn.widgets.TextInput(name='Vector IDs (comma separated)', placeholder='v41690973, v41690914')
statcan_btn = pn.widgets.Button(name='Fetch StatCan', button_type='primary')
statcan_status = pn.pane.Markdown("")
statcan_meta_table = pn.widgets.Tabulator(pagination='remote', page_size=10, name="Metadata")
statcan_data_table = pn.widgets.Tabulator(pagination='remote', page_size=20, name="Data Points")

def update_statcan(event):
    statcan_status.object = "Fetching..."
    meta, data = fetch_statcan_data(statcan_input.value)
    
    if isinstance(data, str): # Error message
         statcan_status.object = data
         statcan_meta_table.value = pd.DataFrame()
         statcan_data_table.value = pd.DataFrame()
    else:
        statcan_status.object = "Success!"
        statcan_meta_table.value = meta
        statcan_data_table.value = data

statcan_btn.on_click(update_statcan)

# BoC Tab
boc_input = pn.widgets.TextInput(name='Series Name', placeholder='FXUSDCAD')
boc_btn = pn.widgets.Button(name='Fetch BoC', button_type='primary')
boc_status = pn.pane.Markdown("")
boc_meta_table = pn.widgets.Tabulator(pagination='remote', page_size=10, name="Metadata")
boc_data_table = pn.widgets.Tabulator(pagination='remote', page_size=20, name="Observations")

def update_boc(event):
    boc_status.object = "Fetching..."
    meta, data = fetch_boc_data(boc_input.value)
    
    if isinstance(data, str): # Error
         boc_status.object = data
         boc_meta_table.value = pd.DataFrame()
         boc_data_table.value = pd.DataFrame()
    else:
        boc_status.object = "Success!"
        boc_meta_table.value = meta
        boc_data_table.value = data

boc_btn.on_click(update_boc)

# Layout
statcan_view = pn.Column(
    "### Statistics Canada WDS",
    "Enter Vector IDs (e.g., `v41690973` for CPI) to inspect raw API response.",
    pn.Row(statcan_input, statcan_btn),
    statcan_status,
    "#### Metadata",
    statcan_meta_table,
    "#### Data Points (Last 5 Years)",
    statcan_data_table
)

boc_view = pn.Column(
    "### Bank of Canada Valet",
    "Enter Series Name (e.g., `FXUSDCAD`) to inspect raw API response.",
    pn.Row(boc_input, boc_btn),
    boc_status,
    "#### Metadata",
    boc_meta_table,
    "#### Observations (Last 5 Years)",
    boc_data_table
)

explorer_tabs = pn.Tabs(
    ('StatsCan', statcan_view),
    ('Bank of Canada', boc_view)
)

def explorer_app():
    return pn.template.FastListTemplate(
        title="StatForge Data Inspector",
        main=[explorer_tabs]
    )

if __name__.startswith("bokeh"):
    explorer_app().servable()
elif __name__ == "__main__":
    explorer_app().show()
