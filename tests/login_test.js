/// <reference path="./steps.d.ts" />
Feature('Login');
var FirstLogin = false;
var loginCookies = [];

Before((I) => {
    I.login('admin', 'password');
});

Scenario('test successful login', (I) => {
    I.seeInCurrentUrl('#dashboard');
    I.wait(30);
    I.click('Logout');
    I.login('admin', 'password');
});
