module.exports = {
    "env": {
        "node": true,
        "browser": true,
        "commonjs": true,
        "es2021": true
    },
    "extends": [
        "eslint:recommended",
        "plugin:react/recommended"
    ],
    "parserOptions": {
        "ecmaFeatures": {
            "jsx": true
        },
        "ecmaVersion": 12,
        "sourceType": "module"
    },
    "plugins": [
        "react"
    ],
    "rules": {
      "no-unused-vars" : [1, { "varsIgnorePattern": "[iI]gnored" }]
    },
    "settings": {
      "react": {
        "version": "999.9.999"
      }
    },
};
