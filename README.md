# pYnsta

[![License](https://img.shields.io/github/license/sheerley/pynsta)](https://github.com/Sheerley/pYnsta/blob/master/LICENSE)


## Disclaimer
This code is published for  educational purposes only. Using it may result in ban on your Instagram account.

## Requirements
To start using *pYnsta*, install all required dependencies:
```bash
pip install --user -r ./requirements.txt
```

## Runing pYnsta
To run *pYnsta* write this in your terminal:
```bash
python3 ./pynsta.py
```

## Configuration

### Credentials
Edit `secrets.py` to include your *username* (e.g. username, e-mail or phone number).
```python
# username, e-mail or phone number
username = 'Your_Username_Here'
# password
password = 'Your_Password_Here'
```

### Hashtags
To include your own hashtags on which action should be performed, edit `topics.txt` file. 

**DO NOT** write more than one hashtag in each line.

Remember to put `#` in front of every line. Line should not include any space or special character.