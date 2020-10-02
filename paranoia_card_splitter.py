"""
This program extracts cards from the Paranoia rulebook PDF file.

Presumably I'm the only one using this, so I designed it to be used with iPython.

Created 8/2/2020 by Benjamin Velie.
veliebm@gmail.com

"""

from pathlib import Path
from PyPDF2 import PdfFileReader, PdfFileWriter
from copy import deepcopy


# Keeps track of how many cards we've printed
CARD_COUNTER = 0


def main(pdf_path):
    """
    Extracts cards from the Paranoia RPG rulebook.


    Parameters
    ----------
    pdf_path : str or Path
        Path to Paranoia rulebook pdf file.

    """

    pdf_path = Path(pdf_path)

    # Access our pages.
    pdf_reader = PdfFileReader(str(pdf_path))
    card_pages = [pdf_reader.getPage(i) for i in range(293, 332)]

    # Write the cards from each page.
    for page in card_pages:
        write_cards_from(page)

    return card_pages

def write_cards_from(page):
    """
    Given a PDF page containing paranoia cards, extracts the cards and writes them to disk.

    """

    # Track how many total cards have already been printed.
    global CARD_COUNTER

    # Extract cards from page.
    cards = extract_cards_from(page)

    for card in cards:
        
        # Write the cards to disk.
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(card)
        with Path(f"card_num-{CARD_COUNTER}.pdf").open(mode="wb") as output_file:
            pdf_writer.write(output_file)

        # Increment amount of cards we've printed.
        CARD_COUNTER += 1


def extract_cards_from(page):
    """
    Extracts cards from a page of the Paranoia rulebook.

    """

    # Height of each card should roughly be page height divided by 3.
    page_height = page.mediaBox.upperLeft[1]
    card_height = page_height / 3

    # We'll store cards here.
    card_pdfs = []

    for i in range(0, 3):
        
        # Deepcopy page so we don't accidentally edit it.
        page_copy = deepcopy(page)

        # Set the dimensions of the page corresponding to the card.
        card_bottom = card_height * i
        card_top = card_height * (i+1)
        page_copy.mediaBox.upperLeft = (0, card_top)
        page_copy.mediaBox.lowerLeft = (0, card_bottom)

        # Add the card to our list of cards.
        card_pdfs.append(page_copy)

    return card_pdfs
