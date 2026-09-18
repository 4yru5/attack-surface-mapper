const axios = require("axios");

function triggerWebhook(req) {

    const url = req.body.url;

    return axios.get(url);

}

module.exports = {
    triggerWebhook
};