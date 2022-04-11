from django.shortcuts import render, redirect
from django.contrib import messages

from .Summarizer import summarizer, url_summarizer
import re
import time
from .forms import pdfForm
import PyPDF2
from .models import PDFModel

# Create your views here.
def pdf_text(pdf):
    pdfFileObj = open(f'./static/images/{pdf}', 'rb') 
    
    pdfreader = PyPDF2.PdfFileReader(pdfFileObj) 
    
    # creating a page object 
    x=pdfreader.numPages 
    pageObj=pdfreader.getPage(x-1)


    print(pageObj.extractText())
    final_pdf = pageObj.extractText()
    pdfFileObj.close()

    return final_pdf    

def index(request):
    context = {'flag':False, 'url_error':False, 'summarize_div':True,'pdfForm':pdfForm}


    if request.method == 'POST':

            # form = pdfForm(request.FILES)
        pdf = request.FILES.get('pdf') 
        if pdf:

                PDFModel.objects.create(pdf=pdf)
            
                pdf = PDFModel.objects.latest('date')
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                pdfText = pdf_text(f'{pdf.pdf}')

                if request.POST['num_lines']:
                        num_lines = request.POST['num_lines']
                else:
                    num_lines = 5
                start = time.time()
                summary = summarizer(pdfText, int(num_lines))
                end = time.time()
                context['time_taken'] = round(end-start, 2)
                context['flag'] = True
                context["content"] = pdfText
                context["summary"] = summary
                context['summarize_div'] = False
                return render(request, 'text_summarizer/index.html', context)
        else:
        
            if len(request.POST['textarea']) > 0 and len(request.POST['url_link']) > 0:
                messages.error(request, "Enter either URL or Text, not Both.")
                return redirect('index')
            
            if len(request.POST['textarea']) >0:
                if request.POST['num_lines']:
                    num_lines = request.POST['num_lines']
                else:
                    num_lines = 5
                content = request.POST['textarea']
                start = time.time()
                summary = summarizer(content, int(num_lines))
                end = time.time()
                context['time_taken'] = round(end-start, 2)
                context['flag'] = True
                context["content"] = content
                context["summary"] = summary
                context['summarize_div'] = False
                return render(request, 'text_summarizer/index.html', context)
            
            elif len(request.POST['url_link']) >0:
                if re.search("(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?", request.POST['url_link']) == None:
                    context['url_error'] = True
                    return render(request, 'text_summarizer/index.html', context)
                
                else:
                    if request.POST['num_lines']:
                        num_lines = request.POST['num_lines']
                    else:
                        num_lines = 5
                    try:
                        start = time.time()
                        content, summary = url_summarizer(request.POST['url_link'], int(num_lines))
                        end = time.time()
                        context['time_taken'] = round(end-start, 2)
                        context['flag'] = True
                        context["content"] = content
                        context["summary"] = summary
                        context['summarize_div'] = False
                        return render(request, 'text_summarizer/index.html', context)
                    except:
                        messages.error(request, "Entered URL doesnt contain any Data.")
                        return redirect('index')
            
            else:
                messages.error(request, "Enter URL or Text to summarize the content.")
                return redirect('index')
    return render(request, 'text_summarizer/index.html', context)