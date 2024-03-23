module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  ignorePatterns: ['dist', '.eslintrc.js', 'vite.config.js'],
  parserOptions: { ecmaVersion: 'latest', sourceType: 'module' },
  plugins: ['import'],
  extends: [
    'eslint:recommended',
    'plugin:vue/essential',
    'plugin:prettier/recommended',
    'airbnb'
  ],
  rules: {
    'vue/order-in-components': [
      'error',
      {
        order: [
          'name',
          'directives',
          'components',
          'mixins',
          ['provide', 'inject'],
          'model',
          'props',
          'filters',
          'data',
          'computed',
          'watch',
          'methods',
          'LIFECYCLE_HOOKS',
          'ROUTER_GUARDS',
        ],
      },
    ],
    'vue/v-for-delimiter-style': ['error', 'of'],
    'vue/next-tick-style': ['error', 'promise'],
    'vue/require-prop-types': 'error',
    'vue/prop-name-casing': ['error', 'camelCase'],
    'vue/component-name-in-template-casing': ['error', 'PascalCase'],
    'vue/component-definition-name-casing': ['error', 'PascalCase'],
    'vue/custom-event-name-casing': ['error', 'camelCase'],
    'vue/no-duplicate-attr-inheritance': 'error',
    'vue/this-in-template': ['error', 'never'],
    'vue/v-on-style': ['error', 'shorthand'],
    'vue/no-multi-spaces': 'error',
    'vue/padding-line-between-blocks': 'error',
    'vue/component-tags-order': [
      'error',
      {
        order: ['template', 'script', 'style'],
      },
    ],
    'vue/v-on-event-hyphenation': ['error', 'never'],
    'vue/attribute-hyphenation': ['error', 'never'],
    'vue/v-bind-style': 'error',
    'vue/v-slot-style': ['error', 'shorthand'],
    'vue/no-unused-properties': [
      'error',
      {
        groups: ['props', 'data', 'computed', 'methods', 'setup'],
        ignorePublicMembers: true,
      },
    ],
  }
}
