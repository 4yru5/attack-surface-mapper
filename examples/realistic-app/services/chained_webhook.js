const axios = require("axios");

function sendRequest(data) {

    return axios.get(data);

}

function processWebhook(req) {

    const url = req.body.url;

    return sendRequest(url);

}

module.exports = {
    processWebhook
};