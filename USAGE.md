## Usage ##
## Example ##
`python3 fget.py http://example.com/file.zip`
`python3 fget.py https://example.com/file.zip`
`python3 fget.py http://example.com/file.zip --user-agent "Mozilla/5.0 (Linux 6.5.0; ; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Chrome/125.0.6422.60 Not.A/Brand/24  Safari/537.36"`
`python3 fget.py http://example.com/file.zip -m POST --data="user=nah&password=1234"`
`python3 fget.py https://example.com/file.zip --cert file.crt`
`python3 fget.py http://example.com/file.zip -d directory`
`python3 fget.py http://example.com/file.zip -m GET`
`python3 fget.py http//example.com/file.zip --timeout 999`
`python3 fget.py http//example.com/file.zip --retries 13`
`python3 fget.py https://example.com/file.zip --no-check-certificate`
`python3 fget.py http://protected.com/secret.txt -u user -p 19876`
`python3 fget.py http//example.com/file.zip --proxy http://asd:asd@21.213.4.56:1239`
`python3 fget.py http//example.com/file.zip --headers "Content-Type: application/x-www-form-urlencoded"`
`python3 fget ftp://127.0.0.1 -u asd -p 123t`
`python3 fget ftp://127.0.0.1 --ftp-anonymous`
`python3 fget http://::1/90.txt -6`
