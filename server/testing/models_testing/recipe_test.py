import pytest
from sqlalchemy.exc import IntegrityError

from app import app
from models import db, Recipe, User


class TestRecipe:
    '''Recipe in models.py'''

    def setup_method(self):
        """Clear tables before each test"""
        with app.app_context():
            Recipe.query.delete()
            User.query.delete()
            db.session.commit()

    def test_has_attributes(self):
        '''has attributes title, instructions, minutes_to_complete, and user_id.'''
        
        with app.app_context():
            # Create a dummy user
            user = User(username="testuser")
            user.password_hash = "password123"
            db.session.add(user)
            db.session.commit()

            recipe = Recipe(
                title="Delicious Shed Ham",
                instructions="""Or kind rest bred with am shed then. In""" + \
                    """ raptures building an bringing be. Elderly is detract""" + \
                    """ tedious assured private so to visited. Do travelling""" + \
                    """ companions contrasted it. Mistress strongly remember""" + \
                    """ up to. Ham him compass you proceed calling detract.""" + \
                    """ Better of always missed we person mr. September""" + \
                    """ smallness northward situation few her certainty""" + \
                    """ something.""",
                minutes_to_complete=60,
                user=user   # ✅ attach to user
            )

            db.session.add(recipe)
            db.session.commit()

            new_recipe = Recipe.query.filter_by(title="Delicious Shed Ham").first()

            assert new_recipe.title == "Delicious Shed Ham"
            assert len(new_recipe.instructions) >= 50
            assert new_recipe.minutes_to_complete == 60
            assert new_recipe.user.username == "testuser"

    def test_requires_title(self):
        '''requires each record to have a title.'''
        with app.app_context():
            user = User(username="testuser2")
            user.password_hash = "password123"
            db.session.add(user)
            db.session.commit()

            recipe = Recipe(
                instructions="X" * 60,
                minutes_to_complete=20,
                user=user
            )
            
            with pytest.raises(IntegrityError):
                recipe.title = None  # explicitly remove title
                db.session.add(recipe)
                db.session.commit()

    def test_requires_50_plus_char_instructions(self):
        with app.app_context():
            user = User(username="testuser3")
            user.password_hash = "password123"
            db.session.add(user)
            db.session.commit()

            '''must raise either a sqlalchemy.exc.IntegrityError with constraints or a custom validation ValueError'''
            with pytest.raises((IntegrityError, ValueError)):
                recipe = Recipe(
                    title="Generic Ham",
                    instructions="idk lol",
                    minutes_to_complete=15,
                    user=user   # ✅ still required
                )
                db.session.add(recipe)
                db.session.commit()
