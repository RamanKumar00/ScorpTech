import pandas as pd
import time
from playwright.sync_api import sync_playwright
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

# Worker function to run in each process
def worker(cin):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            url = f"https://www.mastersindia.co/mca-company-detail/?cname=a/{cin}"
            page.goto(url, timeout=30000)
            page.wait_for_selector("th:has-text('Email Id') + td", timeout=15000)
            email = page.locator("th:has-text('Email Id') + td").text_content()
            print(f"Processing CIN: {cin} → Email: {email}")
            return (cin, email.strip() if email else "Not Found")
        except Exception as e:
            return (cin, "Error")
        finally:
            browser.close()

def main():
    # Load Excel
    df = pd.read_excel("Incorporation-report-March (1).xlsx", sheet_name="Indian Companies", header=8)
    df.columns = df.columns.str.strip()

    # Get CINs list
    cin_list = df["CIN"].astype(str).str.strip().tolist()

    print(f" Total CINs: {len(cin_list)}")
    print(f"Running on {min(cpu_count(), 8)} processes...\n")

    # Run in parallel
    with Pool(processes=min(cpu_count(), 8)) as pool:
        results = list(tqdm(pool.imap(worker, cin_list), total=len(cin_list)))

    # Add results back to DataFrame
    email_map = dict(results)
    df["Email"] = df["CIN"].astype(str).str.strip().map(email_map)

    # Save output
    df.to_excel("output_with_emails_parallel.xlsx", index=False)
    print("\n Emails saved to 'output_with_emails_parallel.xlsx'")

if __name__ == "__main__":
    main()
