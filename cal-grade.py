import csv
import os
def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "FAIL"


def calculate_results(input_file):
    results = []

    try:
        with open(input_file, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row["Name"]
                marks = []

                for key in row:
                    if key != "Name":
                        try:
                            marks.append(float(row[key]))
                        except ValueError:
                            pass

                if marks:
                    total     = sum(marks)
                    maximum   = len(marks) * 100
                    percentage = round((total / maximum) * 100, 2)
                    grade     = calculate_grade(percentage)

                    results.append({
                        "Name":       name,
                        "Total":      total,
                        "Maximum":    maximum,
                        "Percentage": percentage,
                        "Grade":      grade
                    })

    except FileNotFoundError:
        print(f"Error: {input_file} not found.")
        return []

    return results


def save_results(results, output_file):
    if not results:
        print("No results to save.")
        return

    fieldnames = ["Name", "Total", "Maximum", "Percentage", "Grade"]

    with open(output_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to: {output_file}")


def display_results(results):
    if not results:
        print("No results to display.")
        return

    print("\n" + "=" * 60)
    print(f"{'NAME':<20} {'TOTAL':<8} {'PERCENT':<10} {'GRADE':<6}")
    print("=" * 60)

    passed = 0
    failed = 0

    for r in results:
        print(f"{r['Name']:<20} {r['Total']:<8} {r['Percentage']:<10} {r['Grade']:<6}")
        if r["Grade"] == "FAIL":
            failed += 1
        else:
            passed += 1

    print("=" * 60)
    print(f"Total Students : {len(results)}")
    print(f"Passed         : {passed}")
    print(f"Failed         : {failed}")

    percentages = [r["Percentage"] for r in results]
    print(f"Class Average  : {round(sum(percentages) / len(percentages), 2)}%")
    print(f"Highest Score  : {max(percentages)}%")
    print(f"Lowest Score   : {min(percentages)}%")
    print("=" * 60)


def create_sample_input():
    """Creates a sample students.csv if none exists, so the app works immediately."""
    sample = [
        ["Name", "Maths", "Science", "English", "Telugu", "Hindi"],
        ["Ramesh Kumar",   85, 90, 78, 88, 92],
        ["Priya Sharma",   72, 68, 80, 75, 70],
        ["Suresh Reddy",   45, 50, 40, 55, 48],
        ["Anita Verma",    95, 92, 88, 90, 96],
        ["Kiran Babu",     60, 65, 58, 62, 70],
        ["Deepa Nair",     33, 40, 38, 42, 35],
        ["Vijay Teja",     78, 82, 75, 80, 85],
    ]
    with open("students.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(sample)
    print("Sample file 'students.csv' created.")


def main():
    print("\n====== STUDENT GRADE CALCULATOR ======")

    input_file  = "students.csv"
    output_file = "results.csv"

    if not os.path.exists(input_file):
        print(f"'{input_file}' not found. Creating sample file...")
        create_sample_input()

    print(f"\nReading data from: {input_file}")
    results = calculate_results(input_file)

    if results:
        display_results(results)
        save_results(results, output_file)
        print("\nDone! Open results.csv to see the full report.")


main()