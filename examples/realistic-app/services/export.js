const { exec } = require("child_process");

function runCommand(req) {

    const command = req.body.command;

    exec(command);

}

module.exports = {
    runCommand
};