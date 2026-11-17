import type { ImageMetadata } from 'astro';

/**
 * srcset widths and `sizes` for an image shown with object-fit: cover in a fixed-ratio card.
 * An image wider than the card renders wider than the card, so `sizes` is scaled by that
 * overflow. Otherwise the browser picks a file sized to the card and stretches it.
 * `cardRatio` is width / height. `slot` is the card's CSS width, per media query.
 */
export function cardImage(src: ImageMetadata, cardRatio: number, slot: { mobile: string; desktop: string }) {
  const k = Math.max(1, src.width / src.height / cardRatio).toFixed(2);
  const widths = [360, 560, 800, 1100, 1500, 2000].filter((w) => w <= src.width);
  return {
    widths: widths.length ? widths : [src.width],
    sizes: `(max-width: 760px) calc(${slot.mobile} * ${k}), calc(${slot.desktop} * ${k})`,
  };
}
