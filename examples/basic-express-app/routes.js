const express = require("express");

const router = express.Router();

router.get("/users", getUsers);

router.post("/login", login);

router.post(
    "/admin",
    authMiddleware,
    createAdmin
);

module.exports = router;