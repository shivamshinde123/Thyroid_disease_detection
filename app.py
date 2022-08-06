
from flask import Flask, render_template, request
import os
from src.prediction_methods import form_response

webapp_root = 'webpage'
static_folder_path = os.path.join(webapp_root, 'static')
template_folder_path = os.path.join(webapp_root,'templates')

app = Flask(__name__, static_folder=static_folder_path, template_folder=template_folder_path)


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        try:
            if request.form:
                # getting the data which was entered by the user using the html form
                data = request.form

                # converting the data from the html page into the dictionary format
                data = dict(data)

                ## providing the dictionary format data to the form_response method
                prediction = form_response(data)
                return render_template('index.html',prediction=prediction)
        except Exception as e:
            print(e)
            return render_template('404.html',error=e)

    else:
        return render_template('index.html')

@app.route('/metadata',methods=['POST','GET'])
def info():
    return render_template('info.html')


if __name__ == '__main__':
        app.run(debug=True)