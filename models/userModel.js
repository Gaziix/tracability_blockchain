  const db = require('../config/database');

  const getUserByEmail = (email, callback) => {
    const query = `
      SELECT users.*, companies.company_name, companies.phone_number AS company_phone, companies.company_type
      FROM users
      LEFT JOIN companies ON users.company_id = companies.id
      WHERE users.email = ?`;
    db.query(query, [email], callback);
  };

  module.exports = {
    getUserByEmail,
  };
