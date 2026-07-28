/**
 * WPAI / PyMason auth configuration
 * Host this next to index.html on wpaistudio.net.
 *
 * Production: set endpoint to your backend login API:
 *   POST { username, password } → { ok, token, user: { name, email } }
 * Or disable demoUsers and only accept server auth.
 */
window.WPAI_AUTH = window.WPAI_AUTH || {
  studioName: 'Wizard Productions AI Studio',
  studioUrl: 'https://wpaistudio.net',
  gumroadUrl: 'https://wpaistudio.gumroad.com',
  githubUrl: 'https://github.com/MrWizard94-Compile',
  /** Optional server login. null = local demo users only */
  endpoint: null,
  /** Session lifetime in hours */
  sessionHours: 72,
  /** Allow local demo accounts (turn off on public production if you only use API) */
  allowDemo: true,
  /**
   * Demo / seed accounts (client-side). Replace or remove for production.
   * Passwords are checked in-browser — fine for invite-only demos; use endpoint for real security.
   */
  demoUsers: [
    { username: 'studio', password: 'wpai-forge', displayName: 'Studio' },
    { username: 'wizard', password: 'weaponized', displayName: 'Mrwizard94' },
  ],
};
