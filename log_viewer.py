from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>DNS Log Viewer</title>
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { padding: 8px; border: 1px solid #ccc; }
        th { background: #eee; }
    </style>
</head>
<body>
    <h1>DNS Query Log</h1>
    <table>
        <tr>
            <th>ID</th>
            <th>Timestamp</th>
            <th>Client IP</th>
            <th>Domain</th>
        </tr>
        {% for row in logs %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
            <td>{{ row[3] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
'''

@app.route("/")
def index():
    conn = sqlite3.connect("dns_log.db")
    c = conn.cursor()
    c.execute("SELECT * FROM dns_queries ORDER BY timestamp DESC LIMIT 100")
    logs = c.fetchall()
    conn.close()
    return render_template_string(TEMPLATE, logs=logs)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
