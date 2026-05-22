from playwright.sync_api import sync_playwright 
import time
import random 
import csv 

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    
    all_products = []
    base_url = "https://www.daraz.pk/catalog/?_keyori=ss&from=search_history&q=laptop&page="
    
    for page_num in range(1, 6):
        page = browser.new_page()
        print(f"Opening Daraz website - Page {page_num}...")
        current_url = f"{base_url}{page_num}"
        page.goto(current_url)
        
        page.wait_for_selector(".Bm3ON")
        print("Extracting product information...")
        
        page.evaluate("window.scrollBy(0, 2000)")
        time.sleep(random.uniform(2, 6))
        products = page.query_selector_all(".Bm3ON")
        
        for product in products:
            title = product.query_selector(".RfADt").inner_text()
            price = product.query_selector(".ooOxS").inner_text()
            clean_price  = price.replace("PKR ", "").replace("Rs.", "").replace(",", "").strip()
            clean_price = float(clean_price)
            all_products.append((title, clean_price))
            print(f"Product: {title}, Price: {clean_price}")
            print("-" * 50)
            
    avg_price = sum(price for _, price in all_products) / len(all_products)
    print(f"Average Price after {len(all_products)} products: {avg_price:.2f}")
    print("-" * 50)
            
    threashold = avg_price * 0.8
    if clean_price < threashold:
        print(f"🔥 STEAL ALERT: '{title}' is only Rs. {clean_price}!")
        print(f"   (This is {round((1 - clean_price/avg_price)*100)}% below the market average)")
        print("-" * 50)
    else:
        print("No deals found")
        
    browser.close()
    
    with open("daraz_products.csv", "w", newline="", encoding="utf-8") as csvfiles: 
        w = csv.writer(csvfiles)
        w.writerow(["Title", "Price"])
        w.writerows(all_products)
            
if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
    
    
