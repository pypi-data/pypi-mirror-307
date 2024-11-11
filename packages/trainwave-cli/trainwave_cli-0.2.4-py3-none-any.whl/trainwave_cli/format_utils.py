def cents_to_dollars_str(cents: int) -> str:
    dollars = cents / 100
    return f"${dollars:,.2f}"
