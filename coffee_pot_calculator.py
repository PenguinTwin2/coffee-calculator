"""
Coffee Pot Grinds & Water Calculator
-----------------------------------
Calculates the required coffee grinds (in tablespoons and cups)
based on:
  1. Water ratio: 2 tablespoons (tbsp) coffee per 6 oz of water.
  2. Pot calibration: 3 pot lines = 2 cups of water (where 1 cup = 8 fl oz).
"""

from fractions import Fraction
from typing import Dict

# Standard conversion constants
FL_OZ_PER_CUP = 8.0               # 1 standard US measuring cup = 8 fluid ounces
TBSP_PER_CUP = 16.0               # 1 measuring cup = 16 tablespoons
TSP_PER_TBSP = 3.0                # 1 tablespoon = 3 teaspoons

# Recipe and pot specifications
TBSP_PER_OZ_WATER = 2.0 / 6.0     # 2 tbsp of grinds per 6 fl oz of water
CUPS = 2                          # numerator of cup to line ratio
LINES = 3                         # denominator of cup to line ratio
CUPS_PER_LINES = 2.0 / 3.0        # default of 3 pot lines to 2 cups water


def format_fraction(value: float, max_denominator: int = 8) -> str:
    """
    Converts a decimal number into a clean mixed fraction string
    (e.g., 5.33 -> '5 1/3', 0.5 -> '1/2').
    """
    if abs(value) < 1e-4:
        return "0"

    whole_part = int(value)
    fractional_part = value - whole_part
    frac = Fraction(fractional_part).limit_denominator(max_denominator)

    if frac.numerator == 0:
        return str(whole_part)
    elif whole_part == 0:
        return f"{frac.numerator}/{frac.denominator}"
    elif frac.numerator == frac.denominator:
        return str(whole_part + 1)
    else:
        return f"{whole_part} {frac.numerator}/{frac.denominator}"


def break_down_tbsp(total_tbsp: float) -> str:
    """
    Breaks down tablespoons into full tablespoons and remaining teaspoons
    for practical kitchen measuring.
    """
    whole_tbsp = int(total_tbsp)
    remainder_tbsp = total_tbsp - whole_tbsp
    teaspoons = remainder_tbsp * TSP_PER_TBSP

    parts = []
    if whole_tbsp > 0:
        parts.append(f"{whole_tbsp} tbsp")
    if teaspoons > 0.05:
        parts.append(f"{format_fraction(teaspoons, 4)} tsp")

    return " + ".join(parts) if parts else "0 tbsp"


def calculate_coffee(lines: float) -> Dict[str, float]:
    """
    Computes water and coffee amounts for a given number of pot lines.
    
    Formula:
      - Water Cups = lines * (2 cups / 3 lines)
      - Water Ounces = Water Cups * 8 fl oz
      - Coffee Tablespoons = Water Ounces * (2 tbsp / 6 oz)
      - Coffee Cups = Coffee Tablespoons / 16 tbsp
    """
    # Water calculations
    water_cups = lines * CUPS_PER_LINES
    water_oz = water_cups * FL_OZ_PER_CUP

    # Coffee grinds calculations
    coffee_tbsp = water_oz * TBSP_PER_OZ_WATER
    coffee_cups = coffee_tbsp / TBSP_PER_CUP

    return {
        "lines": lines,
        "water_cups": water_cups,
        "water_oz": water_oz,
        "coffee_tbsp": coffee_tbsp,
        "coffee_cups": coffee_cups,
    }


def display_recipe(results: Dict[str, float]) -> None:
    """
    Displays a neatly formatted summary of the coffee recipe.
    """
    lines       = results["lines"]
    water_cups  = results["water_cups"]
    water_oz    = results["water_oz"]
    coffee_tbsp = results["coffee_tbsp"]
    coffee_cups = results["coffee_cups"]

    print("\n" + "=" * 50)
    print(f"          COFFEE BREWING SPECIFICATION")
    print("=" * 50)
    print(f" Pot Target        : {lines:g} line{'s' if lines != 1 else ''}")
    print(f" Water Volume      : {water_oz:.2f} fl oz ({format_fraction(water_cups)} standard cups)")
    print("-" * 50)
    print(" COFFEE GRINDS NEEDED:")
    print(f"   • Tablespoons   : {coffee_tbsp:.2f} tbsp ({format_fraction(coffee_tbsp)} tbsp)")
    print(f"   • Measuring Cups: {coffee_cups:.2f} cups ({format_fraction(coffee_cups)} cup)")
    print(f"   • Kitchen Scoop : {break_down_tbsp(coffee_tbsp)}")
    print("=" * 50)

    # Useful kitchen guidance
    if coffee_cups >= 0.25:
        print(f" TIP: For large batches, measure out grinds using")
        print(f"      your measuring cups ({format_fraction(coffee_cups)} cup) to save time.")
    else:
        print(" TIP: Measuring directly with a tablespoon is")
        print("      easiest for this size.")
    print("=" * 50 + "\n")


def change_line_ratio():
    """
    Asks user for edited pot line to cup ratio.
    """
    while True:
        try:
            raw_input = input("What is the coffee pot line to cup ratio? ").strip()

            ratio = [n for n in raw_input if n.isdigit()]
            if any(int(n) <= 0 for n in ratio):
                print("ERROR:  Please enter a number greater than 0.")
                continue
            
            global CUPS
            CUPS = int(ratio[1])
            global LINES
            LINES = int(ratio[0])
            global CUPS_PER_LINES
            CUPS_PER_LINES = float(ratio[1]) / float(ratio[0])

            print(f"\nThe ratio is now {LINES} lines = {CUPS} cups of water\n")
            return ratio
        except ValueError:
            print("ERROR:  Invalid input. Please enter 2 valid numbers (e.g., 3, 6, 8.5) or 'q' to quit.")


def get_user_lines() -> float:
    """
    Prompts user for input and ensures a valid positive number is provided.
    """
    while True:
        try:
            raw_input = input("How many lines of coffee would you like to make? ").strip()

            # Edit pot line to cup ratio
            if raw_input.lower() in {"c", "change"}:
                return "change"

            lines = float(raw_input)
            if lines <= 0:
                print("ERROR:  Please enter a number greater than 0.")
                continue
            return lines
        except ValueError:
            print("ERROR:  Invalid input. Please enter a valid number (e.g., 3, 6, 8.5).")


def main() -> None:
    """
    Main application loop for interactive coffee calculation.
    """
    print( "--------------------------------------------------")
    print( "    Welcome to the Coffee Pot Grinds Calculator   ")
    print(f"    Rule: {LINES} lines = {CUPS} cups of water    ")
    print( "    type \"c\" to change line to cup ratio        ")
    print( "    Ratio: 2 tbsp grinds per 6 oz water           ")
    print( "--------------------------------------------------")

    while True:
        lines = get_user_lines()

        # if lines < 0:
        #     print("\nEnjoy your coffee! Goodbye.\n")
        #     break
        if lines == "change":
            change_line_ratio()
            continue

        results = calculate_coffee(lines)
        display_recipe(results)

        again = input("Calculate another pot? (y/n): ").strip().lower()
        if again not in {"y", "yes"}:
            print("\nEnjoy your coffee! Goodbye.\n")
            break


if __name__ == "__main__":
    main()