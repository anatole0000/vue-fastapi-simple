from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from flask_migrate import Migrate



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this for security
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Create a model for items
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400
    
    # Use a secure password hash method
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "User created successfully"}), 201

# Login route
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"msg": "Username and password are required"}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if user is None or not check_password_hash(user.password, password):
            return jsonify({"msg": "Invalid username or password"}), 401
        
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    
    except Exception as e:
        print(f"Error during login: {str(e)}")
        return jsonify({"msg": "Internal server error"}), 500


# Protected route
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# Route to get items
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{'id': item.id, 'name': item.name} for item in items])

# Route to add an item
@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    new_item = Item(name=data['name'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'id': new_item.id, 'name': new_item.name}), 201

@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    item = Item.query.get_or_404(id)
    data = request.get_json()
    item.name = data['name']
    db.session.commit()
    return jsonify({'id': item.id, 'name': item.name})

# Delete item by ID
@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted successfully'})

# Get current user's profile
@app.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({
        "username": user.username,
        "email": user.email or ""
    })

# Update current user's profile
@app.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json()
    user.email = data.get("email", user.email)
    if data.get("password"):
        user.password = generate_password_hash(data["password"], method='sha256')  # Hash the new password
    db.session.commit()

    return jsonify({"msg": "Profile updated"})

# Create database and tables within the application context
with app.app_context():
    db.create_all()  # Creates the SQLite database

if __name__ == '__main__':
    app.run(debug=True)
