from flask import Flask, render_template

# Import our psycopg2 library, which lets us connect our Flask app to our Postgres database.
import sqlalchemy

# Create an instance of our Flask app.
app = Flask(__name__)

connection_string = f"postgres:Payrol662!@localhost:5433/CarAuctionDB"

# Pass connection url to the sqlalchemy create_engine method
engine = sqlalchemy.create_engine(f'postgresql://{connection_string}')

# Set route
@app.route('/')
def index():
    # Store the entire footwear collection in a list
    acura = engine.execute("SELECT auction_code, car_year, color, make, model FROM acura")

    # Return the template with the footwear list passed in
    return render_template('index.html', acura=acura)


if __name__ == "__main__":
    app.run(debug=True)