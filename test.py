import unittest
from query import *


# Only run when there's existing actor.json and film.json
class TestQuery(unittest.TestCase):
    """Test query.py"""

    # Check films and their correct grossing.
    def test_total_gross(self):
        """Test method total_gross(film_name)"""
        self.assertEqual(str(7800000), total_gross('Going My Way'))
        self.assertEqual(str(119300000), total_gross('On Golden Pond'))
        self.assertEqual(str(68700000), total_gross('Witness'))

    # Check actors and films they have performed in.
    def test_movie_worked(self):
        """Test method movie_worked(actor_name)"""
        self.assertEqual('Rose, The', movie_worked('Frederic Forrest'))
        self.assertEqual('Ray', movie_worked('Jamie Foxx'))
        self.assertEqual('Million Dollar Baby', movie_worked('Morgan Freeman'))

    # Actors/actresses of Hacksaw Ridge should include Andrew Garfield
    def test_which_actor(self):
        """Test method which_actor(film_name)"""
        self.assertIn('Andrew Garfield', which_actor('Hacksaw Ridge'))

    # Claudette Colbert should be in top grossing actors regardless of how much x is.
    def test_top_actors(self):
        """Test method top_actors(x)"""
        self.assertIn('Claudette Colbert', top_actors(1))
        self.assertIn('Claudette Colbert', top_actors(5))
        self.assertIn('Claudette Colbert', top_actors(10))

    # Luise Rainer should be oldest actress regardless of how many oldest actors we are looking for.
    def test_old_actors(self):
        """Test method old_actors(x)"""
        self.assertIn('Luise Rainer', old_actors(1))
        self.assertIn('Luise Rainer', old_actors(5))
        self.assertIn('Luise Rainer', old_actors(10))

    # Check if movies in 2000 include Walk the Line.
    def test_movies_in_year(self):
        """Test method movies_in_year(year)"""
        self.assertIn('Walk the Line', movies_in_year(2000))

    # Javier Bardem should be one of the actors in 2000.
    def test_actors_in_year(self):
        """Test method actors_in_year"""
        self.assertIn('Javier Bardem', actors_in_year(2000))


if __name__ == '__main__':
    unittest.main()
