# clashogram-serverless

## Quick start

1. Configure awscli - refer to aws docs.
2. Create a telegram bot - refer to telegram docs
3. Create a telegram channel
4. Add your bot from step 2 to the channel as a n admin
5. Get your bot's token from BothFather and add it to the `config.dev.yml` file
6. Clone this repo: `git clone https://github.com/mehdisadeghi/clashogram-serverless`
7. Run `npm install` in the repo root
8. Install serverless: `npm install -g serverless`
9. Run `sls deploy` in the repo root
10. From the output of step 9, find `call` endpint and open it in your browser
11. From the output of step 10 note the displyed ip address
12. Go to clash of clan's developer console and create a token for the IP
13. Add the token to the `config.dev.yml` file
14. Rerun `sls deploy`

If you are lucky the above steps will work flawlessly and you'd have a 
working Clashogram on AWS cloud which will post your clan's war updates
to the given channel every one minute.
