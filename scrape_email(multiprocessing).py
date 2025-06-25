import pandas as pd
import time
from playwright.sync_api import sync_playwright
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import os



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
            
    # pid = os.getpid()
    # print(f"Process {pid} → Working on: {cin}")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
                  
    
    
def main():
    # exccel file se data load karai ga aur extra space ko hatayai ga 
    df = pd.read_excel("incorporation-report-March (1).xlsx", sheet_name="Indian Companies", header=8)
    df.columns = df.columns.str.strip()  
    
    
   # yai cin number ko extract krai ga  yadi duplicate hai toh remove kr dega or isko python list mai convert kr dega 
    cin_list = df["CIN"].dropna().unique().tolist()
    print(f"Total CINs to process: {len(cin_list)}")
    

   # yai multiple process ko parallel run krai ga aur imap har cin kai liye worker function ko call krai ga
    with Pool(processes=cpu_count()) as pool:
        results = list(tqdm(pool.imap(worker, cin_list), total=len(cin_list)))

    #   results ko  DataFrame mai convert krai ga
    results_df = pd.DataFrame(results, columns=["CIN", "Email"])

    #  Save to Excel
    results_df.to_excel("email_results.xlsx", index=False)
    print("All CINs processed. Results saved to 'email_results.xlsx'.")
if __name__ == "__main__":
     main()


 // app.post("/company/cin",async(req, res)=> {
    const cin = req.params.cin;
    const url = 'jo bhi url hai '
    if 
 })    