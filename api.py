from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app) 
api = Api(app)

class UserModel(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self): 
        return f"User(name = {self.name}, email = {self.email})"

user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")


userFields = {
    'id':fields.Integer,
    'name':fields.String,
    'email':fields.String,
    
}

class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all() 
        return users 
    
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email=args["email"])
        db.session.add(user) 
        db.session.commit()
        users = UserModel.query.all()
        return users, 201
    
class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first() 
        if not user: 
            abort(404, message="Usuário não encontrado")
        return user 
    
    @marshal_with(userFields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first() 
        if not user: 
            abort(404, message="Usuário não encontrado")
        user.name = args["name"]
        user.email = args["email"]
        db.session.commit()
        return user 
    
    @marshal_with(userFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first() 
        if not user: 
            abort(404, message="Usuário não encontrado")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users

    
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Visual Touch</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                 background: linear-gradient(135deg, #e0b0ff, #b19cd9, #e0b0ff);
            }
            header {
                background-color: rgba(186, 146, 250, 0.7);
                color: #fff;
                padding: 20px;
                text-align: center;
            }
            h1 {
                margin: 0;
                font-size: 3em;
                letter-spacing: 2px;
            }
            .content {
                padding: 20px;
                text-align: center;
            }
            .content h2 {
                font-size: 2.5em;
                color: #333;
                margin-bottom: 20px;
            }
            .content p {
                font-size: 1.2em;
                color: #000;
                max-width: 800px;
                margin: 0 auto 30px auto;
                margin-top: 20px;
            }
            .image-container {
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                margin-bottom: 50px;
            }
            .image-container img {
                margin: 10px;
                width: 250px;
                height: auto;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }

            form {
                background-color: #fff;
                padding: 20px;
                margin: 0 auto;
                max-width: 400px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            input[type="text"], input[type="email"] {
                    width: 90%;
                    padding: 10px;
                    margin: 10px 10px;
                    border: 1px solid #ccc;
                    border-radius: 15px;
                    font-size: 1em;
            }
            input[type="submit"] {
                background-color: #6a0dad;
                color: white;
                padding: 12px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 1.1em;
                width: 100%;
            }
            input[type="submit"]:hover {
                background-color: #4b0082;
            }

                       

            footer {
                background-color: rgba(186, 146, 250, 0.7);
                color: #fff;
                text-align: center;
                padding: 10px;
                position: fixed;
                bottom: 0;
                width: 100%;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>Visual Touch</h1>
        </header>

        <div class="content">
            <h2>Uma Nova perspectiva da interação</h2>
            <p>Você já imaginou um mundo onde você pode controlar o cursor do seu mouse apenas com o movimento dos seus olhos? Este é o objetivo do nosso projeto inovador, que utiliza a poderosa biblioteca MediaPipe, combinada com OpenCV e PyAutoGUI, para permitir que você navegue pela internet e interaja com seu computador sem precisar usar as mãos..</p>
            
            <div class="image-container">
                <img src="../static/images/cadeirante.png" alt="">
                <img src="../static/images/logovetor.png" alt="">
                <img src="../static/images/sic logo.png" alt="">
             
            </div>

             <form action="/submit" method="POST">
                <input type="text" name="name" placeholder="Digite seu nome" required>
                <input type="email" name="email" placeholder="Digite seu email" required>
                <input type="submit" value="Saiba Mais">
            </form>
            
            <p>Explore como o Visual Touch está transformando a forma como interagimos com os dispositivos. Junte-se a nós na construção de um futuro onde a interação seja mais acessível!!</p>
        </div>

        <footer>
            <p>&copy; 2024 Visual Touch - All Rights Reserved</p>
        </footer>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)  