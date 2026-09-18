const axios = require("axios");

function send(data){

    return axios.get(data);

}

module.exports = {
    send
};