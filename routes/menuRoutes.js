const express = require('express');
const { isAuthenticated } = require('../middlewares/authMiddleware');
const router = express.Router();

router.get('/', isAuthenticated, (req, res) => {
  const user = req.session.user;
  res.render('menu', { 
    user, 
    pageTitle: "Menu Principal" // Titre personnalisé pour cette page
  });
});

module.exports = router;
