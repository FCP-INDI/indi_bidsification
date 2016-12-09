from CPAC.AWS import aws_utils, fetch_creds
import tarfile
import os
import shutil

bucket = fetch_creds.return_bucket('/home/ubuntu/doconnor-fcp-indi-keys.csv', 'fcp-indi')


src_list=[]
for i,k in enumerate(bucket.list(prefix='data/Projects/ACPI/Outputs/')):
    src_list.append([str(k.name), k.size])




subids=sorted(set([sl[0].split('/')[5].split('-')[0] for sl in src_list]))
strats=sorted(set([sl[0].split('/')[4] for sl in src_list]))
strats=strats[3:]

stratdict={}
for strat in strats:
    stratdict[strat]={}
    subdict={}
    for subid in subids:
        subdict[subid]={}
        for i,src_file in enumerate(sorted(src_list)):
            if (subid in src_file[0]) and (strat in src_file[0]):
                nme=src_file[0]
                sze=src_file[1]
                propdict={}
                bits=str(nme).split('/')
                filename=bits[-1]
                propdict['name']=nme
                propdict['size']=sze
                subdict[subid].update({filename:propdict})
        stratdict[strat].update(subdict)

  
fo=open('tarlist.txt', 'w')
for strat in strats:
    tarlist=[]
    for subid in subids:
        print subid
        tarlist.append(subid)
        subsize_gb=0
        for subtar in tarlist:
            subsize_gb+=sum([stratdict[strat][subtar][f]['size'] for f in stratdict[strat][subtar].keys()])/(1024.**3)
        print subsize_gb
        if (subsize_gb >= 2.5) and (subsize_gb <= 3.2):
            
            filestopull=[stratdict[strat][sub][f]['name'] for sub in tarlist for f in stratdict[strat][sub].keys()]  
            while not os.path.isfile('./'+filestopull[-1].replace('data/Projects/ACPI/Outputs/','./')):
                try:
                    aws_utils.s3_download(bucket, filestopull, './', bucket_prefix='data/Projects/ACPI/Outputs/')
                except:
                    print "DL Falied, Trying Again"
            tarname=strat+'_'+tarlist[0]+'_'+tarlist[-1]
            print'Tarring', tarlist, tarname
            fo.write(tarname+'\n')
            tar = tarfile.open(tarname+'.tar.gz', 'w:gz')
            tar.add(strat+'/')
            tar.close()
            shutil.rmtree(strat)
            aws_utils.s3_upload(bucket,[tarname+'.tar.gz'], ['data/Projects/ACPI/OutputTars/'+tarname+'.tar.gz'])
            os.remove(tarname+'.tar.gz')
            tarlist=[]


        elif subsize_gb > 3.2:
            nextlist=[]
            print 'TOOBIG', tarlist, subsize_gb
            while subsize_gb > 3.2:
                nextlist.append(tarlist[-1])
                del tarlist[-1]
                subsize_gb=0
                for subtar in tarlist:
                     subsize_gb+=sum([stratdict[strat][subtar][f]['size'] for f in stratdict[strat][subtar].keys()])/(1024.**3)
                
            filestopull=[stratdict[strat][subt][f]['name'] for subt in tarlist for f in stratdict[strat][subt].keys()]
            while not os.path.isfile('./'+filestopull[-1].replace('data/Projects/ACPI/Outputs/','./')):
                try:
                    aws_utils.s3_download(bucket, filestopull, './', bucket_prefix='data/Projects/ACPI/Outputs/')
                except:
                    print "DL Falied, Trying Again"
            tarname=strat+'_'+tarlist[0]+'_'+tarlist[-1]
            print 'SMALLER', tarlist, tarname, subsize_gb
            fo.write(tarname+'\n')
            tar = tarfile.open(tarname+'.tar.gz', 'w:gz')
            tar.add(strat+'/')
            tar.close()
            shutil.rmtree(strat)
            aws_utils.s3_upload(bucket,[tarname+'.tar.gz'], ['data/Projects/ACPI/OutputTars/'+tarname+'.tar.gz'])
            os.remove(tarname+'.tar.gz')
            tarlist=nextlist

    subsize_gb=0
    for subtar in tarlist:
        subsize_gb+=sum([stratdict[strat][subtar][f]['size'] for f in stratdict[strat][subtar].keys()])/(1024.**3)
    print tarlist, subsize_gb

    if len(tarlist) > 0:
        filestopull=[stratdict[strat][subt][f]['name'] for subt in tarlist for f in stratdict[strat][subt].keys()]
        while not os.path.isfile('./'+filestopull[-1].replace('data/Projects/ACPI/Outputs/','./')):
            try:
                aws_utils.s3_download(bucket, filestopull, './', bucket_prefix='data/Projects/ACPI/Outputs/')
            except:
                print "DL Falied, Trying Again"
        tarname=strat+'_'+tarlist[0]+'_'+tarlist[-1]
        print 'Tarring', tarlist, tarname, subsize_gb
        fo.write(tarname+'\n')
        tar = tarfile.open(tarname+'.tar.gz', 'w:gz')
        tar.add(strat+'/')
        tar.close()
        shutil.rmtree(strat)
        aws_utils.s3_upload(bucket,[tarname+'.tar.gz'], ['data/Projects/ACPI/OutputTars/'+tarname+'.tar.gz'])
        os.remove(tarname+'.tar.gz')
        tarlist=[]

fo.close()
