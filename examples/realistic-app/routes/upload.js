const express = require("express");

const router = express.Router();

router.post(
    "/upload/image",
    authMiddleware,
    uploadImage
);

router.post(
    "/upload/document",
    authMiddleware,
    uploadDocument
);

module.exports = router;