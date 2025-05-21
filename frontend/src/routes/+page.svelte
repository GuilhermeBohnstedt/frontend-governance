<script lang="ts">
	import type { PackageResult } from "$lib/models";

	let paths = $state<string>('');
	let results = $state<PackageResult[]>([]);
	let loading = $state<boolean>(false);
	let error = $state<string | null>(null);

	async function submit() {
		loading = true;
		error = null;
		try {
			const repo_paths = paths
				.split('\n')
				.map((p) => p.trim())
				.filter((p) => p.length > 0);

			const res = await fetch('http://localhost:8000/repo/packages', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(repo_paths)
			});
			if (!res.ok) throw new Error('Error fetching data');
			results = await res.json();
		} catch (e: unknown) {
			error = (e as Error).message;
		} finally {
			loading = false;
		}
	}
</script>

<h1>Consultar package.json de múltiplos repositórios</h1>

<form onsubmit={submit}>
	<label for="paths">Caminhos dos repositórios (um por linha):</label><br />
	<textarea
		id="paths"
		bind:value={paths}
		rows="6"
		cols="60"
		placeholder="/caminho/para/repo1&#10;/caminho/para/repo2"
	></textarea><br />
	<button type="submit" disabled={loading}>Consultar</button>
</form>

{#if loading}
	<p>Consultando...</p>
{/if}

{#if error}
	<p style="color: red;">{error}</p>
{/if}

{#if results.length}
	<h2>Resultados:</h2>
	<ul>
		{#each results as result}
			<li>
				<strong>{result.repo_path}</strong><br />
				{#if result.package}
					<pre>{JSON.stringify(result.package, null, 2)}</pre>
				{:else}
					<span style="color: red;">{result.error}</span>
				{/if}
			</li>
		{/each}
	</ul>
{/if}
