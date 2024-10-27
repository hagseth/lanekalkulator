# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 09:39:31 2024

@author: alexa
"""
import streamlit as st
import matplotlib.pyplot as plt
import mplcyberpunk

st.set_page_config(layout="wide")

# Use a specific style
plt.rcParams['figure.dpi'] = 100
plt.style.use('cyberpunk')  # Choose a style that is easier on the eyes

st.write("## Restlån nedbetalingskalkulator")

st.write("Denne utbetalingskalkulatoren for boliglån hjelper deg med å evaluere hvordan ekstra betalinger kan spare renter og forkorte lånets løpetid.")

col1, col2 = st.columns(2)


help_input = "Hva er den nominelle renten din - uten terminomkostninger"

with col1:
    lånebeløp = st.number_input("Restlån", value= None, placeholder = "Eksempelvis 16000000", format="%0.0f")
    Månedlig_beløp = st.number_input("Terminbeløp - månedlig", value= None, placeholder = "Eksempelvis 12500", format="%0.0f")
    effektiv_rente = st.number_input("Nominell rente",value= None, placeholder = "Eksempelvis 5.5", help =help_input)
    månedlig_kostnad = st.number_input("Månedlig fast kostnad til banken", value=None, placeholder="Eksempelvis 200", format="%0.0f")
    ekstra_betaling = st.number_input("Hva vil du betale ekstra på lånet ditt i måneden", value= None, placeholder = "Eksempelvis 500", format="%0.0f")


# Check if the required inputs are filled out
if lånebeløp is not None and Månedlig_beløp is not None and effektiv_rente is not None and månedlig_kostnad is not None and ekstra_betaling is not None:

    def calculate_balance(lånebeløp, effektiv_rente, Månedlig_beløp, månedlig_kostnad, ekstra_betaling=0):
        monthly_interest_rate = effektiv_rente/100 / 12
        balances = [lånebeløp]
        total_interest_paid = 0 # Initialize the total interest accumulator
        month = 0
        
        
     # Run the loop until the balance reaches zero or negative
        while lånebeløp > 0:
            # Calculate the interest for the current month
            interest = lånebeløp * monthly_interest_rate
            total_interest_paid += interest  # Accumulate the interest
            
            # Add monthly fixed bank cost to the balance
            lånebeløp += månedlig_kostnad
    
            # Update the balance after interest and payment
            lånebeløp = lånebeløp + interest - Månedlig_beløp - ekstra_betaling
            
            # If the balance goes below zero, make it zero to show it’s fully paid
            lånebeløp = max(lånebeløp, 0)
            
            # Add the balance for the current month to the list
            balances.append(lånebeløp)
            
            # Check for an infinite loop in case the payment is too low
            month += 1
            if month > 500:  # prevent very long loops
                print("The monthly payment is too low to ever pay off the loan.")
                break
        
        return balances, month, total_interest_paid

    # Calculate the loan balance, months, and total interest paid
    balances, total_months, total_interest_paid = calculate_balance(lånebeløp, effektiv_rente, Månedlig_beløp, månedlig_kostnad)
    
    # Calculate loan balance with extra payment
    balances_with_extra, total_months_with_extra, total_interest_with_extra = calculate_balance(
        lånebeløp, effektiv_rente, Månedlig_beløp, månedlig_kostnad, ekstra_betaling=ekstra_betaling)
    
    # Convert months to years and months
    years = total_months // 12
    months = total_months % 12
    
    years_with_extra = total_months_with_extra // 12
    months_with_extra = total_months_with_extra % 12
    
    interest_saved = total_interest_paid - total_interest_with_extra
    
    # Plotting with Matplotlib
    fig, ax = plt.subplots()
    
    # Create x-values for the number of years
    x_no_extra = [m / 12 for m in range(len(balances))]
    x_with_extra = [m / 12 for m in range(len(balances_with_extra))]
    
    plt.plot(x_no_extra, balances, marker='o', label = "Orginal"
             , markersize=1.5, color='b')
    plt.plot(x_with_extra, balances_with_extra, label = "Med ekstra betaling"
             , marker='o', markersize=1.5, color='r', linewidth=0.5)
    
    # Title and labels
    ax.set_title("Månedlig restgjeld", fontsize=16, fontweight='bold')
    ax.set_xlabel("År", fontsize=10)
    ax.set_ylabel("Restlån (Kr)", fontsize=10)
    ax.legend(fontsize=10)
    
    
    mplcyberpunk.make_lines_glow(ax)
    
    ax.grid(True)
    
    plt.tight_layout()
    
    with col2:
        st.pyplot(fig) # Display line graph
    
    # Display the total time to pay off the loan
    with col1:
        st.write(f"Det vil ta deg **{years} år og {months} måneder** å betale ned lånet helt.")
        st.write(f"Total rente betalt over lånets løpetid er **{total_interest_paid:,.2f} kr**.")
        st.write(f"Med ekstra betaling på {ekstra_betaling:.0f} kr per måned vil det ta deg **{years_with_extra} år og {months_with_extra} måneder** å betale ned lånet helt.")
        st.write(f"Total rente betalt med ekstra betaling er **{total_interest_with_extra:,.2f} kr**.")
        st.write(f"Med å betale **{ekstra_betaling:,.2f} kr** i måneden sparer du **{interest_saved:,.2f} kr**.")
    
    
    fig_bar, ax_bar = plt.subplots(figsize=(8, 4))
    bar_labels = ['Med ekstra betaling', 'Orginal plan']
    bar_values = [ total_interest_with_extra, total_interest_paid]
    
    # Create horizontal bar chart
    ax_bar.barh(bar_labels, bar_values, color=['red', 'blue'])
    
    # Add titles and labels
    ax_bar.set_title('Total rente betalt', fontsize=16, fontweight='bold')
    ax_bar.set_xlabel('Rente (Kr)', fontsize=14)
    
    
    # Show values on bars
    for index, value in enumerate(bar_values):
        ax_bar.text(value, index, f'{value:,.2f} kr', va='center', fontsize=12)
    
    plt.tight_layout()
    
    with col2:
        st.pyplot(fig_bar)

    with col2:
        st.metric(label="Rentekostnad spart", value=f"{interest_saved:,.2f} kr")
