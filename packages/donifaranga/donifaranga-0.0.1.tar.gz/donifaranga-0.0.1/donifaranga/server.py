#-----------------------------------------
# LIBRARIES
#-----------------------------------------

from flask import Flask, jsonify
from routes import api_bp
import config as cf

#-----------------------------------------
# INIT
#-----------------------------------------

app = Flask(__name__)

app.register_blueprint(api_bp)


#-----------------------------------------
# ERROR HANDLING
#-----------------------------------------

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found", "error_message": str(error), 'lang':cf.supported_languages}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal Server Error", "error_message": "An unexpected error occurred.",'lang':cf.supported_languages}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    # You can also log the exception here
    return jsonify({"error": "Internal Server Error", "error_message": str(e),'lang':cf.supported_languages}), 500


#-----------------------------------------
# RUN
#-----------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
