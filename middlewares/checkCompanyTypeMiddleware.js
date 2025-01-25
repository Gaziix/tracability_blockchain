const checkCompanyType = (requiredType) => {
    return (req, res, next) => {
      if (req.session && req.session.user) {
        const user = req.session.user;
        if (user.company_type === requiredType) {
          return next(); // Allow access if the company type matches
        } else {
          return res.status(403).send('<h1>Accès interdit : type de compagnie non autorisé.</h1>'); // Forbidden if the type does not match
        }
      } else {
        return res.status(401).send('<h1>Utilisateur non authentifié.</h1>'); // Unauthorized if no session
      }
    };
  };
  
  module.exports = { checkCompanyType };
  