<script lang="ts">
	import type { PackageResult } from '$lib/models';
	import { getRepoPackages } from '$lib/api';

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

<h1 class="mb-6 text-2xl font-bold">Consultar package.json de múltiplos repositórios</h1>

<form onsubmit={submit} class="space-y-4">
	{#each paths as path, i (i)}
		<div class="flex items-center gap-2">
			<input
				type="text"
				bind:value={paths[i]}
				placeholder="/caminho/para/repo"
				class="w-96 rounded border px-3 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
			/>
			{#if paths.length > 1}
				<button
					type="button"
					onclick={() => paths.splice(i, 1)}
					class="rounded bg-red-500 px-3 py-1 text-white transition hover:bg-red-600"
				>
					Remover
				</button>
			{/if}
		</div>
	{/each}
	<div class="flex gap-2">
		<button
			type="button"
			onclick={() => (paths = [...paths, ''])}
			class="rounded bg-blue-500 px-3 py-1 text-white transition hover:bg-blue-600"
		>
			Adicionar campo
		</button>
		<button
			type="submit"
			disabled={loading}
			class="rounded bg-green-600 px-4 py-2 text-white transition hover:bg-green-700 disabled:opacity-50"
		>
			Consultar
		</button>
	</div>
</form>

{#if loading}
	<p class="mt-4 font-semibold text-blue-600">Consultando...</p>
{/if}

{#if error}
	<p class="mt-4 font-semibold text-red-600">{error}</p>
{/if}

{#if results.length}
	<h2 class="mb-4 mt-8 text-xl font-semibold">Resultados:</h2>
	<ul class="space-y-6">
		{#each results as result}
			<li class="rounded border bg-gray-50 p-4">
				<strong class="block text-gray-800">{result.repo_path}</strong>
				{#if result.package}
					<pre class="mt-2 overflow-x-auto rounded bg-gray-100 p-2 text-sm">{JSON.stringify(
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