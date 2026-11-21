
# DTI412 Lab 03-04
# Part 6: Advanced Challenge Exercises
# Q Objects and F Expressions

from decimal import Decimal

from django.db.models import (
    Q,
    F,
    Case,
    When,
    DecimalField
)

from inventory.models import Category, Product


# ==========================================
# CREATE SAMPLE DATA
# ==========================================

print("\nCREATING SAMPLE DATA")

electronics, _ = Category.objects.get_or_create(
    name="Electronics"
)

gadgets, _ = Category.objects.get_or_create(
    name="Gadgets"
)

laptop, _ = Product.objects.update_or_create(
    name="Laptop",
    defaults={
        "category": electronics,
        "price": Decimal("12000.00"),
        "max_allowed_price": Decimal("15000.00"),
        "stock_quantity": 4,
        "reorder_level": 5,
        "is_promotional": False,
        "status": "NORMAL",
        "warehouse_country": "China",
        "total_sold": 0,
        "total_revenue": Decimal("0.00"),
    }
)

headset, _ = Product.objects.update_or_create(
    name="Headset",
    defaults={
        "category": electronics,
        "price": Decimal("8000.00"),
        "max_allowed_price": Decimal("10000.00"),
        "stock_quantity": 15,
        "reorder_level": 10,
        "is_promotional": True,
        "status": "DISCOUNTED",
        "warehouse_country": "Thailand",
        "total_sold": 0,
        "total_revenue": Decimal("0.00"),
    }
)

watch, _ = Product.objects.update_or_create(
    name="Smart Watch",
    defaults={
        "category": gadgets,
        "price": Decimal("1000.00"),
        "max_allowed_price": Decimal("1100.00"),
        "stock_quantity": 10,
        "reorder_level": 5,
        "is_promotional": False,
        "status": "NORMAL",
        "warehouse_country": "Thailand",
        "total_sold": 0,
        "total_revenue": Decimal("0.00"),
    }
)

charger, _ = Product.objects.update_or_create(
    name="Charger",
    defaults={
        "category": gadgets,
        "price": Decimal("500.00"),
        "max_allowed_price": Decimal("700.00"),
        "stock_quantity": 1,
        "reorder_level": 3,
        "is_promotional": False,
        "status": "NORMAL",
        "warehouse_country": "Thailand",
        "total_sold": 0,
        "total_revenue": Decimal("0.00"),
    }
)

print("Sample products created successfully.")


# ==========================================
# CHALLENGE 1
# ADVANCED CONDITIONAL SEARCH & NESTED LOGIC
# ==========================================

print("\n========== CHALLENGE 1 ==========")

results = Product.objects.filter(
    (
        Q(category__name="Electronics")
        &
        Q(price__gt=10000)
    )
    |
    (
        Q(status="DISCOUNTED")
        &
        ~Q(warehouse_country="China")
    )
)

for product in results:
    print(
        f"Product: {product.name}, "
        f"Price: {product.price}, "
        f"Status: {product.status}"
    )

print("SQL Query:", results.query)


# ==========================================
# CHALLENGE 2
# DYNAMIC STOCK THRESHOLD ALERT
# ==========================================

print("\n========== CHALLENGE 2 ==========")

alerts = Product.objects.filter(
    Q(stock_quantity__lte=F("reorder_level"))
    |
    (
        Q(is_promotional=True)
        &
        Q(
            stock_quantity__lt=F("reorder_level") * 2
        )
    )
)

for product in alerts:
    print(
        f"Stock Alert: {product.name}, "
        f"Stock: {product.stock_quantity}, "
        f"Reorder Level: {product.reorder_level}"
    )


# ==========================================
# CHALLENGE 3
# ATOMIC PRICE INCREASE WITH SAFETY CEILING
# ==========================================

print("\n========== CHALLENGE 3 ==========")

updated = Product.objects.filter(
    category__name="Gadgets"
).update(
    price=Case(
        When(
            price__gt=F("max_allowed_price") / Decimal("1.15"),
            then=F("max_allowed_price")
        ),
        default=F("price") * Decimal("1.15"),
        output_field=DecimalField(
            max_digits=10,
            decimal_places=2
        )
    )
)

print("Updated Products:", updated)

for product in Product.objects.filter(
    category__name="Gadgets"
):
    print(
        f"Product: {product.name}, "
        f"New Price: {product.price}, "
        f"Maximum Price: {product.max_allowed_price}"
    )


# ==========================================
# CHALLENGE 4
# ATOMIC PURCHASE GUARD CONSTRAINT
# ==========================================

print("\n========== CHALLENGE 4 ==========")

# Successful purchase
quantity = 2

purchase_result = Product.objects.filter(
    pk=watch.pk,
    stock_quantity__gte=quantity
).update(
    stock_quantity=F("stock_quantity") - quantity,
    total_sold=F("total_sold") + quantity,
    total_revenue=F("total_revenue") + (
        F("price") * quantity
    )
)

if purchase_result == 1:
    print("Purchase Successful")
else:
    print("Purchase Failed: Insufficient Stock")

watch.refresh_from_db()

print("Product:", watch.name)
print("Remaining Stock:", watch.stock_quantity)
print("Total Sold:", watch.total_sold)
print("Total Revenue:", watch.total_revenue)


# Test unsuccessful purchase
print("\nTesting purchase with insufficient stock")

quantity = 5

failed_purchase = Product.objects.filter(
    pk=charger.pk,
    stock_quantity__gte=quantity
).update(
    stock_quantity=F("stock_quantity") - quantity,
    total_sold=F("total_sold") + quantity,
    total_revenue=F("total_revenue") + (
        F("price") * quantity
    )
)

if failed_purchase == 1:
    print("Second Purchase Successful")
else:
    print("Second Purchase Failed: Insufficient Stock")

charger.refresh_from_db()

print("Charger Remaining Stock:", charger.stock_quantity)

print("\nALL FOUR BONUS CHALLENGES COMPLETED")
