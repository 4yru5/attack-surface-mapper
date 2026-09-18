const axios = require("axios");

function sendRequest(data){

    return axios.get(data);

}

function processWebhook(req){

    const url = req.body.url;

    const validated = sanitize(url);

    return sendRequest(validated);

}