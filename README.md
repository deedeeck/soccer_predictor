# soccer_predictor
Code to try predicting soccer results

## Chrome driver
* Download chrome driver from https://chromedriver.chromium.org/

### Selenium remote server
* Download remote selenium server from https://www.seleniumhq.org/download/
* Run remote selenium server in a seperate tab
```
java -jar selenium-server-standalone-3.141.59.jar
```
* Run crawler.py once with remote mode and get the session id
```
python crawler.py --remote
```
* Once you have session id, run crawler.py again and it will attach to existing session of selenium remote server
```
python crawler.py --session <<session id>>
```
* If selenium standalone server is giving chrome version error, reclone repo and redownload everything in a new folder