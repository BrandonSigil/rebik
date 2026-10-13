/**
 * Virtual CV — rendered at the bottom of the About section (2026 theme, AboutCV.astro).
 * Source: Peter's LinkedIn profile (Oct 2026) and the "Programs" list on the old peterrebik.com/about.
 * Keep this in step with LinkedIn: recruiters cross-check the two.
 */
export interface Role { title: string; start: string; end: string; mode?: string; summary: string }
export interface Job { org: string; type?: string; location: string; roles: Role[] }

export const experience: Job[] = [
  {
    org: 'Pierce Transit',
    type: 'Full-time',
    location: 'Lakewood, Washington',
    roles: [
      {
        title: 'Marketing Coordinator',
        start: 'Sep 2023', end: 'Present', mode: 'Hybrid',
        summary: 'Lead brand and creative strategy across web, campaigns, lifecycle communications and environmental design, improving consistency across 5+ departments.',
      },
      {
        title: 'Marketing Analyst',
        start: 'Mar 2021', end: 'Sep 2023', mode: 'Hybrid',
        summary: 'Designed and launched multi-channel campaigns across web, print and digital, simplifying complex policy and service information into clear visual narratives.',
      },
      {
        title: 'Marketing Specialist',
        start: 'Mar 2020', end: 'Mar 2021', mode: 'Remote',
        summary: 'Produced campaign, report and promotional assets while maintaining brand consistency and ADA compliance.',
      },
    ],
  },
  {
    org: 'Rebik Design',
    type: 'Self-employed',
    location: 'Tacoma, Washington',
    roles: [
      {
        title: 'Freelance Designer and Strategist',
        start: 'Jan 2017', end: 'Oct 2024', mode: 'Remote',
        summary: 'Led end-to-end brand and website projects for start-ups and regional organisations, clarifying positioning and strengthening go-to-market messaging.',
      },
    ],
  },
  {
    org: 'Gateway Church',
    location: 'Brawley, California',
    roles: [
      {
        title: 'Graphic Designer',
        start: 'Feb 2013', end: 'Dec 2017', mode: 'On-site',
        summary: 'Produced integrated print, digital and multimedia campaigns supporting events and organisational messaging.',
      },
    ],
  },
];

export const education = [
  { school: 'San Diego State University', award: 'Bachelor’s degree, Anthropology', years: '2007–2011' },
];

/** Tools he's proficient in (no proficiency bars, by request). */
export const tools = [
  'Adobe InDesign',
  'Adobe Illustrator',
  'Adobe Photoshop',
  'Adobe Premiere Pro',
  'Figma',
  'WordPress',
  'HubSpot',
  'Microsoft 365',
];
