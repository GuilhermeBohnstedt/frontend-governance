// filepath: frontend/src/routes/test_+page.svelte
import { render, fireEvent } from '@testing-library/svelte';
import { describe, it, expect } from 'vitest';
import Page from './+page.svelte';

describe('+page.svelte', () => {
  it('renders the D3 container and SVG', async () => {
    const { container } = render(Page);
    const d3Div = container.querySelector('.d3-fullscreen');
    expect(d3Div).toBeTruthy();
    // Wait for onMount to run and SVG to be appended
    await new Promise(r => setTimeout(r, 10));
    const svg = d3Div?.querySelector('svg');
    expect(svg).toBeTruthy();
  });

  it('does not show the modal by default', () => {
    const { queryByText } = render(Page);
    expect(queryByText('Tailwind Modal')).toBeNull();
  });

  it('shows the modal when "Open Modal" is clicked', async () => {
    const { getByText, queryByText } = render(Page);
    const openBtn = getByText('Open Modal');
    await fireEvent.click(openBtn);
    expect(queryByText('Tailwind Modal')).toBeTruthy();
  });

  it('closes the modal when "Close" is clicked', async () => {
    const { getByText, queryByText } = render(Page);
    const openBtn = getByText('Open Modal');
    await fireEvent.click(openBtn);
    const closeBtn = getByText('Close');
    await fireEvent.click(closeBtn);
    expect(queryByText('Tailwind Modal')).toBeNull();
  });

  it('renders a centered circle in the SVG', async () => {
    const { container } = render(Page);
    const d3Div = container.querySelector('.d3-fullscreen');
    await new Promise(r => setTimeout(r, 10));
    const circle = d3Div?.querySelector('svg circle');
    expect(circle).toBeTruthy();
    expect(circle?.getAttribute('fill')).toBe('steelblue');
  });
});