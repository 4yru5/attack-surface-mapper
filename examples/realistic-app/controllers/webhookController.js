const service = require("../services/webhookService");

function processWebhook(req){

    const url = req.body.url;

    service.send(url);

}

module.exports = {
    processWebhook
};