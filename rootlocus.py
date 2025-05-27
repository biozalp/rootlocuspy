import sys
import re
import numpy as np
import matplotlib.pyplot as plt
from control import TransferFunction, root_locus
from sympy import symbols, sympify, Poly

def parse_latex_tf(latex_str):
    latex_str = latex_str.replace('\\frac{', '').replace('}{', '/')
    latex_str = latex_str.replace('}', '')
    
    parts = latex_str.split('/')
    if len(parts) != 2:
        raise ValueError("Invalid transfer function format. Expected \\frac{numerator}{denominator}")
    
    num_str, den_str = parts
    

    num_str = re.sub(r's\^(\d+)', r's**\1', num_str)
    den_str = re.sub(r's\^(\d+)', r's**\1', den_str)
    

    num_str = re.sub(r'(\d)s', r'\1*s', num_str)
    den_str = re.sub(r'(\d)s', r'\1*s', den_str)
    

    s = symbols('s')
    

    try:
        num_expr = sympify(num_str)
        den_expr = sympify(den_str)
        

        num_poly = Poly(num_expr, s)
        den_poly = Poly(den_expr, s)
        

        num_coeffs = num_poly.all_coeffs()
        den_coeffs = den_poly.all_coeffs()
        

        num_coeffs = np.array([float(c) for c in num_coeffs])
        den_coeffs = np.array([float(c) for c in den_coeffs])
        
        return num_coeffs, den_coeffs
    except Exception as e:
        print(f"Error parsing transfer function: {e}")
        print("Please ensure your input is in the format: \\frac{numerator}{denominator}")
        print("Example: \\frac{s^2 + 3s + 2}{s^3 + 4s^2 + 5s + 2}")
        sys.exit(1)

def plot_root_locus(num_coeffs, den_coeffs):
    # Create the transfer function
    sys_tf = TransferFunction(num_coeffs, den_coeffs)
    
    # Create a new figure with a good size
    plt.figure(figsize=(10, 8))
    
    # Get poles and zeros
    from control.matlab import pzmap
    poles, zeros = pzmap(sys_tf, plot=False)
    
    # Set up the grid first
    plt.grid(True, linestyle='-', alpha=0.5)
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.7)
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.7)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', alpha=0.3)
    
    # Use a direct approach with control.matlab functions
    from control.matlab import rlocus
    
    # Calculate and plot the root locus
    # This will draw the lines directly
    rlocus(sys_tf)
    
    # Get the current axes
    ax = plt.gca()
    
    # Turn off equal aspect ratio to fix scaling issues
    ax.set_aspect('auto')
    
    # Make sure the root locus lines are visible and thick enough
    for line in ax.get_lines():
        # If it's a root locus line (blue line)
        if line.get_color() == 'b':
            line.set_linewidth(2)  # Make lines thicker
            line.set_visible(True)  # Ensure it's visible
    
    # Plot poles and zeros with clear markers
    plt.plot(np.real(poles), np.imag(poles), 'rx', markersize=10, label='Poles')
    if len(zeros) > 0:
        plt.plot(np.real(zeros), np.imag(zeros), 'go', markersize=10, label='Zeros')
    
    # Add a legend
    plt.legend(fontsize=10)
    
    # Add title and labels
    plt.title('Root Locus Plot', fontsize=14, fontweight='bold')
    plt.xlabel('Real Axis', fontsize=12)
    plt.ylabel('Imaginary Axis', fontsize=12)
    
    # Calculate reasonable axis limits
    all_points = np.concatenate([poles, zeros]) if len(zeros) > 0 else poles
    if len(all_points) > 0:
        real_vals = np.real(all_points)
        imag_vals = np.imag(all_points)
        
        # Get min/max with padding
        real_min, real_max = real_vals.min(), real_vals.max()
        imag_min, imag_max = imag_vals.min(), imag_vals.max()
        
        # Add padding (50% on each side)
        real_range = real_max - real_min
        imag_range = imag_max - imag_min
        
        # Handle cases where all points are at the same location
        real_padding = max(real_range * 0.5, 2.0) if real_range > 0 else 2.0
        imag_padding = max(imag_range * 0.5, 2.0) if imag_range > 0 else 2.0
        
        # Set limits with padding
        plt.xlim(real_min - real_padding, real_max + real_padding)
        plt.ylim(imag_min - imag_padding, imag_max + imag_padding)
    else:
        # Default limits if no poles or zeros
        plt.xlim(-5, 5)
        plt.ylim(-5, 5)
    
    # Adjust layout
    plt.tight_layout()
    
    # Show the plot
    plt.show(block=True)

def main():
    if len(sys.argv) > 1:
        latex_tf = ' '.join(sys.argv[1:])
    else:
        print("Enter the transfer function in LaTeX format:")
        print("Example: \\frac{s^2 + 3s + 2}{s^3 + 4s^2 + 5s + 2}")
        latex_tf = input("> ")
    

    num_coeffs, den_coeffs = parse_latex_tf(latex_tf)
    

    print("\nParsed Transfer Function:")
    print(f"Numerator coefficients: {num_coeffs}")
    print(f"Denominator coefficients: {den_coeffs}")
    

    sys_tf = TransferFunction(num_coeffs, den_coeffs)
    print(f"\nTransfer Function: {sys_tf}")
    

    plot_root_locus(num_coeffs, den_coeffs)

if __name__ == "__main__":
    main()
