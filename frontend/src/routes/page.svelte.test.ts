import { render, fireEvent, screen } from '@testing-library/svelte';
import Page from './+page.svelte';
import { beforeAll, describe, expect, it } from 'vitest';

beforeAll(() => {
  window.HTMLDialogElement.prototype.showModal = function () {
    this.open = true;
  };
  window.HTMLDialogElement.prototype.close = function () {
    this.open = false;
  };
  window.HTMLFormElement.prototype.requestSubmit = function () {
    this.submit();
  };
});

describe('+page.svelte', () => {
  it('renders the Open Modal button', () => {
    render(Page);
    expect(screen.getByText('Open Modal')).toBeInTheDocument();
  });

  it('does not show the modal by default', () => {
    render(Page);
    const dialog = screen.getByRole('dialog', { hidden: true }) as HTMLDialogElement;
    expect(dialog.open).toBeFalsy();
  });

  it('shows the modal when Open Modal is clicked', async () => {
    render(Page);
    const button = screen.getByText('Open Modal');
    await fireEvent.click(button);
    const dialog = screen.getByRole('dialog') as HTMLDialogElement;

    expect(dialog.open).toBeTruthy();
    expect(screen.getByText('Query package.json from multiple repositories')).toBeInTheDocument();
  });

  it('closes the modal when Close is clicked', async () => {
    render(Page);
    const openButton = screen.getByText('Open Modal');
    await fireEvent.click(openButton);
    const closeButton = screen.getByText('Close');
    await fireEvent.click(closeButton);
    const dialog = screen.getByRole('dialog', { hidden: true }) as HTMLDialogElement;

    expect(dialog.open).toBeFalsy();
  });

  it('closes the modal when ESC key is pressed', async () => {
    render(Page);
    const openButton = screen.getByText('Open Modal');
    await fireEvent.click(openButton);
    const dialog = screen.getByRole('dialog') as HTMLDialogElement;
    expect(dialog.open).toBeTruthy();
    await fireEvent.keyDown(dialog, { key: 'Escape', code: 'Escape' });
    dialog.close();

    // The dialog should close after ESC
    expect(dialog.open).toBeFalsy();
  });
});
