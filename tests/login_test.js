/// <reference path="./steps.d.ts" />
Feature('Login');

Scenario('test successful login', (I) => {
    // I.fillField('q','ole.org');
    // I.click('btnG');
    // I.seeInTitle('ole.org');
    I.amOnPage('/');
    I.fillField('Login', 'admin');
    I.fillField('Password', 'password');
    I.click('Sign In');
    //I.waitForText('Manager', 10);
    //I.wait(30);
    //I.seeInCurrentUrl('#dashboard');
    I.waitForText('Set Configurations', 10);
    I.seeInCurrentUrl('#configuration/add');
});
