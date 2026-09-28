# PropertyFinder Egypt Scraper

A Python script to scrape property listings (apartments, villas, etc.) for sale on PropertyFinder Egypt. 

### How it works
PropertyFinder is a Next.js site. Instead of parsing heavy HTML, this script grabs the current dynamic `buildId` from the homepage using regex, then queries their hidden Next.js JSON data endpoints (`/_next/data/...`). This is much faster and less prone to breaking when layout classes change.

### Data Collected
- Property ID, Type, Title, Location (Lat/Lon)
- Price & Price per SQM
- Bedrooms, Bathrooms, SQM Area
- Seller contact details (Phone, Email, WhatsApp)
- Furnished status, Amenities, Payment options

### Requirements
```bash
pip install requests pandas
```
### Running the script
```bash
python Property_finder_scrapper.py
```

### Output
The script will output a CSV file with the scraped data.