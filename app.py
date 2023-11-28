from flask import Flask, render_template, request, jsonify, redirect, url_for
import subprocess
import os

app = Flask(__name__)

mem_address = "" 
profile= ""


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
            #subprocess.run(command)
            try:
                # Execute img_stat command
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                # Wrap the output in <pre> tags and replace newlines with <br> tags
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
    # Logic to retrieve disk partition info
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return output
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during mmls execution.")
    return render_template('storage.html', output=output)
    
    
@app.route('/storage-fls.html', methods=['GET', 'POST'])
def storage_fls():
    with open('file_address.txt', 'r') as file:
        storage_address = file.read().strip()
    output = ""
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'fls':
            offset = request.form['offset']
            command = ['fls',"-o",offset,"-r",storage_address]
    # Logic to retrieve disk partition info
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return output
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during fls execution.")
    return render_template('storage-fls.html', output=output)
	
@app.route('/storage-fsstat.html', methods=['GET', 'POST'])
def storage_fsstat():
    with open('file_address.txt', 'r') as file:
        storage_address = file.read().strip()
    output = ""
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'fsstat':
            offset = request.form['offset']
            command = ['fsstat',"-o",offset,storage_address]
    # Logic to retrieve disk partition info
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return output
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during fsstat execution.")
    return render_template('storage-fsstat.html', output=output)
	
@app.route('/storage-ils.html', methods=['GET', 'POST'])
def storage_ils():
    with open('file_address.txt', 'r') as file:
        storage_address = file.read().strip()
    output = ""
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'ils':
            offset = request.form['offset']
            command = ['ils','-f','ntfs','-o',offset,storage_address]
    # Logic to retrieve disk partition info
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return output
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during ils execution.")
    return render_template('storage-ils.html', output=output)
	
@app.route('/storage-jpegextract.html', methods=['GET', 'POST'])
def storage_jpegextract():
    with open('file_address.txt', 'r') as file:
        storage_address = file.read().strip()
    output = ""
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'jpeg_extract':
            folder = request.form['folder']
            os.makedirs(folder,exist_ok=True)
            command = ["foremost","-t","jpeg","-i",storage_address,"-o",folder]
    # Logic to retrieve disk partition info
            try:
                output = subprocess.run(command, stderr=subprocess.STDOUT, text=True)
                output = "output redirected to "+folder+" folder"
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return output
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during jpeg extract execution.")
    return render_template('storage-jpegextract.html', output=output)
	
@app.route('/storage-icat.html', methods=['GET', 'POST'])
def storage_icat():
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
                return output
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during icat execution.")
    return render_template('storage-icat.html', output=output)
	
@app.route('/storage-istat.html', methods=['GET', 'POST'])
def storage_istat():
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
                return output
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during istat execution.")
    return render_template('storage-istat.html', output=output)
	
@app.route('/storage-sorter.html', methods=['GET', 'POST'])
def storage_sorter():
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
                return output
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during sorter execution.")
    return render_template('storage-sorter.html', output=output)
	
@app.route('/storage-stringsearch.html', methods=['GET', 'POST'])
def storage_stringsearch():
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
                return output
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during stringsearch execution.")
    return render_template('storage-stringsearch.html', output=output)
	
@app.route('/storage-tskrecover.html', methods=['GET', 'POST'])
def storage_recover():
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
                return output
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during recover execution.")
    return render_template('storage-tskrecover.html', output=output)    

    
@app.route('/memory_forensics', methods=['GET', 'POST'])
def memory_forensics():
    return render_template('memory.html')
    
@app.route('/install_dependencies', methods=['POST'])
def install_dependencies():
    try:
        # Your installation script commands
        commands = [
            "wget https://bootstrap.pypa.io/pip/2.7/get-pip.py",
            "sudo python2 get-pip.py",
            "pip2 install --upgrade setuptools",
            "sudo apt-get install python2-dev",
            "pip2 install pycrypto",
            "pip2 install distorm3",
            "git clone https://github.com/volatilityfoundation/volatility.git /opt/volatility"
        ]

        # Run the installation commands one by one
        for command in commands:
            try:
                subprocess.run(command.split(), check=True)
            except subprocess.CalledProcessError as e:
                # Handle Git Clone Error
                if 'destination path' in str(e.output):
                    continue  # Skip if 'destination path' error
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
		#memaddress=mem_address
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
            # Logic to handle 'memimageinfo' action
            command = ["python2", "/opt/volatility/vol.py", "-f", mem_address, "imageinfo"]
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                # Wrap the output in <pre> tags and replace newlines with <br> tags
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return output
            except subprocess.CalledProcessError as e:
                # Handle errors here, for example:
                return jsonify(error="An error occurred during imageinfo execution.")
    return render_template('memory.html', output=output)


    
@app.route('/set_profile',methods=['POST'])
def set_profile():
	global profile
	profile = request.form['profile']
	print(profile)
	return 'Profile Set Successfully'
	
	
    
@app.route('/mem-printkey.html', methods=['GET', 'POST'])
def mem_printkey():
    global mem_address
    with open('mem_address.txt', 'r') as file:
        mem_address = file.read().strip() 
    output = ""
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'printkey':
            # Logic to handle 'memimageinfo' action
            print("i am printing profile in printkey:",profile)
            command = ['python2', '/opt/volatility/vol.py', '-f', mem_address, '--profile='+profile,'printkey']
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                # Wrap the output in <pre> tags and replace newlines with <br> tags
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return output
            except subprocess.CalledProcessError as e:
                # Handle errors here, for example:
                return jsonify(error="An error occurred during printkey execution.")
    # Code to render mem-printkey.html template or perform actions
    return render_template('mem-printkey.html', output=output)
    
@app.route('/mem-netscan.html', methods=['GET', 'POST'])
def mem_netscan():
    global mem_address
    with open('mem_address.txt', 'r') as file:
        mem_address = file.read().strip() 
    output = ""
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'netscan':
            # Logic to handle 'memimageinfo' action
            print("i am printing profile in printkey:",profile)
            command = ['python2', '/opt/volatility/vol.py', '-f', mem_address, '--profile='+profile,'netscan']
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                # Wrap the output in <pre> tags and replace newlines with <br> tags
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return output
            except subprocess.CalledProcessError as e:
                # Handle errors here, for example:
                return jsonify(error="An error occurred during netscan execution.")
    # Code to render mem-printkey.html template or perform actions
    return render_template('mem-netscan.html', output=output)


@app.route('/mem-pslist.html', methods=['GET', 'POST'])
def mem_pslist():
    global mem_address
    with open('mem_address.txt', 'r') as file:
        mem_address = file.read().strip() 
    output = ""
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'pslist':
            # Logic to handle 'memimageinfo' action
            print("i am printing profile in printkey:",profile)
            command = ['python2', '/opt/volatility/vol.py', '-f', mem_address, '--profile='+profile,'pslist']
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                # Wrap the output in <pre> tags and replace newlines with <br> tags
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return output
            except subprocess.CalledProcessError as e:
                # Handle errors here, for example:
                return jsonify(error="An error occurred during pslist execution.")
    # Code to render mem-printkey.html template or perform actions
    return render_template('mem-pslist.html', output=output)


@app.route('/mem-psxview.html', methods=['GET', 'POST'])
def mem_psxview():
    global mem_address
    with open('mem_address.txt', 'r') as file:
        mem_address = file.read().strip() 
    output = ""
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'psxview':
            print("i am printing profile in printkey:",profile)
            command = ['python2', '/opt/volatility/vol.py', '-f', mem_address, '--profile='+profile,'psxview']
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                # Wrap the output in <pre> tags and replace newlines with <br> tags
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return output
            except subprocess.CalledProcessError as e:
                # Handle errors here, for example:
                return jsonify(error="An error occurred during pslist execution.")
    # Code to render mem-printkey.html template or perform actions
    return render_template('mem-psxview.html', output=output)

	

@app.route('/mem-cmdline.html', methods=['GET', 'POST'])
def mem_cmdline():
    global mem_address
    with open('mem_address.txt', 'r') as file:
        mem_address = file.read().strip() 
    output = ""
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'cmdline':
            print("i am printing profile in printkey:",profile)
            command = ['python2', '/opt/volatility/vol.py', '-f', mem_address, '--profile='+profile,'cmdscan']
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                # Wrap the output in <pre> tags and replace newlines with <br> tags
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return output
            except subprocess.CalledProcessError as e:
                # Handle errors here, for example:
                return jsonify(error="An error occurred during cmdscan execution.")
    # Code to render mem-printkey.html template or perform actions
    return render_template('mem-cmdline.html', output=output)
    

@app.route('/mem-hashdump-crackpass.html', methods=['GET', 'POST'])
def mem_hashdump_crackpass():
    return render_template('mem-hashdump-crackpass.html')

@app.route('/mem-hashdump.html', methods=['GET', 'POST'])
def mem_hashdump():
    global mem_address
    with open('mem_address.txt', 'r') as file:
        mem_address = file.read().strip() 
    output = ""
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'hashdump':
            print("i am printing profile in printkey:",profile)
            command = ['python2', '/opt/volatility/vol.py', '-f', mem_address, '--profile='+profile, 'hashdump']
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                # Wrap the output in <pre> tags and replace newlines with <br> tags
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return output
            except subprocess.CalledProcessError as e:
                # Handle errors here, for example:
                return jsonify(error="An error occurred during hashdump execution.")
    # Code to render mem-printkey.html template or perform actions
    return render_template('mem-hashdump-crackpass.html', output=output)


@app.route('/mem-crackpass.html', methods=['GET', 'POST'])
def mem_crackpass():
    global mem_address
    with open('mem_address.txt', 'r') as file:
        mem_address = file.read().strip() 
    output = ""
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'crackpassword':
            print("i am printing profile in printkey:",profile)
            hash_value = request.form['hash_value']  # Get the hash value from the form
            with open('hash.txt', 'w') as hash_file:
                hash_file.write(hash_value)
            command = ['hashcat', '-m', '1000', '-a', '0', 'hash.txt', 'rockyou.txt', '--show']
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                # Wrap the output in <pre> tags and replace newlines with <br> tags
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
                return output
            except subprocess.CalledProcessError as e:
                # Handle errors here, for example:
                return jsonify(error="An error occurred during hashcat execution.")
    # Code to render mem-printkey.html template or perform actions
    return render_template('mem-hashdump-crackpass.html', output=output)




if __name__ == '__main__':
    app.run(debug=True)
