const { exec } = require(
    "child_process"
);

function runCommand(data){

    exec(data);

}

function processExport(req){

    const command =
        req.body.command;

    runCommand(command);

}