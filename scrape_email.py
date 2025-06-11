import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time

# def get_email(cin,page):
#     page.goto(f"https://www.mastersindia.co/mca-company-detail/?cname=a/{cin}")
#     email_value = page.locator("//th[contains(text(),'Email Id')]/following-sibling::td").text_content()
#     print(email_value)

def get_email(cin, page):
    page.goto(f"https://www.mastersindia.co/mca-company-detail/?cname=a/{cin}")
    email_value = page.locator("//th[contains(text(),'Email Id')]/following-sibling::td").text_content()
    return email_value.strip() if email_value else "Not Found"

    
    
# def get_email(cin, page):
#     page.goto("https://www.mastersindia.co/mca-company-detail/")

#     page.wait_for_selector('input[placeholder="Search"]', timeout=15000)
   
#     page.fill('input[placeholder="Search"]', cin)
#     page.click('button:has-text("Search")')

  
#     page.wait_for_timeout(7000)

#     html = page.content()
#     soup = BeautifulSoup(html, 'html.parser')
#     email_elem = soup.find('a', href=lambda h: h and 'mailto:' in h)

#     return email_elem.text.strip() if email_elem else "Not Found"

def get_email_with_retry(cin, page, retries=3):
    for attempt in range(retries):
        try:
            print(f" Trying CIN: {cin} (Attempt {attempt+1})")
            return get_email(cin, page)
        except Exception as e:
            print(f" Error: {e}")
            time.sleep(2)
    return "Error"


def main():
    
    df = pd.read_excel("Incorporation-report-March (1).xlsx", sheet_name="Indian Companies", header=8)
    
    df.columns = df.columns.str.strip()

    df['Email'] = ""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for i, row in df.iterrows():
            cin = str(row['CIN']).strip()
            print(f"Processing CIN: {cin}")
            email = get_email_with_retry(cin, page)
            print(f"Found: {email}")
            df.at[i, 'Email'] = email

        browser.close()

    df.to_excel("output_with_emails.xlsx", index=False)
    print("All emails saved to output_with_emails.xlsx")

main()
