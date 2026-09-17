const express = require("express");

const router = express.Router();

router.get(
    "/users",
    authMiddleware,
    getUsers
);

router.get(
    "/users/:id",
    authenticate,
    getUser
);

router.put(
    "/users/:id",
    authMiddleware,
    updateUser
);

module.exports = router;