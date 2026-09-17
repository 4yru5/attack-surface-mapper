const axios = require("axios");

async function webhook(req){

    return axios.get(
        req.body.url
    );

}