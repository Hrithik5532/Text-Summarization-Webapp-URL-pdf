import PyPDF2
# from .models import PDFModel
def pdf_text(pdf):
    pdfFileObj = open(f'./static/images/{pdf}', 'rb') 
    
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
    
    # creating a page object 
    pageObj = pdfReader.getPage(0) 
    print(pageObj.extractText())
    final_pdf = pageObj.extractText()
    pdfFileObj.close()

    return final_pdf 

# pdf = PDFModel.objects.all()[0]
pdf = pdf_text()
print(pdf)