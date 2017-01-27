
//'use strict';
// in this file you can append custom step methods to 'I' object
module.exports = function () {

  var loginCount = 0; // Used to check for config page.
  var loginCookies = [];
  return actor({

    // Define custom steps here, use 'this' to access default methods of I.
    // It is recommended to place a general 'login' fSunction here.

    login: function (email, password) {
      if (loginCount < 1) {
        this.amOnPage('/');
        this.fillField('Login', 'admin');
        this.fillField('Password', 'password');
        this.click('Sign In');
        this.saveCookies();
      }
      else {
        this.loadCookies();
        this.amOnPage('/');
        this.seeInCurrentUrl('#dashboard');
      }
      loginCount = loginCount + 1;
    }
  });
}
