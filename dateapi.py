import os
from openai import OpenAI
from flask import Flask, jsonify, request
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

today = datetime.today().strftime('%Y-%m-%d')
format = 'CurStart: YYYY/MM/DD CurEnd: YYYY/MM/DD PrevStart: YYYY/MM/DD PrevEnd: YYYY/MM/DD'

app = Flask(__name__)
@app.route('/get-date')
def get_date():
    input_param = request.args.get('input')
    chat_completion = OpenAI(api_key=os.getenv("OPENAI_API_KEY")).chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Clean this input '"+ input_param + "' by stripping all information that does not represent a time period. \
                Convert the cleaned data information to this format "+ format +" Assume today's date is " + today + "(ignore if applicable)  \
                and assume 2024 (unless specified otherwise). Always stick to the format, especially for one day range inputs. \
                If only one date range is provided, output the last two occurences of the range, keeping the interval equal (unless clearly specified otherwise). \
                For example, the input 'what's changed in the last week' should return the last week as the first date range and two weeks ago as the second one (the weeks must be consecutive). \
                The input 'what's changed in the last month' should return the last month as the first date range, and two months ago as the second date range. \
                Another example would be for 'what's changed from christmas', the output should be the date of last christmas and two christmases ago. \
                Another example would be, for 'whats changed from 1st july to today', the first date range should be today and 1st july, \
                and the other date range should be 1st of july seperated by the same amount of time as the first date range.     \
                Make sure it is not the same date, and make sure there are only two sets of date ranges, that follow the format. \
                There may be text that is not related to the date, ignore it. Ensure the format "+ format +" is followed    . ",
            }
        ],
        top_p=0.15,
        model="gpt-3.5-turbo",
    )

    chat_response = chat_completion.choices[0].message.content.split('\n')[0]
    return jsonify(chat_response), 200

if __name__ == '__main__':
    app.run(debug=True)
