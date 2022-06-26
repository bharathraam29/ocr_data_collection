import pandas as pd
import pytesseract
import cv2
import os.path

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def data_type_check(data,field):

    
    if(field in ['Plan No','Policy Number','Term / PPT']):
        try:
            data=int(data.replace(',', ''))
        except Exception as e:
            print(e)
        return data
    elif(field in ['Sum Assured','Premium Amt','Premium + GST','Commission']):
        try:
            if(field=='Commission'):
                data=data[3:]
            data=float(data.replace(',', ''))
            return data
        except Exception as e:
            print(e)
    elif (''.join(e for e in data if e.isalnum()).isalpha()):
        return data
    elif(field in ['Comm. Date','Maturity Date','FUP'] and ''.join(e for e in data if e.isalnum()).isalnum()) :
        return data
    else:
        return ""

def data_extract():
        
    img=cv2.imread('test.jpeg')
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    config = ('-l eng --oem 1 --psm 3')
    text = pytesseract.image_to_string(img, config=config)

    text = text.split('\n')
    text= list(filter(('').__ne__, text))
    data_fields=[
    'Plan No',
    'Plan Name',
    'Policy Number',
    'Nominee Name',
    'Sum Assured',
    'Premium Amt',
    'Premium + GST',
    'Payment Mode',
    'Comm. Date',
    'Term / PPT',
    'Maturity Date',
    'FUP',
    'Commission',
    'Name',
    ]
    result={}
    result[data_fields[-1]]=text[0]

    data_contents=text[len(data_fields):]
    data_contents.append(text[0])
    while(True):
        if(data_contents[2].replace(" ","").isalpha()):
            data_contents[1]=data_contents[1]+" "+data_contents[2]
            data_contents.pop(2)
        else:
            break
    k=0
    for i in range(0,len(data_fields)-1):
        res=data_type_check(data_contents[k],data_fields[i])
        if(res!=""):
            k+=1           
        result[data_fields[i]]=[res]
    return result
def export_to_csv(data_dict):
    df = pd.DataFrame(data_dict)
    if(os.path.exists('out.csv')):
        df.to_csv('out.csv',mode='a', index=False,header=False)
    else:
        df.to_csv('out.csv',mode='a', index=False,header=True)


if (__name__=='__main__'):
    export_to_csv(data_extract())
