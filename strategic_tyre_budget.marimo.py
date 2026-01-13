# /// script
# [tool.marimo.runtime]
# auto_instantiate = false
# ///

import marimo

__generated_with = "0.19.2"
app = marimo.App(width="medium", app_title="tyre_budget")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    return mo, np, pd, plt


@app.cell
def _(mo):
    mo.md("""
    # Tyre Budget Planner

    This interactive notebook helps you plan and visualize your tyre budget. Enter your requirements and see a breakdown of costs.
    """)
    return


@app.cell
def _(mo):
    # UI elements for user input
    num_vehicles = mo.ui.number(value=1, label="Number of Vehicles")
    tyres_per_vehicle = mo.ui.number(value=4, label="Tyres per Vehicle")
    avg_price_per_tyre = mo.ui.number(value=100, label="Average Price per Tyre ($)")
    replacement_interval = mo.ui.number(value=3, label="Replacement Interval (years)")
    budget_years = mo.ui.number(value=5, label="Budget Planning Period (years)")

    mo.vstack([
        num_vehicles,
        tyres_per_vehicle,
        avg_price_per_tyre,
        replacement_interval,
        budget_years
    ])
    return (
        avg_price_per_tyre,
        budget_years,
        num_vehicles,
        replacement_interval,
        tyres_per_vehicle,
    )


@app.cell
def _(
    avg_price_per_tyre,
    budget_years,
    mo,
    np,
    num_vehicles,
    pd,
    replacement_interval,
    tyres_per_vehicle,
):
    # Calculate total tyres needed per replacement
    vehicles = num_vehicles.value
    tyres = tyres_per_vehicle.value
    price = avg_price_per_tyre.value
    interval = replacement_interval.value
    years = budget_years.value

    # Validation
    mo.stop(vehicles <= 0 or tyres <= 0 or price <= 0 or interval <= 0 or years <= 0, 
            mo.md("**Please enter positive values for all fields.**"))

    total_tyres_per_replacement = vehicles * tyres
    num_replacements = int(np.ceil(years / interval))
    total_tyres_needed = total_tyres_per_replacement * num_replacements
    total_cost = total_tyres_needed * price

    summary = pd.DataFrame({
        "Description": [
            "Vehicles",
            "Tyres per Vehicle",
            "Average Price per Tyre ($)",
            "Replacement Interval (years)",
            "Budget Period (years)",
            "Total Tyres Needed",
            "Total Cost ($)"
        ],
        "Value": [
            vehicles,
            tyres,
            price,
            interval,
            years,
            total_tyres_needed,
            total_cost
        ]
    })

    summary
    return interval, price, total_tyres_per_replacement, years


@app.cell
def _(interval, pd, price, total_tyres_per_replacement, years):
    # Yearly breakdown of tyre replacements and costs
    breakdown = []
    for year in range(1, years + 1):
        if (year - 1) % interval == 0:
            tyres_replaced = total_tyres_per_replacement
            cost = tyres_replaced * price
        else:
            tyres_replaced = 0
            cost = 0
        breakdown.append({
            "Year": year,
            "Tyres Replaced": tyres_replaced,
            "Cost ($)": cost
        })
    breakdown_df = pd.DataFrame(breakdown)
    breakdown_df
    return (breakdown_df,)


@app.cell
def _(breakdown_df, plt):
    # Visualization of yearly costs
    plt.figure(figsize=(8, 4))
    plt.bar(breakdown_df["Year"], breakdown_df["Cost ($)"])
    plt.xlabel("Year")
    plt.ylabel("Cost ($)")
    plt.title("Yearly Tyre Replacement Cost")
    plt.gca()
    return


if __name__ == "__main__":
    app.run()
