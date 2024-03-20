from flask import Flask, request, abort, render_template
import json
import os

app = Flask(__name__)

applications = []
for dir in os.listdir('applications'):
    if os.path.exists(os.path.join('applications', dir, 'manifest.json')):
        with open(os.path.join('applications', dir, 'manifest.json')) as f:
            data = json.load(f)
        # Load the modules
        module = __import__(f'applications.{dir}.routes', fromlist=[dir])
        blueprint = getattr(module, data["blueprint"])
        app.jinja_loader.searchpath.append(os.path.join('applications', dir, 'templates'))
        app.register_blueprint(blueprint, url_prefix=f'/applications/{data["application"]}')
        
        # Load in applications for sidebar
        applications.append(data)
# Sort applications
applications = sorted(applications, key=lambda x: x['priority'])

# Dynamically load in backend applications
backendApplications = []
for dir in os.listdir('backendApplications'):
    if os.path.exists(os.path.join('backendApplications', dir, 'manifest.json')):
        with open(os.path.join('backendApplications', dir, 'manifest.json')) as f:
            data = json.load(f)
        # Load the modules
        module = __import__(f'backendApplications.{dir}.routes', fromlist=[dir])
        blueprint = getattr(module, data["blueprint"])
        app.jinja_loader.searchpath.append(os.path.join('backendApplications', dir, 'templates'))
        app.register_blueprint(blueprint, url_prefix=f'/backendApplications/{data["application"]}')

# Dynamically load in backend applications
backendProcesses = []
for dir in os.listdir('backendProcesses'):
    if os.path.exists(os.path.join('backendProcesses', dir, 'manifest.json')):
        with open(os.path.join('backendProcesses', dir, 'manifest.json')) as f:
            data = json.load(f)
        # Load the modules
        module = __import__(f'backendProcesses.{dir}.routes', fromlist=[dir])
        blueprint = getattr(module, data["blueprint"])
        app.jinja_loader.searchpath.append(os.path.join('backendProcesses', dir, 'templates'))
        app.register_blueprint(blueprint, url_prefix=f'/backendProcesses/{data["application"]}')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.context_processor
def inject_var():
    return dict(apps=applications)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test/')
def test():
    return render_template('test.html')

@app.route('/ping/')
def ping():
    return '', 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
