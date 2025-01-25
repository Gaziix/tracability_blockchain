// authController.js
const userModel = require('../models/userModel');

const login = (req, res) => {
  const { email, password } = req.body;

  userModel.getUserByEmail(email, (err, results) => {
    if (err) {
      console.error('Erreur lors de la requête SQL :', err);
      res.status(500).send('Erreur interne du serveur.');
      return;
    }

    if (results.length > 0) {
      const user = results[0];
      if (password === user.password) {
        // Initialiser la session utilisateur
        req.session.user = {
          id: user.id,
          email: user.email,
          last_name: user.last_name,
          first_name: user.first_name,
          company_name: user.company_name, // Nom de la compagnie
          company_phone: user.company_phone, // Numéro de téléphone de la compagnie
          company_type: user.company_type, // Type de la compagnie
        };
        res.redirect('/menu'); // Rediriger vers le menu
      } else {
        res.send('<h1>Mot de passe incorrect.</h1>');
      }
    } else {
      res.send('<h1>Utilisateur non trouvé.</h1>');
    }
  });
};

const logout = (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      return res.status(500).send('Erreur lors de la déconnexion');
    }
    res.redirect('/auth/login'); // Rediriger vers la page de login après la déconnexion
  });
};

module.exports = { login, logout }; // Ajoutez logout ici
