
'use strict';
let Helper = codecept_helper;
var request = require('request');

class SauceLabsSession extends Helper {

  _after() {
    if (process.env.SAUCE_USERNAME) {
      var sessionId = this.helpers['WebDriverIO'].browser.requestHandler.sessionID;
      var sauce_url = "Test finished. Link to job: https://saucelabs.com/jobs/";
      sauce_url = sauce_url.concat(sessionId);
      console.log(sauce_url);


      var dataString = '{"passed": true}';
      var status_url = 'https://saucelabs.com/rest/v1/';
      status_url = status_url.concat(process.env.SAUCE_USERNAME);
      status_url = status_url.concat('/jobs/');
      status_url = status_url.concat(sessionId);

      var options = {
        url: status_url,
        method: 'PUT',
        body: dataString,
        auth: {
          'user': process.env.SAUCE_USERNAME,
          'pass': process.env.SAUCE_ACCESS_KEY
        }
      };

      function callback(error, response, body) {
        if (!error && response.statusCode == 200) {
          console.log(body);
        }
      }

      request(options, callback);
    }
  }
}

module.exports = SauceLabsSession;
