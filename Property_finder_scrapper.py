import requests
import time
import pandas as pd
import re

def Get_Build_Number():
    init_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    home_html = requests.get("https://www.propertyfinder.eg/en/search?c=1&l=1&ob=mr&page=1", headers=init_headers).text
    build_id = re.search(r'"buildId":\s*"(.*?)"', home_html).group(1)
    return build_id

def scraper_code(build_id):
    url = f"https://www.propertyfinder.eg/search/_next/data/{build_id}/en/buy/properties-for-sale.html.json"
    items =[]
    session = requests.Session()
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
        "x-nextjs-data": "1"
    }
    session.headers.update(headers)
    
    for x in range (1 ,11):
        print(f"fetching page {x}...")
        time.sleep(1)
        querystring = {"page":x,"cq_cmp":"18709477384","cq_con":"139697790461","cq_term":"property finder egypt","cq_med":"","cq_plac":"","cq_net":"g","cq_plt":"gp","gad_source":"1","gad_campaignid":"18709477384","categorySlug":"buy","propertyTypeSlug":"properties","saleType":"for-sale","pattern":"/categorySlug/propertyTypeSlug-saleType.html"}
        payload = ""
        try:
            r = session.get(url, data=payload, params=querystring)
            r.raise_for_status()
            print (f"{r.status_code} OK" )
            data = r.json()

        except requests.exceptions.HTTPError as http_err:
            print(f"[!] HTTP error on page {x}: {http_err}")
            break  # Stop the loop if the URL/Build ID is dead
                
        except requests.exceptions.JSONDecodeError:
            print(f"[!] Page {x} did not return JSON. Returned raw HTML/Protection page instead.")
            continue  # Skip to the next page
                
        except requests.exceptions.RequestException as req_err:
            print(f"[!] Network error on page {x}: {req_err}")
            continue
        listings = data.get("pageProps" ,{}).get("searchResult" , {}).get("listings" , {})
        for p in listings:
            if p.get("listing_type") == "property" and "property" in p:
                prop = p["property"]
                propertyID = prop.get("id")
                propertyType = prop.get("property_type")
                title = prop.get("title")
                price = prop.get("price" ,{}).get("value")
                location = prop.get("location", {}).get("coordinates" , {})
                lat = location.get("lat")
                lon = location.get("lon")
                location = f"{lat}, {lon}" if lat and lon else None
                bedrooms = prop.get("bedrooms")
                bathrooms = prop.get("bathrooms")
                size =prop.get("size" , {}).get("value")
                volume = str(size)
                try:
                    price_per_sqm = round(price / size) if size and price else None
                except ZeroDivisionError:
                    price_per_sqm = None
                person_name = prop.get("broker" , {})
                contact = prop.get("contact_options" , {})
                address = person_name.get("address")
                email = person_name.get("email")
                whatsapp = None
                for option in contact:
                    if option.get("type") == "whatsapp":
                        whatsapp = option.get("value")
                        break 
                phone_num = person_name.get("phone")
                amenities_list = prop.get("amenity_names" ,{})
                amenities = ", ".join(amenities_list) if isinstance(amenities_list, list) else ""
                completion = prop.get("completion_status" , {})
                furnished = prop.get("furnished")
                payment_method_list = prop.get("payment_method" , [])
                payment_method = ", ".join(payment_method_list) if isinstance(payment_method_list, list) else ""
                items.append({
                        "Property ID" : propertyID,
                        "Property Type" : propertyType,
                        "Title" : title,
                        "NO.Bedrooms" : bedrooms,
                        "NO.Bathrooms" : bathrooms,
                        "Amenities" : amenities,
                        "Size SQM" : volume,
                        "Price Per SQM (EGP)" :price_per_sqm,
                        "Furnished" : furnished,
                        "Location" : location,
                        "Price (EGP)" : price,
                        "Payment Method" : payment_method,
                        "Seller address" : address,
                        "Seller email" : email,
                        "Seller phone Number" : phone_num,
                        "Seller whatsapp" : whatsapp,
                        "Bulding Complition" : completion
                    
                    })
    return(items)

def ListTo_CSV_EXCEL(items):
    df = pd.DataFrame(items)
    df.to_csv("Property_finder.csv", index=False , encoding='utf-8-sig')
    print(f"Successfully scraped {len(items)} properties!")

def main():
    build_number = Get_Build_Number()
    items = scraper_code(build_number)
    ListTo_CSV_EXCEL(items)

if __name__ == "__main__":
    main()