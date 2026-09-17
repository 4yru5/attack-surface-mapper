const express = require("express");

const router = express.Router();

router.get(
    "/admin",
    authMiddleware,
    getAdmin
);

router.delete(
    "/admin/user/:id",
    authMiddleware,
    deleteUser
);

module.exports = router;