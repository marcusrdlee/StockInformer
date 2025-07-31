#!/usr/bin/env python3
"""
Terminal Helper Functions for Interactive Investment Planning
"""


def get_user_risk_level():
    print("\nWhat is your risk level?")
    print("1. Low")
    print("2. Medium")
    print("3. High")

    while True:
        choice = input("Enter your choice (1-3): ")
        if choice == "1":
            risk_level = "Low"
            break
        elif choice == "2":
            risk_level = "Medium"
            break
        elif choice == "3":
            risk_level = "High"
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    print(f"Your risk level is {risk_level}")
    return risk_level


def get_user_industry():
    while True:
        industry = input(
            "What industry are you interested in? (or press Enter for any): "
        ).strip()
        if industry:
            print(f"{industry} sounds great!")
            return industry
        else:
            print("No specific industry selected.")
            return None


def get_user_investment_amount():
    while True:
        try:
            amount_str = input("How much money do you want to invest? (e.g., 50000): $")
            investment_amount = float(amount_str.replace(",", "").replace("$", ""))
            if investment_amount > 0:
                print(f"You want to invest ${investment_amount:,.2f}")
                return investment_amount
            else:
                print("Please enter a positive amount.")
        except ValueError:
            print("Please enter a valid number.")


def get_user_time_horizon():
    while True:
        time_horizon = input(
            "How long do you want to invest for? (e.g., '1 year', '5 years'): "
        ).strip()
        if time_horizon:
            print(f"You want to invest for {time_horizon}")
            return time_horizon
        else:
            print("Please enter a time horizon.")


def get_user_investment_profile():
    print("🤖 Investment Planning Agent - Interactive Mode")
    print("=" * 50)

    risk_level = get_user_risk_level()
    industry = get_user_industry()
    investment_amount = get_user_investment_amount()
    time_horizon = get_user_time_horizon()

    print("\n" + "=" * 50)
    print("📋 Your Investment Profile:")
    print(f"Risk Level: {risk_level}")
    print(f"Industry: {industry or 'Any'}")
    print(f"Investment Amount: ${investment_amount:,.2f}")
    print(f"Time Horizon: {time_horizon}")
    print("=" * 50)

    return {
        "risk_level": risk_level,
        "industry": industry,
        "investment_amount": investment_amount,
        "time_horizon": time_horizon,
    }


if __name__ == "__main__":
    profile = get_user_investment_profile()
    print(f"\nProfile collected: {profile}")
