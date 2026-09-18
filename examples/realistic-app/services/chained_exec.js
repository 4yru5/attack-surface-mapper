const { exec } = require("child_process");

function runCommand(command) {

    exec(command);

}

function exportData(req) {

    const command = req.body.command;

    runCommand(command);

}

module.exports = {
    exportData
};