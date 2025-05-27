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
    sys_tf = TransferFunction(num_coeffs, den_coeffs)
    
    plt.figure(figsize=(10, 8))
    

    from control.matlab import pzmap
    poles, zeros = pzmap(sys_tf, plot=False)
    

    plt.grid(True, linestyle='-', alpha=0.5)
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.7)
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.7)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', alpha=0.3)
    

    from control import root_locus
    

    fig = plt.gcf()
    ax = fig.gca()
    

    from control.rlocus import root_locus_map
    

    try:

        from control.rlocus import root_locus_map
        kvect = np.logspace(-2, 2, 1000)  # from 0.01 to 100
        clist, rlist = root_locus_map(sys_tf, kvect)
        

        for i in range(rlist.shape[1]):

            trajectory = rlist[:, i]
            

            plt.plot(trajectory.real, trajectory.imag, '-', linewidth=2, color='blue')
            

            indices = np.linspace(0, len(trajectory)-1, 10, dtype=int)
            plt.plot(trajectory[indices].real, trajectory[indices].imag, 'bo', markersize=4)
    except:


        root_locus(sys_tf)
        

        for line in ax.get_lines():

            if line.get_color() == 'b' and line.get_marker() == '' and line.get_linestyle() == '-':
                line.set_linewidth(2)
                line.set_visible(True)
    

    plt.plot(np.real(poles), np.imag(poles), 'rx', markersize=10, label='Poles')
    if len(zeros) > 0:
        plt.plot(np.real(zeros), np.imag(zeros), 'go', markersize=10, label='Zeros')
    

    plt.plot([], [], 'b-', linewidth=2, label='Root Locus')
    plt.legend(fontsize=10)
    

    plt.title('Root Locus Plot', fontsize=14, fontweight='bold')
    plt.xlabel('Real Axis', fontsize=12)
    plt.ylabel('Imaginary Axis', fontsize=12)
    
    # Get and plot poles and zeros
    from control.matlab import pzmap
    poles, zeros = pzmap(sys_tf, plot=False)
    

    plt.plot(np.real(poles), np.imag(poles), 'rx', markersize=10, label='Poles')
    if len(zeros) > 0:
        plt.plot(np.real(zeros), np.imag(zeros), 'go', markersize=10, label='Zeros')
    
    plt.title('Root Locus Plot', fontsize=14, fontweight='bold')
    plt.xlabel('Real Axis', fontsize=12)
    plt.ylabel('Imaginary Axis', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.5)
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.5)
    plt.legend(fontsize=10)
    
    # Set equal aspect ratio for better visualization
    plt.axis('equal')
    
    # Add minor gridlines for more detailed grid
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', alpha=0.4)
    

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    

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
