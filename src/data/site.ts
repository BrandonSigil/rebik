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
    'I’m a graphic designer and art director who bridges strategy and execution, helping organisations define their visual presence across every touchpoint.',
  /** Footer sign-off in the 2026 theme (the Intro already uses the tagline). */
  footerLine: 'Designer + art director. Brand systems, campaigns and digital experiences.',
  /** Words that scroll in the lime band under the hero. */
  marquee: ['Peter Rebik', 'Art Direction', 'Peter Rebik', 'Graphic Design'],
};

/** Header navigation (desktop + mobile menu). Follows the section order of the active theme. */
export const nav =
  site.theme === '2026'
    ? [
        { label: 'Work', href: '/work' },
        { label: 'Skills', href: '/#help' },
        { label: 'Reviews', href: '/#reviews' },
        { label: 'About', href: '/#about' },
      ]
    : [
        { label: 'Skills', href: '/#help' },
        { label: 'Work', href: '/work' },
        { label: 'Reviews', href: '/#reviews' },
        { label: 'About', href: '/#about' },
      ];

/** Footer "Quick Links" — sections in page order. */
export const quickLinks =
  site.theme === '2026'
    ? [
        { label: 'Intro', href: '/#intro' },
        { label: 'Work Examples', href: '/#work' },
        { label: 'What I Bring', href: '/#help' },
        { label: 'Reviews', href: '/#reviews' },
        { label: 'Additional Info', href: '/#about' },
      ]
    : [
        { label: 'Intro', href: '/#intro' },
        { label: 'How I Can Help', href: '/#help' },
        { label: 'Work Examples', href: '/#work' },
        { label: 'Reviews', href: '/#reviews' },
        { label: 'Additional Info', href: '/#about' },
      ];
