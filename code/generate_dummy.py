#!/usr/bin/env python3
import csv
import random
from pathlib import Path

OUTPUT_FILE = Path("data/dummy_families.csv")
NUM_ROWS = 2000
SEED = None  #Change to 42 if you want the same output every time

COLUMNS = [
        "Family ID",
        "Street Address",
        "ZIP Code",
        "County",
        "Caregiver Highest Education",
        "Household Size",
        "Children Under 18",
        "Annual Household Income ($)",
        "WIC / TANF",
        "Military Service",
        "School District",
        "Program Enrollment",
        "Events Attended",
]

TX_LOCATIONS = [
        {
            "city": "San Antonio",
            "county": "Bexar",
            "zips": ["78201", "78207", "78244", "78249", "78254", "78255", "78258"],
            "districts": ["San Antonio ISD", "Northside ISD", "North East ISD", "Other"],
        },
        {
            "city": "Austin",
            "county": "Travis",
            "zips": ["78727", "78652", "78745", "78748", "78758"],
            "districts": ["Austin ISD", "Pflugerville ISD", "Other"],
        },
        {
            "city": "Los Fresnos",
            "county": "Cameron",
            "zips": ["78566"],
            "districts": ["Los Fresnos CISD", "Other"],
        },
        {
            "city": "Schulenburg",
            "county": "Fayette",
            "zips": ["78956"],
            "districts": ["Schulenburg ISD", "Other"],
        },
]

STREET_NAMES = [
        "Lake Concordia",
        "Alameda Trace Circle",
        "Winding Shelf",
        "Brady Blvd",
        "Alametos",
        "Sonoma Ridge",
        "Apricot Bloom",
        "Babcock Road",
        "Kessler Ave",
        "Mission Trail",
        "Cypress Hollow",
        "Bluebonnet Ridge",
        "Pecan Valley",
        "Stone Creek",
        "Cedar Grove",
        "Oak Meadow",
        "Willow Bend",
        "Sunset Pass",
        "Heritage Way",
        "River Terrace",
]

APT_PREFIXES = ["Apt", "Unit", "#"]

EDUCATION_LEVELS = [
        "Less than high school",
        "High school diploma or GED",
        "Some college, no degree",
        "Associate degree",
        "Bachelor's (4-year) degree",
        "Master's degree",
        "Doctorate or other professional degree",
]

PROGRAMS = [
        "Coffee & Connections",
        "DDA",
        "Caregiver Support Group",
        "Expedited",
        "Camp AUsome!",
        "Parent Training",
        "Resource Navigation",
]


def unique_family_id(existing_ids):
        while True:
            family_id = str(random.randint(8_000_000_000, 19_999_999_999))
            if family_id not in existing_ids:
                existing_ids.add(family_id)
            return family_id


def make_address(location):
        number = random.randint(100, 12999)
        street = random.choice(STREET_NAMES)

        apt = ""
        if random.random() < 0.18:
            apt = f" {random.choice(APT_PREFIXES)} {random.randint(100, 999)}"

        zip_code = random.choice(location["zips"])
        city = location["city"]

        address = f"{number} {street}{apt}, {city}, TX {zip_code}, USA"
        return address, zip_code


def make_program_enrollment():
        programs = ["Coffee & Connections"]

        if random.random() < 0.35:
            programs.append(random.choice([p for p in PROGRAMS if p != "Coffee & Connections"]))

        if random.random() < 0.15:
            extra = random.choice([p for p in PROGRAMS if p not in programs])
            programs.append(extra)

        return ", ".join(programs)


def make_income(education, household_size):
        ranges = {
            "Less than high school": (0, 45000),
            "High school diploma or GED": (18000, 65000),
            "Some college, no degree": (22000, 80000),
            "Associate degree": (30000, 95000),
            "Bachelor's (4-year) degree": (35000, 150000),
            "Master's degree": (45000, 190000),
            "Doctorate or other professional degree": (70000, 350000),
        }

        low, high = ranges.get(education, (20000, 100000))
        high += household_size * random.randint(1500, 5000)

        if random.random() < 0.03:
            return 0

        return random.randrange(low, high + 1, 500)


def yes_no(prob_yes):
        return "Yes" if random.random() < prob_yes else "No"


def generate_rows(n):
        rows = []
        used_ids = set()

        for _ in range(n):
            location = random.choice(TX_LOCATIONS)
            address, zip_code = make_address(location)

            education = random.choice(EDUCATION_LEVELS)

            household_size = random.randint(1, 7)
            children_under_18 = random.randint(0, max(0, household_size - 1))

            income = make_income(education, household_size)

            if income == 0:
                wic_tanf = yes_no(0.45)
            elif income < 35000:
                wic_tanf = yes_no(0.35)
            elif income < 65000:
                wic_tanf = yes_no(0.18)
            else:
                wic_tanf = yes_no(0.04)

            military_service = yes_no(0.08)
            school_district = random.choice(location["districts"])
            program_enrollment = make_program_enrollment()

            program_count = len(program_enrollment.split(", "))

            if program_count == 1:
                events_attended = random.choices(
                    [1, 2, 3, 4, 5, 6, 7, 8, 9],
                    weights=[35, 18, 14, 9, 7, 5, 4, 3, 2],
                    k=1,
                )[0]
            else:
                events_attended = random.choices(
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    weights=[10, 10, 15, 15, 12, 10, 8, 6, 5, 4, 3, 2],
                    k=1,
                )[0]

            row = {
                "Family ID": unique_family_id(used_ids),
                "Street Address": address,
                "ZIP Code": zip_code,
                "County": location["county"],
                "Caregiver Highest Education": education,
                "Household Size": household_size,
                "Children Under 18": children_under_18,
                "Annual Household Income ($)": income,
                "WIC / TANF": wic_tanf,
                "Military Service": military_service,
                "School District": school_district,
                "Program Enrollment": program_enrollment,
                "Events Attended": events_attended,
            }

            rows.append(row)
        return rows


def write_csv(rows, output_file):
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(rows)


def main():
        if SEED is not None:
            random.seed(SEED)

        rows = generate_rows(NUM_ROWS)
        write_csv(rows, OUTPUT_FILE)

        print(f"Generated {NUM_ROWS} rows in {OUTPUT_FILE}")


if __name__ == "__main__":
        main()
