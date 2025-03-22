import json
import os


def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def calculate_score(supplier):
    """Calculate a ranking score based on certifications, industries, processes, and other fields."""
    score = 0

    if supplier.get("certifications") and supplier["certifications"] != ["Unknown"]:
        score += len(supplier["certifications"]) * 5  # Certifications are important

    if supplier.get("industries_served") and supplier["industries_served"] != ["Unknown"]:
        score += len(supplier["industries_served"])  # More industries mean versatility

    if supplier.get("manufacturing_processes") and supplier["manufacturing_processes"] != ["Unknown"]:
        score += len(supplier["manufacturing_processes"])  # More processes indicate better capability

    if supplier.get("customers") and supplier["customers"] != ["Unknown"]:
        score += len(supplier["customers"])  # More known customers add credibility

    if supplier.get("annual_revenue") and supplier["annual_revenue"] != "Unknown":
        score += 10  # Revenue is a strong indicator of company success

    if supplier.get("employees") and supplier["employees"] != "Unknown":
        score += 3  # More employees might indicate a bigger company

    if supplier.get("price") and supplier["price"] != "Unknown":
        try:
            prices = [float(p.replace("$", "").replace(",", "").strip()) for p in supplier["price"].split("-") if
                      p.strip()]
            avg_price = sum(prices) / len(prices)
            score += max(10 - avg_price / 100, 1)  # Lower price is better
        except:
            pass

    return score


def standardize_supplier_data(suppliers):
    """Standardize supplier data by unifying field names and handling missing values."""
    standardized_data = []

    for supplier in suppliers:
        standardized_supplier = {
            "company_name": supplier.get("Company Name") or supplier.get("company") or supplier.get("name", "Unknown"),
            "website": supplier.get("Website") or supplier.get("website", "Unknown"),
            "country": supplier.get("Country") or supplier.get("country", "Unknown"),
            "industries_served": supplier.get("Industries Served") or supplier.get("industries", []),
            "manufacturing_processes": supplier.get("Manufacturing Processes") or supplier.get("processes", []),
            "certifications": supplier.get("Certifications") or supplier.get("certifications", []),
            "customers": supplier.get("Customers") or supplier.get("customers", []),
            "employees": supplier.get("Metadata", {}).get("# Employees") or supplier.get("employees", "Unknown"),
            "annual_revenue": supplier.get("Metadata", {}).get("Annual Revenue") or supplier.get("revenue", "Unknown"),
            "price": supplier.get("price", "Unknown")
        }
        standardized_supplier["score"] = calculate_score(standardized_supplier)
        standardized_data.append(standardized_supplier)

    return standardized_data


def save_json(data, output_path):
    """Save standardized data to a JSON file."""
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def main():
    input_files = ["alibaba_suppliers.json", "trade_india_suppliers.json", "mfg_suppliers.json", "indiamart_suppliers.json"]
    all_suppliers = []

    for file in input_files:
        if os.path.exists(file):
            data = load_json(file)
            standardized_data = standardize_supplier_data(data)
            all_suppliers.extend(standardized_data)

    # Rank suppliers based on score
    ranked_suppliers = sorted(all_suppliers, key=lambda x: x["score"], reverse=True)

    # Print ranked suppliers
    print("\nRanked Suppliers:\n")
    for idx, supplier in enumerate(ranked_suppliers, 1):
        print(f"{idx}. {supplier['company_name']} - Score: {supplier['score']} website: {supplier['website']}")

    output_file = "output.json"
    save_json(ranked_suppliers, output_file)
    print(f"\nCleaned and ranked data saved to {output_file}")


if __name__ == "__main__":
    main()
