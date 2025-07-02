<script lang="ts">
	import type { PackageResult } from '$lib/models';
	import { getRepoPackages } from '$lib/api';

	interface Props {
		onAccept: (results: PackageResult[]) => void;
	}

	const { onAccept }: Props = $props();

	let paths = $state<string[]>(['']);
	let results = $state<PackageResult[]>([]);
	let loading = $state<boolean>(false);
	let error = $state<string | null>(null);

	async function submit() {
		loading = true;
		error = null;

		results = await getRepoPackages(paths, {
			onError: (err) => {
				error = err.message;
				loading = false;
			},
			onFinally: () => {
				loading = false;
			}
		});
	}
</script>

<h2 class="mb-6 text-2xl font-bold">Query package.json from multiple repositories</h2>

<form onsubmit={submit} class="space-y-4">
	{#each paths as path, i (i)}
		<div class="flex items-center gap-2">
			<label class="input">
				Path
				<input type="text" class="grow" placeholder="src/app/" bind:value={paths[i]} />
			</label>
			{#if paths.length > 1}
				<button type="button" onclick={() => paths.splice(i, 1)} class="btn btn-error">
					Remove
				</button>
			{/if}
		</div>
	{/each}
	<div class="flex gap-2">
		<button type="button" onclick={() => (paths = [...paths, ''])} class="btn btn-primary">
			Add Path
		</button>
		<button type="submit" disabled={loading} class="btn btn-success"> Find </button>
		<button type="button" disabled={loading} class="btn btn-neutral" onclick={() => onAccept(results)}> Accept </button>

	</div>
</form>

{#if loading}
	<span class="loading loading-ring loading-xl"></span>
{/if}

{#if error}
	<div role="alert" class="alert alert-error">
		<svg
			xmlns="http://www.w3.org/2000/svg"
			class="h-6 w-6 shrink-0 stroke-current"
			fill="none"
			viewBox="0 0 24 24"
		>
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
			/>
		</svg>
		<span>{error}</span>
	</div>
{/if}

{#if results.length}
	<h2 class="mb-4 mt-8 text-xl font-semibold">Resultados:</h2>
	<ul class="space-y-6">
		{#each results as result}
			<li class="rounded border p-4 border-zinc-600">
				<strong class="block">{result.repo_path}</strong>
				{#if result.package}
					<pre class="mt-2 overflow-x-auto rounded p-2 text-sm">{JSON.stringify(
							result.package,
							null,
							2
						)}</pre>
				{:else}
					<span class="mt-2 block text-red-500">{result.error}</span>
				{/if}
			</li>
		{/each}
	</ul>
{/if}
