from flask import Flask, render_template, request, jsonify, redirect, url_for
import subprocess
import os

app = Flask(__name__)
mem_address = "" 


@app.route('/', methods=['GET', 'POST'])
def choose_forensics():
    return render_template('index.html')
    

@app.route('/storage_forensics', methods=['GET', 'POST'])
def storage_forensics():
    return render_template('storage.html')
    
    
@app.route('/storage_upload',methods=['POST'])	
def upload_file():
	global fileaddress
	uploaded_file = request.files['file']
	if uploaded_file.filename != '':
		upload_dir = 'Image'
		os.makedirs(upload_dir, exist_ok=True)
		file_address = os.path.join(upload_dir,uploaded_file.filename)
		fileaddress = file_address
		uploaded_file.save(file_address)
		with open('file_address.txt','w') as file:
			file.write(file_address)
			return 'File uploaded successfully!'
	else:
		return 'No file selected'


@app.route('/storage-imgstat', methods=['GET', 'POST'])
def image_info():
    with open('file_address.txt', 'r') as file:
        storage_address = file.read().strip() 
    output = ""
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'img_stat':
            command = ["img_stat", storage_address]
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return  output
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during img_stat execution.")
    return render_template('storage.html', output=output)
    

@app.route('/storage-mmls', methods=['GET', 'POST'])
def partition_info():
    with open('file_address.txt', 'r') as file:
        storage_address = file.read().strip()
    output = ""
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'mmls':
            command = ["mmls", storage_address]
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return output
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during mmls execution.")
    return render_template('storage.html', output=output)
    
@app.route('/strg-fls',methods=['POST'])
def strg_fls():
    with open('file_address.txt', 'r') as file:
        storage_address = file.read().strip() 
    output = ""
    
    if request.method == 'POST':
        action = request.form.get('action')
	
        if action == 'fls':
            offset = request.form['offset']
            command = ['fls',"-o",offset,"-r",storage_address]
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during fls execution.")
    return output
    
@app.route('/strg-fsstat',methods=['POST'])
def strg_fsstat():
    with open('file_address.txt', 'r') as file:
        storage_address = file.read().strip() 
    output = ""
    
    if request.method == 'POST':
        action = request.form.get('action')
	
        if action == 'fsstat':
            offset = request.form['offset']
            command = ['fsstat',"-o",offset,storage_address]
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during fsstat execution.")
    return output
    
@app.route('/strg-ils',methods=['POST'])
def strg_ils():
    with open('file_address.txt', 'r') as file:
        storage_address = file.read().strip() 
    output = ""
    
    if request.method == 'POST':
        action = request.form.get('action')
	
        if action == 'ils':
            offset = request.form['offset']
            command = ['ils','-f','ntfs','-o',offset,storage_address]
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during ils execution.")
    return output
    
@app.route('/strg-jpeg_extract',methods=['POST'])
def strg_jpeg_extract():
    with open('file_address.txt', 'r') as file:
        storage_address = file.read().strip() 
    output = ""
    
    if request.method == 'POST':
        action = request.form.get('action')
	
        if action == 'jpeg_extract':
            folder = request.form['folder']
            os.makedirs(folder,exist_ok=True)
            command = ["foremost","-t","jpeg","-i",storage_address,"-o",folder]
            try:
                output = subprocess.run(command, stderr=subprocess.STDOUT, text=True)
                output = "output redirected to "+folder+" folder"
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during jpeg_extract execution.")
    return output
    
@app.route('/strg-icat',methods=['POST'])
def strg_icat():
    with open('file_address.txt', 'r') as file:
        storage_address = file.read().strip() 
    output = ""
    
    if request.method == 'POST':
        action = request.form.get('action')
	
        if action == 'icat':
            offset = request.form['offset']
            inode = request.form['inode']
            command = ['icat','-o',offset,storage_address,inode]
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during icat execution.")
    return output
    
@app.route('/strg-istat',methods=['POST'])
def strg_istat():
    with open('file_address.txt', 'r') as file:
        storage_address = file.read().strip() 
    output = ""
    
    if request.method == 'POST':
        action = request.form.get('action')
	
        if action == 'istat':
            offset = request.form['offset']
            inode = request.form['inode']
            command = ["istat","-o",offset,storage_address,inode]
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during icat execution.")
    return output
    
@app.route('/strg-sorter',methods=['POST'])
def strg_sorter():
    with open('file_address.txt', 'r') as file:
        storage_address = file.read().strip() 
    output = ""
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'sorter':
            offset = request.form['offset']
            os.makedirs('sorted_files',exist_ok=True)
            command = ["sorter","-o",offset,"-s","-d","sorted_files",storage_address]
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during icat execution.")
    return output
    
@app.route('/strg-stringsearch',methods=['POST'])
def strg_stringsearch():
    with open('file_address.txt', 'r') as file:
        storage_address = file.read().strip() 
    output = ""
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'stringsearch':
            searchString = request.form['searchString']
            offset = request.form['offset']
            command = f"blkls -o {offset} {storage_address} | strings -t d | grep {searchString}"
            try:
                output = subprocess.run(command, shell=True, capture_output=True, text=True)
                if output.returncode == 0:
            	    output = '<pre>' + output.stdout.replace('\n','<br>') + '</pre>'
                else:
            	    output = '<pre>' + output.stderr.replace('\n','<br>') + '</pre>'
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during stringsearch execution.")
    return output   
    
@app.route('/strg-recover',methods=['POST'])
def strg_recover():
    with open('file_address.txt', 'r') as file:
        storage_address = file.read().strip() 
    output = ""
    
    if request.method == 'POST':
        action = request.form.get('action')        

        if action == 'recover':
            dire = request.form['dire']
            offset = request.form['offset']
            print(offset)
            command = ['tsk_recover','-e','-o',offset,storage_address,dire]
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                output += "\nFiles recovered to "+dire+" folder"
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during recover execution.")
    return output
    
    
@app.route('/storage-fls.html')
def storage_fls():
	return render_template('storage-fls.html')
	
@app.route('/storage-fsstat.html')
def storage_fsstat():
	return render_template('storage-fsstat.html')
	
@app.route('/storage-ils.html')
def storage_ils():
	return render_template('storage-ils.html')
	
@app.route('/storage-jpegextract.html')
def storage_jpegextract():
	return render_template('storage-jpegextract.html')
	
@app.route('/storage-icat.html')
def storage_icat():
	return render_template('storage-icat.html')
	
@app.route('/storage-istat.html')
def storage_istat():
	return render_template('storage-istat.html')
	
@app.route('/storage-sorter.html')
def storage_sorter():
	return render_template('storage-sorter.html')
	
@app.route('/storage-stringsearch.html')
def storage_stringsearch():
	return render_template('storage-stringsearch.html')
	
@app.route('/storage-tskrecover.html')
def storage_recover():
	return render_template('storage-tskrecover.html')    

    
@app.route('/memory_forensics', methods=['GET', 'POST'])
def memory_forensics():
    return render_template('memory.html')
    
@app.route('/install_dependencies', methods=['POST'])
def install_dependencies():
    try:
        commands = [
            "wget https://bootstrap.pypa.io/pip/2.7/get-pip.py",
            "sudo python2 get-pip.py",
            "pip2 install --upgrade setuptools",
            "sudo apt-get install python2-dev",
            "pip2 install pycrypto",
            "pip2 install distorm3",
            "git clone https://github.com/volatilityfoundation/volatility.git /opt/volatility"
        ]

        for command in commands:
            try:
                subprocess.run(command.split(), check=True)
            except subprocess.CalledProcessError as e:
                if 'destination path' in str(e.output):
                    continue
                else:
                    return jsonify({'message': f'Error during installation: {e}'})
        
        return jsonify({'message': 'Dependencies installed successfully'})
    except Exception as e:
        return jsonify({'message': f'Error during installation: {e}'}), 500


@app.route('/memory_upload',methods=['POST'])	
def upload_dump():
	global mem_address
	uploaded_file = request.files['file']
	if uploaded_file.filename != '':
		upload_dir = 'Image'
		os.makedirs(upload_dir, exist_ok=True)
		mem_address = os.path.join(upload_dir,uploaded_file.filename)
		uploaded_file.save(mem_address)
		with open('mem_address.txt','w') as file:
			file.write(mem_address)
			return 'Memory dump uploaded successfully!'
	else:
		return 'No file selected'


@app.route('/mem-image-info', methods=['POST'])
def mem_imageinfo():
    global mem_address
    with open('mem_address.txt', 'r') as file:
        mem_address = file.read().strip() 
    output = ""
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'memimageinfo':
            command = ["python2", "/opt/volatility/vol.py", "-f", mem_address, "imageinfo"]
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return output
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during imageinfo execution.")
    return render_template('memory.html', output=output)


    
@app.route('/set_profile',methods=['POST'])
def set_profile():
	global profile
	profile = request.form['profile']
	return 'Profile Set Successfully'
	
	
    
@app.route('/mem-printkey.html')
def mem_printkey():
    return render_template('mem-printkey.html')

@app.route('/mem-psxview.html')
def mem_psxview():
	return render_template('mem-psxview.html')
	
@app.route('/mem-netscan.html')
def mem_netscan():
	return render_template('mem-netscan.html')

@app.route('/mem-cmdline.html')
def mem_cmdline():
	return render_template('mem-cmdline.html')

@app.route('/mem-pslist.html')
def mem_pslist():
	return render_template('mem-pslist.html')

@app.route('/mem-hashdump-crackpass.html')
def mem_hashdump_crackpass():
	return render_template('mem-hashdump-crackpass.html')




@app.route('/memory_tools', methods=['GET', 'POST'])
def memory_tools():
    global mem_address
    with open('mem_address.txt', 'r') as file:
        mem_address = file.read().strip() 
    output = ""
    # This route will handle memory forensics tool actions
    if request.method == 'POST':
        # Add code here to process the memory forensics tool actions
        # You can use request.form to access form data
        # For example:
        action = request.form.get('action')

        if action == 'memimageinfo':
            # Logic to handle 'memimageinfo' action
            command = ["python2", "/opt/volatility/volatility/vol.py", "-f", mem_address, "imageinfo"]
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                # Wrap the output in <pre> tags and replace newlines with <br> tags
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return output
            except subprocess.CalledProcessError as e:
                # Handle errors here, for example:
                return jsonify(error="An error occurred during imageinfo execution.")

        if action == 'printkey':
            # Logic to handle 'printkey' action (displaying registry keys)
            # profile = request.form.get('profile')
            # Add logic to display registry keys using the provided profile
            command = ['python2', '/opt/volatility/volatility/vol.py', '-f', mem_address, '--profile='+profile,'printkey']
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                # Wrap the output in <pre> tags and replace newlines with <br> tags
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return output
            except subprocess.CalledProcessError as e:
                # Handle errors here, for example:
                print(e.cmd, e.output)
                return jsonify(error="An error occurred during printkey execution.")

        if action == 'netscan':
            command = ['python2', '/opt/volatility/volatility/vol.py', '-f', mem_address, '--profile='+profile,'netscan']
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                # Wrap the output in <pre> tags and replace newlines with <br> tags
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return output
            except subprocess.CalledProcessError as e:
                # Handle errors here, for example:
                print(e.cmd, e.output)
                return jsonify(error="An error occurred during netscan execution.")
                
        if action == 'pslist':
            command = ['python2', '/opt/volatility/volatility/vol.py', '-f', mem_address, '--profile='+profile,'pslist']
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                # Wrap the output in <pre> tags and replace newlines with <br> tags
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return output
            except subprocess.CalledProcessError as e:
                # Handle errors here, for example:
                print(e.cmd, e.output)
                return jsonify(error="An error occurred during pslist execution.")
                
        if action == 'psxview':
            command = ['python2', '/opt/volatility/volatility/vol.py', '-f', mem_address, '--profile='+profile,'psxview']
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                # Wrap the output in <pre> tags and replace newlines with <br> tags
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return output
            except subprocess.CalledProcessError as e:
                # Handle errors here, for example:
                print(e.cmd, e.output)
                return jsonify(error="An error occurred during psxview execution.")
        
        if action == 'hashdump':
            command = ['python2', '/opt/volatility/volatility/vol.py', '-f', mem_address, '--profile='+profile, 'hashdump']
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                # Wrap the output in <pre> tags and replace newlines with <br> tags
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return output
            except subprocess.CalledProcessError as e:
                # Handle errors here, for example:
                print(e.cmd, e.output)
                return jsonify(error="An error occurred during psxview execution.")
               
        if action == 'crackpassword':
            hash_value = request.form['hash_value']  # Get the hash value from the form
            with open('hash.txt', 'w') as hash_file:
                hash_file.write(hash_value)
            command = ['hashcat', '-m', '1000', '-a', '0', 'hash.txt', 'rockyou.txt']
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
        # Wrap the output in <pre> tags and replace newlines with <br> tags
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return output
            except subprocess.CalledProcessError as e:
        # Handle errors here, for example:
                print(e.cmd, e.output)
            return jsonify(error="An error occurred during hashcat execution.")
        
        if action == 'cmdline':
            command = ['python2', '/opt/volatility/volatility/vol.py', '-f', mem_address, '--profile='+profile,'cmdscan']
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                # Wrap the output in <pre> tags and replace newlines with <br> tags
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return output
            except subprocess.CalledProcessError as e:
                print(e.cmd, e.output)
                return jsonify(error="An error occurred during cmdline execution.")                
               
    # Return the appropriate response or render the necessary template
    return render_template('memory.html', output=output)  # Rendering the memory tools page
    
    
    



@app.route('/execute', methods=['GET','POST'])
def execute():
    with open('file_address.txt', 'r') as file:
        storage_address = file.read().strip() 
    output = ""
    if request.method == 'POST':
        action = request.form.get('action')
            
        if action == 'srch_strings':
            command = ['srch_strings',storage_address]
            try:
                result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=True)
                output_text = result.stdout
                with open('output.txt', 'w') as output_file:
            	    output_file.write(output_text)
                output = "Output redirected to output.txt\n"
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during srch_strings execution.")
    return output

if __name__ == '__main__':
    app.run(debug=True)
