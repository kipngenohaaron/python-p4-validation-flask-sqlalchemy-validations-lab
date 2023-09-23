from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Author name is required.')
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number and len(phone_number) != 10:
            raise ValueError('Author phone number must be exactly ten digits.')
        return phone_number
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name}, phone_number={self.phone_number})'

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String, default='news')  #
    summary = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError('Post title is required.')
        # Add custom validation for clickbait-y titles
        if not any(keyword in title for keyword in ["Won't Believe", "Secret", "Top", "Guess"]):
            raise ValueError('Post title must be clickbait-y.')
        return title

    @validates('content')
    def validate_content(self, key, content):
        if content and len(content) < 250:
            raise ValueError('Post content must be at least 250 characters long.')
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError('Post summary must be a maximum of 250 characters.')
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if category not in ['news', 'sports', 'entertainment']:
            raise ValueError('Invalid category.')
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, category={self.category})'