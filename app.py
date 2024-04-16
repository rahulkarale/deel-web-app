import logging
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask application
app = Flask(__name__)

# Connect to SQLite database
DATABASE_URL = 'sqlite:///ip_addresses.db'
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define IPAddress model
class IPAddress(Base):
    __tablename__ = 'ip_addresses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    original_ip = Column(String, unique=True)
    reversed_ip = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Route to handle incoming requests
@app.route('/')
def index():
    client_ip = request.remote_addr

    # Check if IP address already exists in the database
    session = Session()
    existing_ip = session.query(IPAddress).filter_by(original_ip=client_ip).first()
    session.close()

    if existing_ip:
        logger.info(f"IP address '{client_ip}' already exists in the database.")
        return f"IP address '{client_ip}' already exists in the database.", 409

    # Reverse the IP address
    reversed_ip = '.'.join(reversed(client_ip.split('.')))
    reversed_ip = reversed_ip.rstrip('%')

    # Log the incoming and reversed IP addresses
    logger.info(f"Incoming IP: {client_ip}")
    logger.info(f"Reversed IP: {reversed_ip}")

    # Save the original and reversed IP addresses to the database
    session = Session()
    ip_address = IPAddress(original_ip=client_ip, reversed_ip=reversed_ip)
    session.add(ip_address)
    session.commit()
    session.close()

    return f"Reversed IP: {reversed_ip}"

# Endpoint to retrieve all IP addresses from the database
@app.route('/ip_addresses', methods=['GET'])
def get_ip_addresses():
    try:
        session = Session()
        ip_addresses = session.query(IPAddress).all()
        session.close()

        # Convert IP addresses to dictionary format
        ip_addresses_dict = [{'original_ip': ip.original_ip, 'reversed_ip': ip.reversed_ip} for ip in ip_addresses]

        return jsonify(ip_addresses_dict), 200
    except Exception as e:
        logger.error(f"An error occurred while retrieving IP addresses: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5001)
