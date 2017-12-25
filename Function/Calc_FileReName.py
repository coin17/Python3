import shutil,os

path = 'C:\\Users\\Neil\\Desktop\\hourly-temperature'
for file in os.listdir(path):
    if os.path.isfile(os.path.join(path,file))==True:
        if file.find('.jpg') > 0:
        	folder = file[:8]
        	newpath = path + '\\' + folder
        	if not os.path.exists(newpath):
        		os.makedirs(newpath)

        	newname = file.replace(' ','').replace('_00.jpg','')+'_500hPa_ZT.png'
        	os.rename(os.path.join(path,file),os.path.join(path,newname))
        	shutil.move(os.path.join(path,newname),os.path.join(newpath,newname))   

            #os.rename(os.path.join(path,file),os.path.join(path,newname))
