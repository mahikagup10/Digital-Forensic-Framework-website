from flask import Flask, render_template, request, jsonify, redirect, url_for
import subprocess
import os

app = Flask(__name__)

mem_address = "" 


@app.route('/')
def choose_forensics():
    return render_template('index.html')
    

@app.route('/storage_forensics', methods=['GET', 'POST'])
def storage_forensics():
    if request.method == 'POST':
        #return redirect(url_for('storage_forensics'))
        return render_template('storage.html')
    return render_template('storage.html')

@app.route('/image_info', methods=['GET', 'POST'])
def disk_image_info():
    with open('file_address.txt', 'r') as file:
        storage_address = file.read().strip() 
    output = ""
    if request.method == 'POST':
        action = request.form.get('action')
        
        
        if action == 'img_stat':
            command = ["img_stat", storage_address]
            subprocess.run(command)
            try:
                # Execute img_stat command
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                # Wrap the output in <pre> tags and replace newlines with <br> tags
                output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
            except subprocess.CalledProcessError as e:
                return jsonify(error="An error occurred during img_stat execution.")
    return output  # Return the output as plain text
    

#def disk_image_info():
#    global mem_address
#    with open('file_address.txt', 'r') as file:
#        storage_address = file.read().strip()

    # Logic to retrieve disk image info
#    try:
#        command = ["img_stat", storage_address]
#        subprocess.run(command)
#        output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
#        disk_image_output = output.replace('\n', '<br>')  # Remove <pre> tags
#    except subprocess.CalledProcessError as e:
#        return jsonify(error="An error occurred during img_stat execution.")

#    return jsonify({'output': disk_image_output}) 

@app.route('/partition_info', methods=['POST'])
def disk_partition_info():
    global mem_address
    with open('file_address.txt', 'r') as file:
        storage_address = file.read().strip()

    # Logic to retrieve disk partition info
    try:
        command = ['mmls', storage_address]
        subprocess.run(command)
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
        partition_info_output = output.replace('\n', '<br>')  # Remove <pre> tags
    except subprocess.CalledProcessError as e:
        return jsonify(error="An error occurred during mmls execution.")

    return jsonify({'output': partition_info_output})
    
@app.route('/memory_forensics', methods=['GET', 'POST'])
def memory_forensics():
    return render_template('memory.html')
    
@app.route('/mem-printkey.html')
def mem_printkey():
    # Code to render mem-printkey.html template or perform actions
    return render_template('mem-printkey.html')


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


    
@app.route('/set_profile',methods=['POST'])
def set_profile():
	global profile
	profile = request.form['profile']
	return 'Profile Set Successfully'

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


@app.route('/execute', methods=['GET','POST'])
def execute():
    with open('file_address.txt', 'r') as file:
        storage_address = file.read().strip() 
    output = ""
    # This route will handle memory forensics tool actions
    if request.method == 'POST':
        # Add code here to process the memory forensics tool actions
        # You can use request.form to access form data
        # For example:
        action = request.form.get('action')
	
#    if action == 'img_stat':
#       # Compile and execute img_stat tool
#        command = ["img_stat",storage_address]
#        # Compile the C program if not already compiled
#        subprocess.run(command)

        # Replace '/path/to/your/image.dd' with the actual path to your forensic image file
#        try:
#            output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
            # Wrap the output in <pre> tags and replace newlines with <br> tags
#            output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
#        except subprocess.CalledProcessError as e:
            # Handle errors here, for example:
#            return jsonify(error="An error occurred during img_stat execution.")

    if action == 'mmls':
        # Compile and execute mmls tool
        command = ['mmls',storage_address]
        # Compile the C program if not already compiled
        subprocess.run(command)

        # Replace '/path/to/your/image.dd' with the actual path to your forensic image file
        try:
            #output = subprocess.check_output(['./mmls', '/home/mahika/Downloads/CapstoneFramework/Mantooth_raw.dd.raw'], stderr=subprocess.STDOUT, text=True)
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
            # Wrap the output in <pre> tags and replace newlines with <br> tags
            output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
        except subprocess.CalledProcessError as e:
            # Handle errors here, for example:
            return jsonify(error="An error occurred during mmls execution.")
            
    if action == 'fls':
        # Get the offset from the form data
        offset = request.form['offset']
        try:
            # Compile and execute fls tool
            command = ['fls',"-o",offset,"-r",storage_address]
            subprocess.run(command)
            # Replace '/path/to/your/image.dd' with the actual path to your forensic image file
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
            # Wrap the output in <pre> tags and replace newlines with <br> tags
            output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
        except subprocess.CalledProcessError as e:
            # Handle errors here, for example:
            #return e
            print(type(output))
            print(e)
            return jsonify(error="An error occurred during fls execution.")
            
    if action == 'fsstat':
        # Get the offset from the form data
        offset = request.form['offset']
  
        try:
            # Compile and execute fls tool
            command = ['fsstat',"-o",offset,storage_address]
            subprocess.run(command)
            # Replace '/path/to/your/image.dd' with the actual path to your forensic image file
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
            
            # Wrap the output in <pre> tags and replace newlines with <br> tags
            output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
        except subprocess.CalledProcessError as e:
            # Handle errors here, for example:
            return jsonify(error="An error occurred during fsstat execution.")
            
    if action == 'ils':
        # Get the offset from the form data
        offset = request.form['offset']
        try:
            # Compile and execute fls tool
            command = ['ils','-f','ntfs','-o',offset,storage_address]
            subprocess.run(command)
            # Replace '/path/to/your/image.dd' with the actual path to your forensic image file
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
            # Wrap the output in <pre> tags and replace newlines with <br> tags
            output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
        except subprocess.CalledProcessError as e:
            # Handle errors here, for example:
            #return e
            print(type(output))
            print(e)
            return jsonify(error="An error occurred during ils execution.")
            
    if action == 'jpeg_extract':
        # Get the offset from the form data
        folder = request.form['folder']
        try:
            os.makedirs(folder,exist_ok=True)
            # Compile and execute fls tool
            command = ["foremost","-t","jpeg","-i",storage_address,"-o",folder]
            #subprocess.run(command)
            # Replace '/path/to/your/image.dd' with the actual path to your forensic image file
            output = subprocess.run(command, stderr=subprocess.STDOUT, text=True)
            # Wrap the output in <pre> tags and replace newlines with <br> tags
            output = "output redirected to "+folder+" folder"
            output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
        except subprocess.CalledProcessError as e:
            # Handle errors here, for example:
            #return e
            print(type(output))
            print(e)
            return jsonify(error="An error occurred during jpegs execution.")
            
    if action == 'icat':
        # Get the offset from the form data
        offset = request.form['offset']
        inode = request.form['inode']
  
        try:
            # Compile and execute fls tool
            command = ['icat','-o',offset,storage_address,inode]
            subprocess.run(command)
            # Replace '/path/to/your/image.dd' with the actual path to your forensic image file
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
            
            # Wrap the output in <pre> tags and replace newlines with <br> tags
            output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
        except subprocess.CalledProcessError as e:
            # Handle errors here, for example:
            return jsonify(error="An error occurred during icat execution.")
            
    if action == 'istat':
        # Get the offset from the form data
        offset = request.form['offset']
        inode = request.form['inode']
  
        try:
            # Compile and execute fls tool
            command = ["istat","-o",offset,storage_address,inode]
            subprocess.run(command)
            # Replace '/path/to/your/image.dd' with the actual path to your forensic image file
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
            
            # Wrap the output in <pre> tags and replace newlines with <br> tags
            output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
        except subprocess.CalledProcessError as e:
            # Handle errors here, for example:
            return jsonify(error="An error occurred during istat execution.")

    if action == 'sorter':
        # Get the offset from the form data
        offset = request.form['offset']
        try:
            os.makedirs('sorted_files',exist_ok=True)
            # Compile and execute fls tool
            command = ["sorter","-o",offset,"-s","-d","sorted_files",storage_address]
            subprocess.run(command)
            # Replace '/path/to/your/image.dd' with the actual path to your forensic image file
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
            # Wrap the output in <pre> tags and replace newlines with <br> tags
            output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
        except subprocess.CalledProcessError as e:
            # Handle errors here, for example:
            #return e
            print(type(output))
            print(e)
            return jsonify(error="An error occurred during fls execution.")
    
    if action == 'stringsearch':
        searchString = request.form['searchString']
        offset = request.form['offset']

        try:
            # Compile and execute stringsearch tool
            command = f"blkls -o {offset} {storage_address} | strings -t d | grep {searchString}"
            #subprocess.run(command)
            #subprocess.run(command,shell=True,capture_output=True,text=True)

            # Execute the stringsearch program with offset and searchString as arguments
            #output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
            output = subprocess.run(command, shell=True, capture_output=True, text=True)

            # Wrap the output in <pre> tags and replace newlines with <br> tags
            #output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
            if output.returncode == 0:
            	output = '<pre>' + output.stdout.replace('\n','<br>') + '</pre>'
            else:
            	output = '<pre>' + output.stderr.replace('\n','<br>') + '</pre>'
        except subprocess.CalledProcessError as e:
            # Handle errors here, for example:
            return jsonify(error="An error occurred during stringsearch execution.")
            
    if action == 'recover':
        dire = request.form['dire']
        offset = request.form['offset']
        print(offset)

        try:
            # Compile and execute recover tool
            command = ['tsk_recover','-e','-o',offset,storage_address,dire]
            subprocess.run(command)

            # Execute the tsk_recover program with offset and file name as arguments
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
            output += "\nFiles recovered to "+dire+" folder"

            # Wrap the output in <pre> tags and replace newlines with <br> tags
            output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
        except subprocess.CalledProcessError as e:
            # Handle errors here, for example:
            return jsonify(error="An error occurred during recover execution.")
            
    if action == 'srch_strings':
        # Compile and execute srch_strings tool
        command = ['srch_strings',storage_address]
        # Compile the C program if not already compiled
        #subprocess.run(command)

        # Replace '/path/to/your/image.dd' with the actual path to your forensic image file
        try:
            #output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
            
            # Execute the command and capture the output
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=True)

            # Get the output
            output_text = result.stdout

            # Optionally, you can write the output to a file if needed
            with open('output.txt', 'w') as output_file:
            	output_file.write(output_text)
            # Wrap the output in <pre> tags and replace newlines with <br> tags
            output = "Output redirected to output.txt\n"
            output = '<pre>' + output.replace('\n', '<br>') + '</pre>'
            
        except subprocess.CalledProcessError as e:
            # Handle errors here, for example:
            return jsonify(error="An error occurred during srch_strings execution.")

    #print(type(output))
    return output

if __name__ == '__main__':
    app.run(debug=True)
