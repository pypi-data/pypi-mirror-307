from decimal import Decimal

def calculate_returns(price):
    """Calculate estimated returns after deducting taxes."""
    capital_gains_tax_rate = Decimal('0.33')  # 33%
    admin_tax_rate = Decimal('0.05')  # Example: 5% admin tax

    # Calculate total taxes
    total_tax_rate = capital_gains_tax_rate + admin_tax_rate
    total_tax = price * total_tax_rate
    estimated_returns = price - total_tax

    return estimated_returns


def calculate_stamp_duty(price):
    """Calculate stamp duty based on property price."""
    if price > Decimal('150000'):
        stamp_duty = price * Decimal('0.06')  # 6% for properties over 150k
    else:
        stamp_duty = price * Decimal('0.02')  # 2% for properties under 150k

    return stamp_duty


def calculate_admin_fee(price):
    """Calculate admin fee."""
    admin_fee = price * Decimal('0.0005')  # Example: 0.05% admin fee
    return admin_fee


def calculate_total_cost(price):
    """Calculate total cost including stamp duty and admin fee."""
    stamp_duty = calculate_stamp_duty(price)
    admin_fee = calculate_admin_fee(price)
    total_cost = price + stamp_duty + admin_fee

    return total_cost