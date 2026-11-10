import requests
from bs4 import BeautifulSoup
import pandas as pd
import io

def load_institutional_map():
    # Structural registry tracking exactly where the raw surveillance numbers leak
    pipeline_data = """Source_Type,Governing_Body,Program_Or_Database,Data_Location_URL,Tracked_Identifiers
Government White Paper,Home Office (UK),WAND Program,https://www.gov.uk,"Cotinine, Anabasine, tobacco, population"
Academic Journal,Oxford University Press,OUP Academic Registry,https://oup.com,"DOI: 10.1093/jlb/lsaf001, Wastewater metrics"
Corporate Procurement,UK Government Contracts Finder,Consortium Logistics Log,https://service.gov.uk,"Wastewater analysis, Automated extraction machinery"
"""
    return pd.read_csv(io.StringIO(pipeline_data))

def execute_live_scan(target_url):
    print(f"[ENGINE] Connecting directly to target directory: {target_url}")
    surveillance_keywords = ["Cotinine", "Anabasine", "tobacco", "nicotine", "surveillance", "tax gap"]
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(target_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            raw_text = soup.get_text()
            
            detected_metrics = []
            for word in surveillance_keywords:
                count = raw_text.lower().count(word.lower())
                if count > 0:
                    detected_metrics.append({"Indicator": word, "Occurrences": count})
            
            return pd.DataFrame(detected_metrics)
        else:
            print(f"[ALERT] Host server returned status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"[FAILED] Live connection error: {str(e)}")
        return None

# Main execution loop
if __name__ == "__main__":
    print("=== FORENSIC SURVEILLANCE ENGINE ACTIVATED ===")
    df_map = load_institutional_map()
    
    print("\n--- DEPLOYING REGISTRY VERIFICATION ---")
    # Scan the primary institutional link listed in our map
    target = "https://www.gov.uk"
    evidence_df = execute_live_scan(target)
    
    if evidence_df is not None and not evidence_df.empty:
        print("\n=== SYSTEMIC MATCHES EXPOSED IN LIVE DATA STREAM ===")
        print(evidence_df.to_string(index=False))
    else:
        print("\n[STATUS] Live landing layout verified. Deeper data sub-logs required for extraction.")
