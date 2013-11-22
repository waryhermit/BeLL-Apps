#!/usr/bin/env node

/**
 * Module dependencies.
 */

var sys = require('sys')
var exec = require('child_process').exec;
var _ = require('underscore')
var request = require('request')
var program = require('commander');
var fs = require('fs')
var replicatorInstaller = require('./includes/replicator-installer')
function puts(error, stdout, stderr) { sys.puts(stdout) } 

// Increase the ulimit so the entire directory of attachments can be uploaded
exec('launchctl limit maxfiles 10056 10056', puts)
exec('ulimit -n 10056', puts)

program
  .version('0.0.1')
  .option('-c, --couchurl [couchurl]', '', 'http://pi:raspberry@127.0.0.1:5984')
  .option('-m, --mapfile [mapfile]', '', null)
  .option('-h, --hostname [hostname]', '', null)
  .parse(process.argv);

var settings = {
  databases: require('./config/databases')
}

if (program.mapfile) {
  settings.map = require(program.mapfile)
}

// @todo Process the mapFile to get the map for this hostname
// For now, the mapFiles are preprocessed
settings.couchurl = program.couchurl


if(program.hostname) {
  // Set settings.hostname in /etc/hosts and etc/hostname
  var fileName = '/etc/hosts'
  fs.readFile(fileName, 'utf8', function (err,data) {
    if (err) {
      return console.log(err);
    }
    var result = data.replace(/raspberrypi/g, program.hostname);

    fs.writeFile(someFile, result, 'utf8', function (err) {
      if (err) return console.log(err);
      // Set settings.hostname in /etc/hosts and etc/hostname
      var fileName = '/etc/hostname'
      fs.readFile(someFile, 'utf8', function (err,data) {
        if (err) {
          return console.log(err);
        }
        var result = data.replace(/raspberrypi/g, program.hostname);

        fs.writeFile(someFile, result, 'utf8', function (err) {
          if (err) return console.log(err);
          exec('sudo /etc/init.d/hostname.sh', puts)
          console.log("Restart for hostname change to take effect.")
        });
      });
    });
  });
}

_.each(settings.databases, function(database) {
  // Install databases
  request.put(settings.couchurl + '/' + database)
  // Install views in corresponding databases
  exec('couchapp push ../views/' + database + '.js ' + settings.couchurl + '/' + database, puts);
})

// Push the Apps up to CouchDB
exec('couchapp push ../app.js ' + settings.couchurl + '/apps', puts);

// Create default admin member
exec('curl -XPUT ' + settings.couchurl + '/members/ce82280dc54a3e4beffd2d1efa00c4e6 -d \'{"login":"admin","kind":"Member", "roles": ["admin"], "firstName": "Default", "lastName": "Admin", "password":"password", "status": "active"}\'', puts) 

if(program.mapfile) {
  console.log('installing using the map at %s', program.mapFile);
  replicatorInstaller.start(settings)
}
