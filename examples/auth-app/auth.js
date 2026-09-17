const passport = require('passport');
const jwt = require('jsonwebtoken');

router.get(
    "/profile",
    passport.authenticate('jwt', { session: false }),
    getProfile
);

router.get(
    "/admin",
    authMiddleware,
    getAdminData
)