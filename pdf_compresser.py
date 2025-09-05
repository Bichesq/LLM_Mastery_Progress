import PyPDF2
import os
import subprocess
import sys

def compress_pdf_advanced(input_path, output_path, method='auto'):
    """
    Advanced PDF compression with multiple methods
    """
    try:
        if method == 'ghostscript':
            # Use Ghostscript for professional compression
            try:
                # Adjust compression level (dPDFSETTINGS)
                # /screen - low quality, smallest size
                # /ebook - medium quality
                # /printer - high quality
                # /prepress - very high quality
                
                cmd = [
                    'gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                    '-dPDFSETTINGS=/ebook', '-dNOPAUSE', '-dQUIET', '-dBATCH',
                    f'-sOutputFile={output_path}', input_path
                ]
                
                subprocess.run(cmd, check=True)
                return True
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("Ghostscript not found, falling back to PyPDF2")
                return compress_pdf_pypdf2(input_path, output_path)
        
        else:  # auto or pypdf2
            return compress_pdf_pypdf2(input_path, output_path)
            
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_install_instructions():
    """Print installation instructions for required packages"""
    print("Install required packages:")
    print("pip install PyPDF2 PyMuPDF img2pdf pillow")
    print("For Ghostscript method, install Ghostscript from: https://www.ghostscript.com/")

# Main execution
if __name__ == "__main__":
    input_pdf = input("Enter input PDF path: ").strip().strip('"')
    output_pdf = input("Enter output PDF path: ").strip().strip('"')
    
    if not os.path.exists(input_pdf):
        print("Input file does not exist!")
        sys.exit(1)
    
    print("Choose compression method:")
    print("1. PyPDF2 (Basic)")
    print("2. Image conversion (Better for images)")
    print("3. Ghostscript (Professional, requires installation)")
    
    choice = input("Enter choice (1-3): ").strip()
    
    success = False
    if choice == '1':
        success = compress_pdf_pypdf2(input_pdf, output_pdf)
    elif choice == '2':
        success = compress_pdf_img2pdf(input_pdf, output_pdf)
    elif choice == '3':
        success = compress_pdf_advanced(input_pdf, output_pdf, method='ghostscript')
    else:
        print("Invalid choice! Using PyPDF2 method.")
        success = compress_pdf_pypdf2(input_pdf, output_pdf)
    
    if success:
        original_size = os.path.getsize(input_pdf)
        compressed_size = os.path.getsize(output_pdf)
        compression_ratio = compressed_size / original_size
        
        print(f"\nCompression completed successfully!")
        print(f"Original size: {original_size / 1024:.2f} KB")
        print(f"Compressed size: {compressed_size / 1024:.2f} KB")
        print(f"Compression ratio: {compression_ratio:.2%}")
        
        if compression_ratio > 0.4:
            print("Note: Compression ratio is higher than 1/3. You may want to:")
            print("- Use Ghostscript method if available")
            print("- Try lower quality settings for image-heavy PDFs")
    else:
        print("Compression failed!")
        get_install_instructions()