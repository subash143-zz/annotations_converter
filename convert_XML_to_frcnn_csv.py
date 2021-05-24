from xml.dom import minidom
import os
import glob
import csv


toDelete = []

def convert_xml2frcnnpytorch():
    # field names  
    fields = ['image_id', 'width', 'height', 'bbox', 'source']
    rows = []

    for fname in glob.glob("*.xml"):
        
        xmldoc = minidom.parse(fname)
        
        name = fname[:-4]
        for fil in glob.glob(f"{name}.*"):
            if not fil.endswith(".xml"):
                fname_out = fil.replace(".", "_")
                break
                

        itemlist = xmldoc.getElementsByTagName('object')
        size = xmldoc.getElementsByTagName('size')[0]
        width = int((size.getElementsByTagName('width')[0]).firstChild.data)
        height = int((size.getElementsByTagName('height')[0]).firstChild.data)

        for item in itemlist:
            # get class label
            classid =  (item.getElementsByTagName('name')[0]).firstChild.data
            # get bbox coordinates
            xmin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmin')[0]).firstChild.data
            ymin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymin')[0]).firstChild.data
            xmax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmax')[0]).firstChild.data
            ymax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymax')[0]).firstChild.data
            if float(xmax) - float(xmin) == 0 or float(ymax) - float(ymin) == 0:
            	print("Invalid width/height of annotation: ", fname_out)
            else:
            	rows.append([fname_out, width, height, "[" + str(xmin) +", "+ str(ymin) + ", " + str(float(xmax)-float(xmin)) + ", " + str(float(ymax)-float(ymin)) + "]", classid])

	
    # name of csv file  
    filename = "train.csv"
        
    # writing to csv file  
    with open(filename, 'w') as csvfile:  
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
            
        # writing the fields  
        csvwriter.writerow(fields)  
            
        # writing the data rows  
        csvwriter.writerows(rows) 

def main():
    convert_xml2frcnnpytorch()


if __name__ == '__main__':
    main()
