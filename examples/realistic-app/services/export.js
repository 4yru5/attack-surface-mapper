const { exec } = require(
  "child_process"
);

function exportData(req){

    exec(
        req.body.command
    );

}