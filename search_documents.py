import PyPDF2
import os

TERMS = ['radar']
FOLDER = 'EOI-Documents/'


def check_terms(terms, page_content):
    terms_found = []
    for term in terms:
        if term in page_content:
            terms_found += [term]
    return terms_found


def get_blurbs(terms_found, page_content):
    blurbs = []
    for term in terms_found:
        index = page_content.index(term)
        start = max(0, index - 100)
        end = min(len(page_content) - 1, index + 100)
        blurb = page_content[start:end]
        blurb = blurb.replace(term, '***' + term.upper() + '***')
        blurbs += [blurb]
    return blurbs


def parsePDF(path, terms):
    with open(path, 'rb') as f:
        try:
            pdf = PyPDF2.PdfFileReader(f)
            for i in range(0, pdf.getNumPages()):
                content = pdf.getPage(i).extractText().lower()
                terms_found = check_terms(terms, content)
                if terms_found:
                    blurbs = get_blurbs(terms_found, content)
                    print('Terms found:', terms_found,
                          'in', path, 'on page', i + 1)
                    print('\n'.join(blurbs))
                    break
        except PyPDF2.utils.PdfReadError as e:
            print(e, path)


for file in os.listdir(FOLDER):
    if not file.endswith(".pdf"):
        continue
    parsePDF(FOLDER + file, TERMS)
