import csv

from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>===== NayePankh Foundation =====</h1>
    <ul>
        <li><a href="/add_volunteer">Add Volunteer</a></li>
        <li><a href="/view_volunteers">View Volunteers</a></li>
        <li><a href="/search_volunteer">Search Volunteer</a></li>
        <li><a href="/add_donation">Add Donation</a></li>
        <li><a href="/view_donations">View Donations</a></li>
        <li><a href="/generate_report">Generate Report</a></li>
        <li><a href="/delete_volunteer">Delete Volunteer</a></li>
        <li><a href="/filter_donations">Filter Donations</a></li>
        <li><a href="/exit">Exit</a></li>
    </ul>
    '''


    # ================= ADD VOLUNTEER =================
@app.route('/add_volunteer', methods=['GET', 'POST'])
def add_volunteer():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        with open('volunteers.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, phone, email])

        return redirect('/view_volunteers')

    return '''
    <h2>Add Volunteer</h2>
    <form method="post">
        Name: <input name="name"><br>
        Phone: <input name="phone"><br>
        Email: <input name="email"><br>
        <button type="submit">Add</button>
    </form>
    '''

    # ================= VIEW VOLUNTEERS =================
@app.route('/view_volunteers')
def view_volunteers():
    data = []

    try:
        with open('volunteers.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 3:
                    data.append(row)
    except:
        pass

    html = "<h2>Volunteers</h2>"

    for v in data:
        html += f"<p>{v[0]} | {v[1]} | {v[2]}</p>"

    html += '<a href="/">Back</a>'
    return html

@app.route('/search_volunteer', methods=['GET', 'POST'])
def search_volunteer():
    result = None

    if request.method == 'POST':
        search_name = request.form['name']

        try:
            with open('volunteers.csv', 'r') as file:
                reader = csv.reader(file)

                for row in reader:
                    if len(row) == 3:
                        if search_name.lower() in row[0].lower():
                            result = row
                            break
        except:
            result = None

    return f"""
    <h2>Search Volunteer</h2>

    <form method="post">
        Enter Name: <input name="name">
        <button type="submit">Search</button>
    </form>

    <br>

    {"<p><b>Found:</b> " + result[0] + " | " + result[1] + " | " + result[2] + "</p>" if result else "<p>No volunteer found</p>"}

    <br>
    <a href="/">Back</a>
    """
    # ================= ADD DONATION =================
@app.route('/add_donation', methods=['GET', 'POST'])
def add_donation():
    if request.method == 'POST':
        donor = request.form['donor']
        amount = request.form['amount']

        with open('donations.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([donor, amount])

        return redirect('/view_donations')

    return '''
    <h2>Add Donation</h2>
    <form method="post">
        Donor: <input name="donor"><br>
        Amount: <input name="amount"><br>
        <button>Add</button>
    </form>
    '''

    # ================= VIEW DONATIONS =================
@app.route('/view_donations')
def view_donations():
    data = []

    try:
        with open('donations.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    data.append(row)
    except:
        pass

    html = "<h2>Donations</h2>"

    for d in data:
        html += f"<p>{d[0]} - ₹{d[1]}</p>"

    html += '<a href="/">Back</a>'
    return html
    # ================= REPORT =================
@app.route('/generate_report')
def generate_report():
    volunteer_count = 0
    donation_count = 0
    total_amount = 0

    # Volunteers count
    try:
        with open('volunteers.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 3:
                    volunteer_count += 1
    except:
        pass

    # Donations count + total
    try:
        with open('donations.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    donation_count += 1
                    try:
                        total_amount += float(row[1])
                    except:
                        pass
    except:
        pass

    return f"""
    <h2>Report</h2>
    <p>Total Volunteers: {volunteer_count}</p>
    <p>Total Donations: {donation_count}</p>
    <p>Total Donation Amount: ₹{total_amount}</p>
    <br>
    <a href="/">Back</a>
    """
    # ================= DELETE VOLUNTEER =================
@app.route('/delete_volunteer', methods=['GET', 'POST'])
def delete_volunteer():
    message = ""

    if request.method == 'POST':
        name_to_delete = request.form['name']
        data = []
        found = False

        try:
            with open('volunteers.csv', 'r') as file:
                reader = csv.reader(file)

                for row in reader:
                    if len(row) == 3:
                        if row[0].lower() != name_to_delete.lower():
                            data.append(row)
                        else:
                            found = True
        except:
            pass

        with open('volunteers.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

        if found:
            message = "Volunteer deleted successfully!"
        else:
            message = "Volunteer not found!"

    return f"""
    <h2>Delete Volunteer</h2>

    <form method="post">
        Enter Name: <input name="name">
        <button type="submit">Delete</button>
    </form>

    <p>{message}</p>

    <br>
    <a href="/">Back</a>
    """

@app.route('/filter_donations', methods=['GET', 'POST'])
def filter_donations():
    result = []
    min_amount = 0

    if request.method == 'POST':
        try:
            min_amount = float(request.form['amount'])
        except:
            min_amount = 0

        try:
            with open('donations.csv', 'r') as file:
                reader = csv.reader(file)

                for row in reader:
                    if len(row) == 2:
                        try:
                            if float(row[1]) >= min_amount:
                                result.append(row)
                        except:
                            pass
        except:
            pass

    html = """
    <h2>Filter Donations</h2>

    <form method="post">
        Minimum Amount: <input name="amount">
        <button type="submit">Filter</button>
    </form>
    """

    if result:
        for r in result:
            html += f"<p>{r[0]} - ₹{r[1]}</p>"
    elif request.method == 'POST':
        html += "<p>No matching donations found</p>"

    html += '<br><a href="/">Back</a>'
    return html

    # ================= EXIT =================
@app.errorhandler(404)
def not_found(e):
    return "<h2>Page Not Found</h2><a href='/'>Home</a>"