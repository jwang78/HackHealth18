from flask import Flask
from flask import request
import json

app = Flask(__name__)
"""
@app.route("/")
def hello():
    return "Hello World!"
"""

userbase = {}

screenbank = {}
screenbank["depression"] = {'questions': [{'q': '1. Little interest or pleasure in doing things', 'a': ['Not at all', 'Several days', 'More than half the days', 'Nearly every day']}, {'q': '2. Feeling down, depressed, or hopeless', 'a': ['Not at all', 'Several days', 'More than half the days', 'Nearly every day']}, {'q': '3. Trouble falling or staying asleep, or sleeping too much', 'a': ['Not at all', 'Several days', 'More than half the days', 'Nearly every day']}, {'q': '4. Feeling tired or having little energy', 'a': ['Not at all', 'Several days', 'More than half the days', 'Nearly every day']}, {'q': '5. Poor appetite or overeating', 'a': ['Not at all', 'Several days', 'More than half the days', 'Nearly every day']}, {'q': '6. Feeling bad about yourself - or that you are a failure or have let yourself or your family down', 'a': ['Not at all', 'Several days', 'More than half the days', 'Nearly every day']}, {'q': '7. Trouble concentrating on things, such as reading the newspaper or watching television', 'a': ['Not at all', 'Several days', 'More than half the days', 'Nearly every day']}, {'q': '8. Moving or speaking so slowly that other people could have noticed', 'a': ['Not at all', 'Several days', 'More than half the days', 'Nearly every day']}, {'q': '9. Thoughts that you would be better off dead, or of hurting yourself', 'a': ['Not at all', 'Several days', 'More than half the days', 'Nearly every day']}, {'q': '10. If you checked off any problems, how difficult have these problems made it for you at work, home, or with other people?', 'a': ['Not difficult at all', 'Somewhat difficult', 'Very difficult', 'Extremely difficult']}], 'instructions': 'Over the past two weeks, how often have you been bothered by the following problems?'}

def evaluate(screen, responses, user):
    if screen == "depression":
        flag = False
        if answers[responses[8]] > 0:
            flag = True
        answers = {'Not at all': 0, 'Several days': 1, 'More than half the days': 2, 'Nearly every day': 3}
        total = 0
        for a in responses[:-1]:
            total += answers[a]
        outputs = [(4,"Minimal depression"),(9,"Mild depression"),(14,"Moderate depression"),(19,"Moderately severe depression"),(27,"Severe depression")]
        results = {"Minimal depression":"Your results indicate that you have none, or very few symptoms of depression.","Mild depression":"Your results indicate that you may be experiencing some symptoms of mild depression. While your symptoms are not likely having a major impact on your life, it is important to monitor them.","Moderate depression":"Your results indicate that you may be experiencing symptoms of moderate depression. Based on your answers, living with these symptoms could be causing difficulty managing relationships and even the tasks of everyday life.","Moderately severe depression":"Your results indicate that you may be experiencing symptoms of moderately severe depression. Based on your answers, living with these symptoms is causing difficulty managing relationships and even the tasks of everyday life.","Severe depression":"Your results indicate that you may be experiencing symptoms of severe depression. Based on your answers, these symptoms seem to be greatly interfering with your relationships and the tasks of everyday life."}
        if total > 19:
            flag = True
        warning = ""
        if flag:
            warning += "Your responses indicate you may be at risk for harming yourself or someone else. Are you in crisis? Please call 911 or the National Suicide Prevention Hotline at 1-800-273-TALK or go immediately to the nearest emergency room. "
        for x in outputs:
            if total <= x[0]:
                userbase[user] = {"depression":total}
                return {"result":x[1],"details":warning + results[x[1]]}
    return "This shouldn't happen..."
        
@app.route("/questions/<screen>")
def getquestions(screen):
    currbank = screenbank[screen]
    return json.dumps(currbank)

@app.route("/results/<screen>")
def getresponses():
    user = request.args.get("username")
    data = request.args.get("data")
    return evaluate(screen,data)

@app.route("/register")
def register():
    firstname = request.args.get("firstname")
    lastname = request.args.get("lastname")
    email = request.args.get("email")
    phone = request.args.get("phone")
    username = firstname[0] + lastname + "0"
    while username in userbase:
        username = username[:-1] + str(1 + int(username[-1]))
    userbase["username"] = {"username": username,"firstname": firstname,"lastname": lastname,"email": email,"phone": phone}
    return json.dumps(userbase["username"])

if __name__ == "__main__":
    app.run(port=8000)
