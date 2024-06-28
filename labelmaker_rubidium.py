#!/usr/bin/env python2

import sys
import os
import argparse
import tempfile
import subprocess
from fpdf import FPDF

defaultPrinter = 'DYMO-LabelManager-PnP'

def pdfOutput(filename, text, fontsize, font, style, border, height):
    pdf = FPDF('L', 'mm', 'A4')
    pdf.set_font(font, style, fontsize)
    textlength = pdf.get_string_width(text)
    textheight = fontsize*0.352778
    pdf.close()

    pagewidth = textlength+2*border

    pdf = FPDF('L', 'mm', (height, pagewidth))
    pdf.add_page()

    pdf.set_font(font, style, fontsize)
    pdf.text(border, textheight+2, text)

    pdf.output(filename, 'F')


def printOutput(printer, text, fontsize, font, style, border, height):
    f, filename = tempfile.mkstemp()
    os.close(f)

    pdfOutput(filename, text, fontsize, font, style, border, height)
    
    subprocess.call(['lpr', '-P{}'.format(printer), filename])

    os.remove(filename)


def parseCommandLine():
    parser = argparse.ArgumentParser(description='Print a label.')
    parser.add_argument('text', nargs='+')
    parser.add_argument('--width', '-w', help='Label width', type=int, default=9)
    parser.add_argument('--font', '-f', help='Text font', default='Times')
    parser.add_argument('--fontsize', '-s', help='Font size in pt', type=int, default=10)
    parser.add_argument('--fontstyle', '-t', help='Font style (B, I, U)', choices=['B', 'I', 'U', 'BI', 'BU', 'IU', 'BIU'], default='')
    parser.add_argument('--border', '-b', help='Border length', type=int, default=2)
    parser.add_argument('--printer', '-p', help='Printer name (as in -P for lpr)', default=defaultPrinter)
    parser.add_argument('--pdf', '-o', help='Output to PDF file')
    parser.parse_args()

    return parser.parse_args()

def main():
    args = parseCommandLine()

    if args.pdf:
        pdfOutput(args.pdf, ' '.join(args.text), args.fontsize, args.font, args.fontstyle, args.border, args.width)
    else:
        printOutput(args.printer, ' '.join(args.text), args.fontsize, args.font, args.fontstyle, args.border, args.width)


if __name__ == '__main__':
    main()