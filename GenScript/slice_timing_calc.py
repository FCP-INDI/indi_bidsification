import sys, os

TR=2
sequence='seq+'
numslices=34
manufacturer='Siemens'
software='vb17'

sequence_list=['int+','int-','seq+','seq-']
manuf_list=['philips','siemens','ge']

manufacturer=manufacturer.lower()

def calculate_slice_times(TR,sequence,numslices):

    if sequence not in sequence_list:
        raise Exception('Sequence specified must be one of: '+'\n'.join(sequence_list))

    if manufacturer not in manuf_list:
        raise Exception('Manufacturer specified must be one of: '+'\n'.join(manuf_list))

    if manufacturer == 'siemens':

	    if sequence == 'seq+':
            slice_times=np.arange(0,TR,float(TR)/numslices)*1000

        elif sequence == 'seq-':
            slice_times=np.arange(0,TR,float(TR)/numslices)*1000
            slice_times=slice_times[::-1]
        
        elif sequence == 'int+' and (numslices % 2):
        	x=np.arange(0,TR,float(TR)/numslices)*1000
            y1=x[:(len(x)/2)+1]
            y2=x[(len(x)/2)+1:]
            slice_times=np.hstack([np.array([y1[i],y2[i]]) for i in range(0,len(x)/2)])
            slice_times=np.hstack(np.array((slice_times,y1[-1])))

        elif sequence == 'int+' and not (numslices % 2):
        	x=np.arange(0,TR,float(TR)/numslices)*1000
            slice_times=np.hstack([np.array([x[(len(x)/2):][i],x[:(len(x)/2)][i]]) for i in range(0,len(x)/2)])

        elif sequence == 'int-':
        	raise Exception('Siemens interleaved acquisition are always interleaved ascending')
