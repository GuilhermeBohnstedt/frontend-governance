<script lang="ts">
	import { onMount } from 'svelte';
	import * as d3 from 'd3';

	let showModal = $state<boolean>(false);

	let d3Container: HTMLDivElement;

	onMount(() => {
		const width = window.innerWidth;
		const height = window.innerHeight;

		// Limpa o container
		d3.select(d3Container).selectAll('*').remove();

		const svg = d3
			.select(d3Container)
			.append('svg')
			.attr('width', width)
			.attr('height', height)
			.style('display', 'block');

		// Exemplo: desenha um círculo centralizado
		svg
			.append('circle')
			.attr('cx', width / 2)
			.attr('cy', height / 2)
			.attr('r', 80)
			.attr('fill', 'steelblue');
	});
</script>

<button
	class="fixed right-4 top-4 z-20 rounded bg-blue-600 px-4 py-2 text-white shadow"
	onclick={() => (showModal = true)}
>
	Open Modal
</button>

<div bind:this={d3Container} class="d3-fullscreen z-0"></div>

{#if showModal}
	<div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-blend-exclusion">
		<div class="w-full max-w-md rounded-lg bg-white p-6 shadow-lg">
			<h2 class="mb-4 text-xl font-bold">Tailwind Modal</h2>
			<p>This is a modal using Tailwind classes only.</p>
			<button
				class="mt-6 rounded bg-gray-700 px-4 py-2 text-white"
				onclick={() => (showModal = false)}
			>
				Close
			</button>
		</div>
	</div>
{/if}

<style>
	.d3-fullscreen {
		position: fixed;
		inset: 0;
		width: 100vw;
		height: 100vh;
		z-index: 10;
		background: white;
	}
</style>
