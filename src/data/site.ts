/**
 * Global site settings. Edit copy that appears in more than one place here.
 */
export const site = {
  /**
   * Visual theme. 'original' = faithful wireframe build, '2026' = tinker refresh.
   * Preview the other one in a browser with ?theme=original or ?theme=2026 (?theme=reset to clear).
   */
  theme: '2026' as 'original' | '2026',
  name: 'Peter Rebik',
  title: 'Peter Rebik — Designer & Art Director',
  description:
    'Designer and art director bridging strategy and execution, helping organisations define their visual presence across every touchpoint.',
  email: 'peterrebik@gmail.com',
  get mailto() {
    return `mailto:${this.email}`;
  },
  tagline:
    'I’m a graphic designer and art director that bridges strategy and execution, helping organisations define their visual presence across every touchpoint.',
  /** Words that scroll in the lime band under the hero. */
  marquee: ['Peter Rebik', 'Art Direction', 'Peter Rebik', 'Graphic Design'],
};

/** Header navigation (desktop + mobile menu). */
export const nav = [
  { label: 'Skills', href: '/#help' },
  { label: 'Work', href: '/#work' },
  { label: 'Reviews', href: '/#reviews' },
  { label: 'About', href: '/#about' },
];

/** Footer "Quick Links" — sections in page order. */
export const quickLinks = [
  { label: 'Intro', href: '/#intro' },
  { label: 'How I Can Help', href: '/#help' },
  { label: 'Work Examples', href: '/#work' },
  { label: 'Reviews', href: '/#reviews' },
  { label: 'Additional Info', href: '/#about' },
];
