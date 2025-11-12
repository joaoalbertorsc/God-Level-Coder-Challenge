module.exports = {
  root: true,
  env: {
    node: true
  },
  'extends': [
    'plugin:vue/vue3-essential',
    'eslint:recommended'
  ],
  // Use the official parser for Vue 3
  parser: 'vue-eslint-parser',
  parserOptions: {
    // The vue-eslint-parser uses this parser for the <script> block
    parser: '@babel/eslint-parser',
    requireConfigFile: false, // This is the key to disable the babel config requirement
    ecmaVersion: 2020,
    sourceType: 'module'
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off'
  }
}
