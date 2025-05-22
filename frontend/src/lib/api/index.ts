export interface AwaitOptions {
	onError?: (error: Error) => void;
	onFinally?: () => void;
}

export const getRepoPackages = async (paths: string[], options: AwaitOptions = {}) => {
  try {
    const repo_paths = paths.map((p) => p.trim()).filter((p) => p.length > 0);

    const res = await fetch('http://localhost:8000/repo/packages', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ paths: repo_paths })
    });

    if (!res.ok) throw new Error('Error fetching data');

    return res.json();
  } catch (e: unknown) {
    options.onError?.(e as Error);
  } finally {
    options.onFinally?.();
  }
};
