from website import create_app  #  This will take the folder website and use it as an python application 

app = create_app()

if __name__ == '__main__':  # This line will trigger the main application in this case Flask app. In the upper right corner there is a play button, which will run the web server with this code and the code written in the __init__.py file.
    app.run(debug=True)