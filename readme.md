# Openclassrooms Project 9
# Litreview - A Social App to Share Book&Articles Reviews

This project was created for the Openclassrooms' Python App Developper degree.

The Litreview app is an [MVP](https://en.wikipedia.org/wiki/Minimum_viable_product) for a social app.

## Users can:

- Create an account
- Ask for a review for a book or an article
- Create a review for a book or an article
- Answer a review request from another user they follow
- Edit or delete their tickets and reviews
- Follow, unfollow, see their followers
- See their posts and the posts from users they follow


## Admins can:

- Login as an admin to the admin area
```
http://127.0.0.1:8000/admin/login
```
- Create, update, edit, delete any:
  - Ticket
  - Review
  - User
  - Following connection (User following another)



## Installation

Create and activate a virtual environment.

```bash
python3 -m venv env
source env/bin/activate
```


Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Litreview.

```bash
pip3 install -r requirements.txt
```

## Usage

Launch the server:

```bash
python3 litreview/manage.py runserver --insecure
```
Visit the website in your browser at:
```
http://127.0.0.1:8000/
```

For a quick demo, Login with:
```
Username: John
Password: &é"'(§è!
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
