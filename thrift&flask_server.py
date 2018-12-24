import logging
logging.basicConfig(level=logging.DEBUG)
from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from hbase import Hbase

# Connect to HBase Thrift server
transport = TTransport.TBufferedTransport(TSocket.TSocket('192.168.1.154', 9090))
protocol = TBinaryProtocol.TBinaryProtocolAccelerated(transport)
 
# Create and open the client connection
client = Hbase.Client(protocol)


from flask import Flask,request,render_template
app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('home.html')
    
@app.route('/fetch1')
def fetch1():
    return render_template('fetch.html')
    
@app.route('/fetch',methods=['POST'])    
def fetch():
    transport.open()
    s1=int(request.form['start'])
    e1=int(request.form['end'])
    chno=request.form['chno']
    
    i=1
    k=1
    
    rowKeys=[]
    rowKeys1=[]
    rowKeys2=[]
    message={}
    message_bam={}
    
    for j in range(1,102747):
    	rowKeys.append(str(j))
    
    
  
    rows = client.getRows('Database', rowKeys,{})
    z=0
    for row in rows:
        if(z==0):
            z=z+1
            continue
        s2=int(row.columns.get("database:Start_Index").value)
        e2=int(row.columns.get("database:End_Index").value)
        c=row.columns.get("database:Chromosome_No").value
        if(c==chno):
        	if(s2<>e2):
        		if((s2<=s1 and e2>=e1) or (s2>=s1 and s2<=e1) or (s1<=e2 and s2<=e1)):
        			sums=0
        			no=0
        			for bam1 in range(52748,102748):
        			    rowKeys1.append(str(bam1))
        			rows1 = client.getRows('Database', rowKeys1,{})
        			for row1 in rows1:
        			    s3=int(row1.columns.get("database:Start_Index").value)
        			    e3=int(row1.columns.get("database:End_Index").value)
        			    c3=row1.columns.get("database:Chromosome_No").value
        			    if(c3==chno):
        			        if((s2<=s3) and (s3<=e2)):
        			            try:
        			                sums=sums+int(row1.columns.get("database:read_count").value)
        			                no=no+1
        			            except:
        			            	continue    
        			try:
        			    mean=sums/no            
        			except:
        			    mean=0
        			sums=0
        			no=0
        			for bam2 in range(102748,152777):
        			    rowKeys2.append(str(bam2))
        			rows2 = client.getRows('Database', rowKeys2,{})
        			for row2 in rows2:
        			    s4=int(row2.columns.get("database:Start_Index").value)
        			    e4=int(row2.columns.get("database:End_Index").value)
        			    c4=row2.columns.get("database:Chromosome_No").value
        			    if(c4==chno):
        			        if((s2<=s4) and (s4<=e2)):
        			            try:
        			                sums=sums+int(row2.columns.get("database:read_count").value)
        			                no=no+1
        			            except:
        			            	continue    
        			try:
        			    mean1=sums/no            
        			except:
        			    mean1=0    
        			message1=[]
        			message1.append(row.columns.get("database:ID").value)
        			message1.append(row.columns.get("database:Species").value)
        			message1.append(row.columns.get("database:Chromosome_No").value)
        			message1.append(row.columns.get("database:Start_Index").value)
        			message1.append(row.columns.get("database:End_Index").value)
        			message1.append(row.columns.get("database:Variant").value)
        			message1.append(row.columns.get("database:Gene").value)
        			message1.append(row.columns.get("database:Disease").value)
        			message1.append(row.columns.get("database:Method").value)
        			message1.append(mean)
        			message1.append(mean1)
       				message.update({str(i):message1})
       				i=i+1
       				
       		'''else:
       			if((s1<=s2) and (s2<=e1)):
       				message2=[]
        			message2.append(row.columns.get("database:Chromosome_No").value)
        			message2.append(row.columns.get("database:Start_Index").value)
        			message2.append(row.columns.get("database:End_Index").value)
        			message2.append(row.columns.get("database:read_count").value)
        			message2.append(row.columns.get("database:quantification").value)
       				message_bam.update({str(i):message2})
       				
       		                i=i+1
       	k=k+1	  '''              
    transport.close()   		
    return render_template('fetch1.html',s=s1,e=e1,c=chno,mes=message)

@app.route('/gene2')
def gene2():
	return render_template('gene2.html')
       
@app.route('/gene1',methods=['POST'])
def gene1():
    chno=request.form['chno']
    transport.open()
    rowKeys=[]
    message={}
    message1=[]
    message2=[]
    i=1
    z=0
    for j in range(1,52747):
    	rowKeys.append(str(j))
    rows = client.getRows('Database', rowKeys,{})
    for row in rows:
        if(z==0):
            z=z+1
            continue
            
        c=row.columns.get("database:Chromosome_No").value    
        try:
            
            g=row.columns.get("database:Gene").value
        except:
            continue 
        if(c==chno):
        	if(g in message2):
        		continue
        	message1.append(row.columns.get("database:Gene").value)
        	message2.append(row.columns.get("database:Gene").value)
        #message1.append(c)
        #message.update({str(i):message1})
        #i=i+1
    transport.close()
    message1.sort()
    return render_template('gene.html',mes=message1,chno=chno)  
  
@app.route('/gene',methods=['POST'])
def gene():
    transport.open()
    gene=request.form['gene']
    chno=request.form['chno']
    maxs=0
    
    i=1
    k=1
    
    rowKeys=[]
    message={}
    message_bam={}
    
    for j in range(1,102747):
    	rowKeys.append(str(j))
    
    
    rows = client.getRows('Database', rowKeys,{})
    z=0
    for row in rows:
        if(z==0):
            z=z+1
            continue
        s2=int(row.columns.get("database:Start_Index").value)
        e2=int(row.columns.get("database:End_Index").value)    
        c=row.columns.get("database:Chromosome_No").value    
        try:
            
            g=row.columns.get("database:Gene").value
        except:
            continue    
        if(gene==g and chno==c):
        	if(s2<>e2):
        	    if(i==1):
        	        mins=s2
        	    if(s2<mins):
        	        mins=s2
        	    if(e2>maxs):
        	        maxs=e2
        	    message1=[]
        	    message1.append(row.columns.get("database:ID").value)
        	    message1.append(row.columns.get("database:Species").value)
                    message1.append(row.columns.get("database:Chromosome_No").value)
        	    message1.append(row.columns.get("database:Start_Index").value)
        	    message1.append(row.columns.get("database:End_Index").value)
        	    message1.append(row.columns.get("database:Variant").value)
        	    message1.append(row.columns.get("database:Gene").value)
        	    message1.append(row.columns.get("database:Disease").value)
        	    message1.append(row.columns.get("database:Method").value)
       		    message.update({str(i):message1})
       		    i=i+1
       	k=k+1	                
    transport.close()   		
    return render_template('fetch2.html',mes=message,chno=chno,mins=mins,maxs=maxs)
    
@app.route('/disease1')
def disease1():
    return render_template('disease.html')  
  
@app.route('/disease',methods=['POST'])
def disease():
    transport.open()
    dis=request.form['chno']
    sel=request.form['gene']
    
    i=1
    k=1
    
    rowKeys=[]
    message={}
    message_bam={}
    
    for j in range(1,102747):
    	rowKeys.append(str(j))
    
    
    rows = client.getRows('Database', rowKeys,{})
    z=0
    if(sel=="region"):
    	for row in rows:
        	if(z==0):
                	z=z+1
                	continue
            	s2=int(row.columns.get("database:Start_Index").value)
            	e2=int(row.columns.get("database:End_Index").value)    
            	try:
                	d=row.columns.get("database:Disease").value
            	except:
                	continue    
            	if(dis==d):
        	    	if(s2<>e2):
        	        	message1=[]
        	        	message1.append(row.columns.get("database:ID").value)
        	        #message1.append(row.columns.get("database:Species").value)
                        	message1.append(row.columns.get("database:Chromosome_No").value)
        	        	message1.append(row.columns.get("database:Start_Index").value)
        	        	message1.append(row.columns.get("database:End_Index").value)
        	        #message1.append(row.columns.get("database:Variant").value)
        	        #message1.append(row.columns.get("database:Gene").value)
        	        	message1.append(row.columns.get("database:Disease").value)
        	        #message1.append(row.columns.get("database:Method").value)
       		        	message.update({str(i):message1})
       		        	i=i+1
    	transport.close()   		
    	return render_template('fetch3.html',mes=message)
    else:
    	for row in rows:
        	if(z==0):
                	z=z+1
                	continue
            	s2=int(row.columns.get("database:Start_Index").value)
            	e2=int(row.columns.get("database:End_Index").value)    
            	try:
                	d=row.columns.get("database:Disease").value
            	except:
                	continue    
            	if(dis==d):
        	    	if(s2<>e2):
        	        	message1=[]
        	        	message1.append(row.columns.get("database:ID").value)
        	        #message1.append(row.columns.get("database:Species").value)
                        	#message1.append(row.columns.get("database:Chromosome_No").value)
        	        	#message1.append(row.columns.get("database:Start_Index").value)
        	        	#message1.append(row.columns.get("database:End_Index").value)
        	        #message1.append(row.columns.get("database:Variant").value)
        	        	message1.append(row.columns.get("database:Gene").value)
        	        	message1.append(row.columns.get("database:Disease").value)
        	        #message1.append(row.columns.get("database:Method").value)
       		        	message.update({str(i):message1})
       		        	i=i+1
       		                
    	transport.close()   		
    	return render_template('fetch5.html',mes=message)

@app.route('/variant1')
def variant1():
    return render_template('variant.html')
   
@app.route('/variant',methods=['POST'])    
def variant():
    transport.open()
    var=request.form['var']
    chno=request.form['chno']
    i=1
    k=1
    
    rowKeys=[]
    message={}
    #message_bam={}
    
    for j in range(1,102747):
    	rowKeys.append(str(j))
    
    
    rows = client.getRows('Database', rowKeys,{})
    z=0
    for row in rows:
        if(z==0):
            z=z+1
            continue
        s2=int(row.columns.get("database:Start_Index").value)
        e2=int(row.columns.get("database:End_Index").value)    
        c=row.columns.get("database:Chromosome_No").value    
        try:
            
            v=row.columns.get("database:Variant").value
        except:
            continue    
        if(var==v and chno==c):
        	if(s2<>e2):
        	    
        	    message1=[]
        	    message1.append(row.columns.get("database:ID").value)
        	    message1.append(row.columns.get("database:Species").value)
                    message1.append(row.columns.get("database:Chromosome_No").value)
        	    message1.append(row.columns.get("database:Start_Index").value)
        	    message1.append(row.columns.get("database:End_Index").value)
        	    message1.append(row.columns.get("database:Variant").value)
        	    message1.append(row.columns.get("database:Gene").value)
        	    message1.append(row.columns.get("database:Disease").value)
        	    message1.append(row.columns.get("database:Method").value)
       		    message.update({str(i):message1})
       		    i=i+1
    transport.close()
    return render_template('fetch4.html',var=var,c=chno,mes=message)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)    

