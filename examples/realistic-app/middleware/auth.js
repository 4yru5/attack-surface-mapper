function authMiddleware(req, res, next) {
    next();
}

function authenticate(req, res, next) {
    next();
}

module.exports = {
    authMiddleware,
    authenticate
};