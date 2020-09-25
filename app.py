from flask import Flask, request, render_template, Response, session, redirect, url_for
from flask_restful import Resource, Api
import sqlite3
import json
import jsonpickle
import requests
import ast
from markupsafe import escape
from fuzzywuzzy import fuzz
import markdown
import markdown.extensions.fenced_code

app = Flask(__name__, static_url_path='/static')
api = Api(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


class GetRandom(Resource):
    def get(self):
        if request.headers.get('X-RapidAPI-Proxy-Secret') == "a678f990-eca0-11ea-84db-2fbcc004579c":
            conn = sqlite3.connect('database/firefly.db')
            c = conn.cursor()
            c.execute(
                """Select character,episode,quote from quotes ORDER BY RANDOM() LIMIT 1""")
            results_set = c.fetchone()

            if results_set == None:
                return {"body": "No results"}

            result_dictionary = {
                "Character": results_set[0],
                "Episode": results_set[1],
                "Quote": results_set[2]
            }
            return {"body": result_dictionary}
        else:
            return "Api key failure"


class GetCharacterQuotes(Resource):
    def get(self, chname):
        if request.headers.get('X-RapidAPI-Proxy-Secret') == "a678f990-eca0-11ea-84db-2fbcc004579c":
            conn = sqlite3.connect('database/firefly.db')
            c = conn.cursor()
            c.execute("Select character,episode,quote from quotes where character = '" +
                      chname.title() + "' ORDER BY RANDOM() LIMIT 1""")
            results_set = c.fetchone()

            if results_set == None:
                return {"body": "No results"}

            result_dictionary = {
                "Character": results_set[0],
                "Episode": results_set[1],
                "Quote": results_set[2]
            }
            return {"body": result_dictionary}
        else:
            return "Api Key Failure"


class GetEpisodeQuotes(Resource):
    def get(self, epname):
        if request.headers.get('X-RapidAPI-Proxy-Secret') == "a678f990-eca0-11ea-84db-2fbcc004579c":
            conn = sqlite3.connect('database/firefly.db')
            c = conn.cursor()
            c.execute("Select character,episode,quote from quotes where episode = '" +
                      epname.title() + "' ORDER BY RANDOM() LIMIT 1""")
            results_set = c.fetchone()

            if results_set == None:
                return {"body": "No results"}

            result_dictionary = {
                "Character": results_set[0],
                "Episode": results_set[1],
                "Quote": results_set[2]
            }
            return {"body": result_dictionary}
        else:
            return "Api Key Failure"


class GetHome(Resource):
    def get(self):
        return app.send_static_file('MainResume.html')


class mail(Resource):
    def get(self):
        return "nope"

    def post(self):
        conn = sqlite3.connect('database/firefly.db')
        c = conn.cursor()
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        c.execute("Insert into messages values ('" +
                  name+"','"+email+"','"+message+"')")
        conn.commit()
        return request.form


class GetZipInfo(Resource):

    def get(self, ziptosearch):
        # print("Get Zip Info Called")
        if request.headers.get('X-RapidAPI-Proxy-Secret') == "e2a4d700-f1e5-11ea-bc74-5b45dd6d70e2":
            conn = sqlite3.connect('database/firefly.db')
            c = conn.cursor()
            c.execute("select zip,type,decommissioned,primary_city,acceptable_cities,unacceptable_cities,state,county,timezone,area_codes,world_region,country,latitude,longitude,irs_estimated_population_2015 from zipdata where zip = " +
                      str(ziptosearch))
            results_set = c.fetchone()

            if results_set == None:
                return {"body": "No results"}

            result_dictionary = {
                "zip": results_set[0],
                "type": results_set[1],
                "decommissioned": results_set[2],
                "primary_city": results_set[3],
                "acceptable_cities": results_set[4],
                "unacceptable_cities": results_set[5],
                "state": results_set[6],
                "county": results_set[7],
                "timezone": results_set[8],
                "area_codes": results_set[9],
                "world_region": results_set[10],
                "country": results_set[11],
                "latitude": results_set[12],
                "longitude": results_set[13],
                "irs_estimated_population_2015": results_set[14]
            }
            return {"body": result_dictionary}
        else:
            return "Api Key Failure"


class GetZipInfoByCityState(Resource):

    def get(self, city, state):
        if request.headers.get('X-RapidAPI-Proxy-Secret') == "e2a4d700-f1e5-11ea-bc74-5b45dd6d70e2":
            conn = sqlite3.connect('database/firefly.db')
            c = conn.cursor()
            c.execute("select zip,type,decommissioned,primary_city,acceptable_cities,unacceptable_cities,state,county,timezone,area_codes,world_region,country,latitude,longitude,irs_estimated_population_2015 from zipdata where primary_city = '" +
                      str(city) + "' and state = '" + str(state) + "'")
            results_set = c.fetchall()

            result_array = []
            result_dictionary = {}

            if results_set == None:
                return {"body": "No results"}

            for row in results_set:
                result_dictionary["zip"] = row[0]
                result_dictionary["type"] = row[1]
                result_dictionary["decommissioned"] = row[2]
                result_dictionary["primary_city"] = row[3]
                result_dictionary["acceptable_cities"] = row[4]
                result_dictionary["unacceptable_cities"] = row[5]
                result_dictionary["state"] = row[6]
                result_dictionary["county"] = row[7]
                result_dictionary["timezone"] = row[8]
                result_dictionary["area_codes"] = row[9]
                result_dictionary["world_region"] = row[10]
                result_dictionary["country"] = row[11]
                result_dictionary["latitude"] = row[12]
                result_dictionary["longitude"] = row[13]
                result_dictionary["irs_estimated_population_2015"] = row[14]

                result_array.append(result_dictionary)

            return {"body": result_array}
        else:
            return "Api Key Failure"


class GetZipInfoByState(Resource):

    def get(self, state):
        if request.headers.get('X-RapidAPI-Proxy-Secret') == "e2a4d700-f1e5-11ea-bc74-5b45dd6d70e2":
            conn = sqlite3.connect('database/firefly.db')
            c = conn.cursor()
            c.execute("select zip,type,decommissioned,primary_city,acceptable_cities,unacceptable_cities,state,county,timezone,area_codes,world_region,country,latitude,longitude,irs_estimated_population_2015 from zipdata where state = '" + str(state) + "'")
            results_set = c.fetchall()

            result_array = []
            result_dictionary = {}

            if results_set == None:
                return {"body": "No results"}

            for row in results_set:
                result_dictionary["zip"] = row[0]
                result_dictionary["type"] = row[1]
                result_dictionary["decommissioned"] = row[2]
                result_dictionary["primary_city"] = row[3]
                result_dictionary["acceptable_cities"] = row[4]
                result_dictionary["unacceptable_cities"] = row[5]
                result_dictionary["state"] = row[6]
                result_dictionary["county"] = row[7]
                result_dictionary["timezone"] = row[8]
                result_dictionary["area_codes"] = row[9]
                result_dictionary["world_region"] = row[10]
                result_dictionary["country"] = row[11]
                result_dictionary["latitude"] = row[12]
                result_dictionary["longitude"] = row[13]
                result_dictionary["irs_estimated_population_2015"] = row[14]

                result_array.append(result_dictionary)

            return {"body": result_array}
        else:
            return "Api Key Failure"


api.add_resource(GetRandom, '/quotes/random')
api.add_resource(GetCharacterQuotes, '/quotes/<string:chname>')
api.add_resource(GetEpisodeQuotes, '/quotes/episodes/<string:epname>')
api.add_resource(GetHome, '/')
api.add_resource(mail, '/mail')
api.add_resource(GetZipInfo, '/zipcode/<int:ziptosearch>')
api.add_resource(GetZipInfoByCityState,
                 '/zipcodebyname/<string:city>/<string:state>')
api.add_resource(GetZipInfoByState,
                 '/zipcodebystate/<string:state>')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']

        conn = sqlite3.connect('database/firefly.db')
        c = conn.cursor()
        username = request.form['username']

        c.execute("select userid from users where username = '"+username + "'")
        exist = c.fetchone()

        if exist is None:
            c.execute("Insert into users (username, correct, incorrect) values ('" +
                      username+"',"+str(0)+","+str(0)+")")
            conn.commit()

        c.execute("select userid from users where username = '"+username + "'")
        result = c.fetchone()

        session['userid'] = result

        return redirect("/trivia")


@app.route('/trivia', methods=['GET'])
def GetTrivia():
    if request.method == 'GET':
        if 'username' in session:

            if 'score' not in session:
                session['score'] = {"correct": 0, "incorrect": 0}
                score = {"correct": 0, "incorrect": 0}
            else:
                score = session['score']

            username = escape(session['username'])

            conn = sqlite3.connect('database/firefly.db')
            c = conn.cursor()
            c.execute("select distinct(category) as category from questions")
            results_set = c.fetchall()

            return render_template('Trivia.html', categories=results_set, username=username, score=score)
        else:
            return render_template('Login.html')


@ app.route('/getquestions', methods=['GET'])
def GetStandings():
    if request.method == 'GET':
        category = request.args.get('questions')
        conn = sqlite3.connect('database/firefly.db')
        c = conn.cursor()
        c.execute("select questionid,question from questions where category = '" +
                  category + "' ORDER BY RANDOM() LIMIT 1")
        results_set = c.fetchone()
        if(results_set is not None):
            return render_template('Quiz.html', questions=results_set, category=category)
        else:
            return redirect("/trivia")
    else:
        return "Nope"


@ app.route('/standings', methods=['GET'])
def GetQuestions():
    if request.method == 'GET':
        #category = request.args.get('questions')
        conn = sqlite3.connect('database/firefly.db')
        c = conn.cursor()
        c.execute("select username, correct, incorrect from users")
        results_set = c.fetchall()
        if(results_set is not None):
            return render_template('Standings.html', standings=results_set)
        else:
            return redirect("/trivia")
    else:
        return "Nope"


@ app.route('/answer', methods=['POST'])
def CheckAnswer():
    if request.method == 'POST':
        if 'username' in session:
            answer = request.form.get('answer')
            question = request.form.get('question')
            conn = sqlite3.connect('database/firefly.db')
            score_correct = session['score']['correct']
            score_incorrect = session['score']['incorrect']
            userid = session['userid']
            c = conn.cursor()
            c.execute(
                "select answer from questions where questionid = " + question)
            results_set = c.fetchone()
            Partial_Ratio = fuzz.partial_ratio(
                results_set[0].lower(), answer.lower())
            if(Partial_Ratio >= 80):
                modified_correct = score_correct + 1
                session['score'] = {
                    "correct": modified_correct, "incorrect": score_incorrect}
                c.execute("update users set correct = '" + str(modified_correct) +
                          "', incorrect = '" + str(score_incorrect) + "' where userid ='" + str(userid[0])+"'")
                conn.commit()
                qresult = 'Correct'
            else:
                modified_incorrect = score_incorrect + 1
                session['score'] = {
                    "correct": score_correct, "incorrect": modified_incorrect}
                c.execute(
                    "update users set correct = '" + str(score_correct) + "', incorrect = '" + str(modified_incorrect) + "' where userid = '" + str(userid[0]) + "'")
                conn.commit()
                qresult = 'Incorrect'
            return render_template('Result.html', qresult=qresult, answer=results_set[0])
        else:
            redirect('/trivia')
    else:
        return "Nope"


@ app.route('/blog', methods=['GET'])
def GetBlog():
    readme_file = open("blog.md", "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"])
    return render_template('Blog.html', markdown=md_template_string)


@ app.errorhandler(404)
def page_not_found(e):
    result = "Page not found"
    return result


if __name__ == '__main__':
    app.run(port=8000)
