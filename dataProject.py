# =============================================================================
# Grouped Data Statistics Application
# Name: [Imran Mohammede], P-Number: [P433238], Course: IY499
# Packages: pandas, numpy, matplotlib, statistics
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics as stat
import os
import csv

DATA_FILE = "data.csv"
user_data = []


# =============================================================================
# Gets a valid float from user, with optional min/max range check
# =============================================================================
def get_valid_float(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = float(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Error: Value must be at least {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"Error: Value must be at most {max_val}")
                continue
            return value
        except ValueError:
            print("Error: Invalid input. Please enter a valid number.")


# =============================================================================
# Collects data from user and saves to CSV using pandas
# =============================================================================
def get_user_data():
    global user_data

    print("\n" + "="*50)
    print("       DATA ENTRY")
    print("="*50)

    count = int(get_valid_float("How many data points do you want to enter? ", min_val=1))

    temp_data = []
    print(f"\nPlease enter {count} numerical values (one per line):")
    for i in range(count):
        value = get_valid_float(f"  Data point {i+1}: ")
        temp_data.append(value)

    class_width = get_valid_float("\nEnter the class width for grouping data: ", min_val=0.1)

    try:
        # Save to CSV using pandas DataFrame
        df = pd.DataFrame({
            'data': temp_data,
            'class_width': [class_width] * len(temp_data)
        })
        df.to_csv(DATA_FILE, index=False)
        user_data = temp_data.copy()
        print(f"\n[SUCCESS] {count} data points saved to '{DATA_FILE}'.")
        print(f"          Class width set to: {class_width}")
    except Exception as e:
        print(f"\n[ERROR] Failed to save data: {e}")


# =============================================================================
# Reads data from CSV file using pandas
# Returns (data, class_width) or (None, None) if file not found
# =============================================================================
def read_data():
    global user_data

    if not os.path.exists(DATA_FILE):
        print(f"\n[ERROR] File '{DATA_FILE}' not found. Please add data first (Option 1).")
        return None, None

    try:
        df = pd.read_csv(DATA_FILE)
        user_data = df['data'].tolist()
        class_width = df['class_width'].iloc[0] if 'class_width' in df.columns else None

        if not user_data:
            print("\n[WARNING] No data found in the file.")
            return None, None

        print(f"\n[SUCCESS] Loaded {len(user_data)} data points from '{DATA_FILE}'.")
        return user_data, class_width
    except Exception as e:
        print(f"\n[ERROR] Failed to read data: {e}")
        return None, None


# =============================================================================
# Groups data into classes and counts frequencies
# Returns a dictionary with classes, frequencies, sorted_data, and class_width
# =============================================================================
def create_grouped_data(data, class_width):
    if not data or class_width is None:
        return None

    sorted_data = sorted(data)  # Sorting algorithm for grouping
    min_val = min(sorted_data)
    max_val = max(sorted_data)

    # Calculate number of classes: ceil(range / width) + 1
    num_classes = int(np.ceil((max_val - min_val) / class_width)) + 1

    classes = []
    frequencies = []

    for i in range(num_classes):
        lower = min_val + (i * class_width)
        upper = lower + class_width
        freq = sum(1 for x in sorted_data if lower <= x < upper)

        if freq > 0 or i == 0:
            classes.append((lower, upper))
            frequencies.append(freq)

    # Remove empty classes at the end
    while frequencies and frequencies[-1] == 0:
        frequencies.pop()
        classes.pop()

    return {
        'classes': classes,
        'frequencies': frequencies,
        'sorted_data': sorted_data,
        'class_width': class_width
    }


# =============================================================================
# Computes and displays mean, median, mode, variance, and standard deviation
# =============================================================================
def compute_statistics(data):
    if data is None or len(data) == 0:
        print("\n[ERROR] No data available. Please load data first (Option 1 or 2).")
        return None

    print("\n" + "="*50)
    print("       STATISTICAL ANALYSIS")
    print("="*50)

    mean_val = stat.mean(data)
    median_val = stat.median(data)

    # Mode: handle multi-modal case (no unique mode)
    try:
        mode_val = stat.mode(data)
        mode_str = str(mode_val)
    except stat.StatisticsError:
        from collections import Counter
        counts = Counter(data)
        max_freq = max(counts.values())
        modes = [k for k, v in counts.items() if v == max_freq]
        mode_str = ", ".join(str(m) for m in modes) + " (multi-modal)"

    # Variance and stdev need at least 2 data points
    if len(data) > 1:
        variance_val = stat.variance(data)
        std_dev_val = stat.stdev(data)
    else:
        variance_val = 0.0
        std_dev_val = 0.0

    range_val = max(data) - min(data)

    print(f"\n  Number of data points:  {len(data)}")
    print(f"  Minimum value:          {min(data):.4f}")
    print(f"  Maximum value:          {max(data):.4f}")
    print(f"  Range:                  {range_val:.4f}")
    print(f"  Mean:                   {mean_val:.4f}")
    print(f"  Median:                 {median_val:.4f}")
    print(f"  Mode:                   {mode_str}")
    print(f"  Variance:               {variance_val:.4f}")
    print(f"  Standard Deviation:     {std_dev_val:.4f}")
    print("="*50)

    return {
        'mean': mean_val,
        'median': median_val,
        'mode': mode_str,
        'variance': variance_val,
        'std_dev': std_dev_val,
        'range': range_val,
        'count': len(data)
    }


# =============================================================================
# Finds the class with the highest frequency
# =============================================================================
def compute_modal_class(grouped_data):
    if not grouped_data or not grouped_data['frequencies']:
        return None

    frequencies = grouped_data['frequencies']
    classes = grouped_data['classes']

    max_freq = max(frequencies)
    modal_index = frequencies.index(max_freq)

    return classes[modal_index], max_freq


# =============================================================================
# Displays a frequency table and draws a histogram using Matplotlib
# =============================================================================
def draw_histogram(data):
    if data is None or len(data) == 0:
        print("\n[ERROR] No data available. Please load data first (Option 1 or 2).")
        return

    _, class_width = read_data()
    if class_width is None:
        class_width = get_valid_float("Enter class width for histogram: ", min_val=0.1)

    grouped = create_grouped_data(data, class_width)
    if not grouped:
        print("[ERROR] Could not create grouped data.")
        return

    classes = grouped['classes']
    frequencies = grouped['frequencies']

    # Build bin edges for matplotlib histogram
    bin_edges = [c[0] for c in classes] + [classes[-1][1]]

    # Print frequency distribution table
    print("\n" + "="*50)
    print("       GROUPED DATA TABLE")
    print("="*50)
    print(f"{'Class Interval':<20} {'Frequency':<12} {'Midpoint':<12}")
    print("-" * 50)

    for i, (cls, freq) in enumerate(zip(classes, frequencies)):
        midpoint = (cls[0] + cls[1]) / 2
        print(f"{cls[0]:.2f} - {cls[1]:.2f}       {freq:<12} {midpoint:.2f}")

    modal_class, modal_freq = compute_modal_class(grouped)
    if modal_class:
        print("-" * 50)
        print(f"Modal Class: {modal_class[0]:.2f} - {modal_class[1]:.2f} (Frequency: {modal_freq})")
    print("="*50)

    # Draw histogram with matplotlib
    print("\nGenerating histogram...")
    plt.figure(figsize=(10, 6))
    n, bins, patches = plt.hist(data, bins=bin_edges, edgecolor='black',
                                 color='skyblue', alpha=0.7, rwidth=0.95)
    plt.xlabel('Data Values', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title(f'Histogram of Grouped Data\n(Class Width: {class_width})', fontsize=14)
    plt.grid(axis='y', alpha=0.3, linestyle='--')

    # Add frequency labels on top of bars
    for i, (rect, freq) in enumerate(zip(patches, frequencies)):
        if freq > 0:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width()/2., height,
                    f'{int(freq)}', ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.show()
    print("[SUCCESS] Histogram displayed.")


# =============================================================================
# Shows the current data stored in memory
# =============================================================================
def display_data():
    global user_data

    if not user_data:
        print("\n[INFO] No data in memory. Please load data first.")
        return

    print("\n" + "="*50)
    print("       CURRENT DATA")
    print("="*50)
    print(f"Total data points: {len(user_data)}")
    print(f"Data: {user_data}")
    print("="*50)


# =============================================================================
# Main menu loop - runs until user chooses to exit
# =============================================================================
def main():
    print("\n" + "="*50)
    print("   GROUPED DATA STATISTICS APPLICATION")
    print("="*50)
    print("   IY499 - Introduction to Programming")
    print("="*50)

    # Load existing data on startup if available
    if os.path.exists(DATA_FILE):
        read_data()

    while True:
        menu = "\n" + "-"*50
        menu += "\n                 MAIN MENU"
        menu += "\n" + "-"*50
        menu += "\n   1. Add and Save Data"
        menu += "\n   2. Show Statistics"
        menu += "\n   3. Draw Histogram"
        menu += "\n   4. View Current Data"
        menu += "\n   5. Exit"
        menu += "\n" + "-"*50
        print(menu)

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            get_user_data()

        elif choice == "2":
            if not user_data:
                data, _ = read_data()
                if data:
                    compute_statistics(data)
                else:
                    print("\n[INFO] Please add data first (Option 1).")
            else:
                compute_statistics(user_data)

        elif choice == "3":
            if not user_data:
                data, _ = read_data()
                if data:
                    draw_histogram(data)
                else:
                    print("\n[INFO] Please add data first (Option 1).")
            else:
                draw_histogram(user_data)

        elif choice == "4":
            if not user_data:
                data, _ = read_data()
                if data:
                    display_data()
                else:
                    print("\n[INFO] No data available. Please add data first (Option 1).")
            else:
                display_data()

        elif choice == "5":
            print("\n" + "="*50)
            print("   Thank you for using the application!")
            print("   Goodbye!")
            print("="*50 + "\n")
            break

        else:
            print("\n[ERROR] Invalid option. Please enter a number between 1 and 5.")


# =============================================================================
# Entry point - runs main() only when this file is executed directly
# =============================================================================
if __name__ == "__main__":
    main()